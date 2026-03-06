================================================================================
  Power Mode Selector
  A lightweight Windows system tray application for switching power plans
  GitHub: https://github.com/canyrtcn/PowerModeSelector
================================================================================


OVERVIEW
--------
Power Mode Selector sits quietly in your Windows system tray and lets you
switch between all your power plans with just two clicks — no digging through
Control Panel required.

Features:
  - Automatically detects all installed power plans (no hardcoded GUIDs)
  - Color-coded tray icon changes based on the active plan
  - Optional startup with Windows via Task Scheduler
  - Supports Turkish and English Windows installations
  - Lightweight (~15 MB), no installation required


REQUIREMENTS
------------
  - Windows 10 or Windows 11
  - No additional software required (standalone EXE)


USAGE
-----
1. Download PowerModeSelector.exe from the Releases page.
2. Run the EXE — a tray icon will appear in the bottom-right corner.
3. Right-click the tray icon to see your power plans.
4. Click any plan to switch to it instantly.

To enable automatic startup with Windows:
  - Right-click the tray icon
  - Click "Run at startup"
  - Accept the UAC prompt (administrator permission required for Task Scheduler)


BUILDING FROM SOURCE
--------------------
Requirements:
  - Python 3.8+
  - pip install pystray pillow pyinstaller

Build command:
  python -m PyInstaller --onefile --noconsole --icon="ICON.ico" ^
    --hidden-import=pystray._win32 ^
    --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageDraw ^
    --exclude-module=tkinter --exclude-module=numpy --exclude-module=pandas ^
    --name "PowerModeSelector" power_mode_selector.py


ANTIVIRUS NOTE
--------------
Some antivirus software may flag this application as suspicious because it
interacts with Windows Task Scheduler to enable startup functionality.
This is a false positive. The application does not modify system files,
collect data, or communicate over the network.

If your antivirus blocks the EXE, please add it to your exclusion list.
The full source code is available on GitHub for review.


LICENSE
-------
This project is licensed under the MIT License.
See the LICENSE file for details.

Copyright (c) 2026 canyrtcn (https://github.com/canyrtcn)


AUTHOR
------
  GitHub : https://github.com/canyrtcn

================================================================================
