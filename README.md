# Marvel Rivals Stretch Res Tool

A simple Windows tool for setting custom resolutions in Marvel Rivals. Pick an aspect ratio and resolution, hit save, and the game's config is updated and locked to read-only so it sticks.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey)

## Features

- Set resolution from preset 16:9 and 16:10 options because 16:# is the only res that gives no black bars.
- Automatically detects `GameUserSettings.ini` and the game launcher
- Locks the INI to read-only after saving so the game doesn't overwrite it
- Optional "Save + Start" button to apply and launch the game in one click
- Settings menu to manually configure file paths

## Download

Grab `MR Res.exe` from [Releases](../../releases) or clone the repo and run from source.

## Usage

1. Run `MR Res.exe` (or `python app.py`)
2. Select your aspect ratio and resolution
3. Click **Save** to apply, or **Save + Start** to apply and launch Marvel Rivals

Use the gear icon to configure paths if auto-detection doesn't find your install.

## Building from Source

```bash
pip install pyinstaller
pyinstaller MRResolution.spec
```

The built exe will be in `dist/`.

## Config

`config.json` stores the paths to your game settings and launcher:

```json
{
  "ini_path": "C:\\Users\\...\\GameUserSettings.ini",
  "exe_path": "C:\\Program Files (x86)\\Steam\\...\\MarvelRivals_Launcher.exe"
}
```

Both are auto-detected on first run if Marvel Rivals is installed in the default Steam location.
