<p align="center">
  <img src="PowerModeSelector.png" width="150" alt="Power Mode Selector Logo"/>
</p>

<h1 align="center">Power Mode Selector</h1>

<p align="center">
  A lightweight Windows 11 & 10 system tray application for switching power plans instantly.
</p>

<p align="center">
  <a href="https://github.com/canyrtcn/PowerModeSelector/releases">
    <img src="https://img.shields.io/github/v/release/canyrtcn/PowerModeSelector?style=flat-square" alt="Latest Release"/>
  </a>
  <img src="https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-blue?style=flat-square" alt="Platform"/>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square" alt="Python"/>
  <img src="https://img.shields.io/github/license/canyrtcn/PowerModeSelector?style=flat-square" alt="License"/>
</p>

---

## Overview

Power Mode Selector sits quietly in your Windows system tray and lets you switch between all your power plans with just two clicks — no digging through Control Panel required.

**Features:**
- Automatically detects all installed power plans (no hardcoded GUIDs)
- Color-coded tray icon changes based on the active plan
- Optional startup with Windows via Task Scheduler
- Supports Turkish and English Windows installations
- Lightweight (~15 MB), no installation required

---

## Requirements

- Windows 10 or Windows 11
- No additional software required (standalone EXE)

---

## Usage

1. Download `PowerModeSelector.exe` from the [Releases](https://github.com/canyrtcn/PowerModeSelector/releases) page.
2. Run the EXE — a tray icon will appear in the bottom-right corner.
3. Right-click the tray icon to see your power plans.
4. Click any plan to switch to it instantly.

To enable automatic startup with Windows:
- Right-click the tray icon
- Click **"Run at startup"**
- Accept the UAC prompt (administrator permission required for Task Scheduler)

---

## Building from Source

**Requirements:**
```
pip install pystray pillow pyinstaller
```

**Build command:**
```
python -m PyInstaller --onefile --noconsole --icon="ICON.ico" ^
  --hidden-import=pystray._win32 ^
  --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageDraw ^
  --exclude-module=tkinter --exclude-module=numpy --exclude-module=pandas ^
  --name "PowerModeSelector" power_mode_selector.py
```

---

## Antivirus Note

Some antivirus software may flag this application as suspicious because it interacts with Windows Task Scheduler to enable startup functionality. This is a **false positive**. The application does not modify system files, collect data, or communicate over the network.

The full source code is available here for review.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 [canyrtcn](https://github.com/canyrtcn)
