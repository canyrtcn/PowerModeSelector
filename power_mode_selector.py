# -*- coding: utf-8 -*-
import subprocess, re, sys, os, ctypes, time
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item

APP_NAME  = "Power Mode Selector"
TASK_NAME = "PowerModeSelector"

_APPDATA_BASE    = os.path.join(os.getenv("LOCALAPPDATA") or os.path.expanduser("~"), APP_NAME)
FIRST_RUN_MARKER = os.path.join(_APPDATA_BASE, ".first_run")
DO_ENABLE_FLAG   = os.path.join(_APPDATA_BASE, ".do_enable")
DO_DISABLE_FLAG  = os.path.join(_APPDATA_BASE, ".do_disable")

def get_exe_path():
    return sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)

def _startupinfo():
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE
    return si

def _is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except:
        return False

def is_startup_enabled():
    try:
        r = subprocess.run(["schtasks", "/query", "/tn", TASK_NAME],
                           capture_output=True, startupinfo=_startupinfo())
        return r.returncode == 0
    except:
        return False

def _schtasks_create():
    exe = get_exe_path()
    subprocess.run(["schtasks", "/create", "/tn", TASK_NAME,
                    "/tr", f'"{exe}"', "/sc", "ONLOGON", "/f"],
                   capture_output=True, startupinfo=_startupinfo())

def _schtasks_delete():
    subprocess.run(["schtasks", "/delete", "/tn", TASK_NAME, "/f"],
                   capture_output=True, startupinfo=_startupinfo())

def enable_startup():
    if _is_admin():
        _schtasks_create()
    else:
        os.makedirs(_APPDATA_BASE, exist_ok=True)
        open(DO_ENABLE_FLAG, "w").close()
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", get_exe_path(), None, None, 0
        )
        for _ in range(10):
            time.sleep(0.5)
            if is_startup_enabled():
                break

def disable_startup():
    if _is_admin():
        _schtasks_delete()
    else:
        os.makedirs(_APPDATA_BASE, exist_ok=True)
        open(DO_DISABLE_FLAG, "w").close()
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", get_exe_path(), None, None, 0
        )
        for _ in range(10):
            time.sleep(0.5)
            if not is_startup_enabled():
                break

def is_first_run():
    return not os.path.exists(FIRST_RUN_MARKER)

def mark_as_run():
    os.makedirs(_APPDATA_BASE, exist_ok=True)
    open(FIRST_RUN_MARKER, "w").close()

def show_welcome_message():
    ctypes.windll.user32.MessageBoxW(
        0,
        "Thank you for using Power Mode Selector.\n\n"
        "You can switch between your Windows power plans quickly "
        "from the system tray icon.\n\n"
        "To enable automatic startup with Windows, simply click the "
        "tray icon and check \"Run at startup\" from the menu.\n\n"
        "Enjoy seamless power management.",
        "Welcome to Power Mode Selector",
        0x00000040
    )

def _decode(raw):
    for enc in ["cp857", "cp1254", "cp1252", "utf-8", "latin-1"]:
        try:
            text = raw.decode(enc)
            if any(c in text for c in "ğüşıöçĞÜŞİÖÇ"):
                return text
        except: continue
    return raw.decode("utf-8", errors="replace")

def _run(args):
    return _decode(subprocess.run(args, capture_output=True, startupinfo=_startupinfo()).stdout)

def get_power_plans():
    plans = []
    for line in _run(["powercfg", "/list"]).splitlines():
        if "GUID" not in line.upper(): continue
        gm = re.search(r'([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})', line)
        if not gm: continue
        nm = re.search(r'\((.+?)\)', line)
        plans.append({"guid": gm.group(1), "name": nm.group(1).strip() if nm else gm.group(1)})
    return plans

def get_active_plan_guid():
    m = re.search(r'([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})',
                  _run(["powercfg", "/getactivescheme"]))
    return m.group(1) if m else None

def set_power_plan(guid):
    try:
        subprocess.run(["powercfg", "/setactive", guid], check=True,
                       capture_output=True, startupinfo=_startupinfo())
        return True
    except: return False

ICON_COLORS = [
    (["ultra", "minimum"],                  ("#0a3d6b", "#82b1ff")),
    (["tasarruf", "saver", "eco", "save"],  ("#1565c0", "#64b5f6")),
    (["dengeli", "balanced", "normal"],     ("#2e7d32", "#81c784")),
    (["yüksek", "high", "performance"],     ("#e65100", "#ffb74d")),
    (["ultimate", "boost", "game", "oyun"],("#b71c1c", "#ef9a9a")),
]

def get_color_for_plan(name):
    lower = name.lower()
    for kws, colors in ICON_COLORS:
        if any(k in lower for k in kws): return colors
    return ("#6a1b9a", "#ce93d8")

def make_icon(name):
    size = 64
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    bg, fg = get_color_for_plan(name)
    draw.ellipse([2,2,size-2,size-2], fill=bg)
    draw.arc([10,10,size-10,size-10], start=130, end=50, fill=fg, width=6)
    draw.line([size//2,10,size//2,size//2], fill=fg, width=6)
    return img

_icon_cache = {}
def get_icon(name):
    if name not in _icon_cache: _icon_cache[name] = make_icon(name)
    return _icon_cache[name]

def toggle_startup(tray):
    if is_startup_enabled(): disable_startup()
    else: enable_startup()
    tray.menu = build_menu(tray)

def build_menu(tray):
    plans = get_power_plans()
    active_guid = (get_active_plan_guid() or "").lower()
    menu_items = []
    for plan in plans:
        guid, name = plan["guid"], plan["name"]
        is_active = guid.lower() == active_guid
        label = f"✔  {name}" if is_active else f"      {name}"
        def make_cb(g, n):
            def cb(icon, _):
                if set_power_plan(g):
                    icon.icon = get_icon(n)
                    icon.title = f"Power: {n}"
                    icon.menu = build_menu(icon)
            return cb
        menu_items.append(item(label, make_cb(guid, name)))
    menu_items.append(pystray.Menu.SEPARATOR)
    startup_label = "✔  Run at startup" if is_startup_enabled() else "      Run at startup"
    menu_items.append(item(startup_label, lambda icon, _: toggle_startup(icon)))
    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(item("🔄  Refresh", lambda icon, _: refresh(icon)))
    menu_items.append(item("❌  Exit", lambda icon, _: icon.stop()))
    return pystray.Menu(*menu_items)

def refresh(tray):
    plans = get_power_plans()
    active_guid = (get_active_plan_guid() or "").lower()
    active_name = next((p["name"] for p in plans if p["guid"].lower() == active_guid), "Power Mode")
    tray.icon = get_icon(active_name)
    tray.title = f"Power: {active_name}"
    tray.menu = build_menu(tray)

def main():
    if _is_admin():
        if os.path.exists(DO_ENABLE_FLAG):
            os.remove(DO_ENABLE_FLAG)
            _schtasks_create()
            sys.exit(0)
        if os.path.exists(DO_DISABLE_FLAG):
            os.remove(DO_DISABLE_FLAG)
            _schtasks_delete()
            sys.exit(0)

    if is_first_run():
        mark_as_run()
        show_welcome_message()

    plans = get_power_plans()
    active_guid = (get_active_plan_guid() or "").lower()
    active_name = next((p["name"] for p in plans if p["guid"].lower() == active_guid), "Power Mode")

    tray = pystray.Icon(name=APP_NAME, icon=get_icon(active_name), title=f"Power: {active_name}")
    tray.menu = build_menu(tray)
    tray.run()

if __name__ == "__main__":
    main()
