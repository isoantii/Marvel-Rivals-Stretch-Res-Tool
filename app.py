import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog

# -----------------------------
# CONFIG LOCATION
# -----------------------------

if getattr(sys, "frozen", False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(APP_DIR, "config.json")

SECTION = "[/Script/Marvel.MarvelGameUserSettings]"

RESOLUTIONS_BY_ASPECT = {
    "16:9": [
        "1280x720",
        "1600x900",
        "1920x1080",
        "2560x1440",
        "3840x2160"
    ],
    "16:10": [
        "1280x800",
        "1440x900",
        "1680x1050",
        "1920x1200",
        "2560x1600"
    ]
}

# -----------------------------
# CONFIG
# -----------------------------

def detect_game_user_settings():

    local = os.environ.get("LOCALAPPDATA")

    if not local:
        return ""

    path = os.path.join(
        local,
        "Marvel",
        "Saved",
        "Config",
        "Windows",
        "GameUserSettings.ini"
    )

    if os.path.exists(path):
        return path

    return ""


def detect_launcher():

    path = r"C:\Program Files (x86)\Steam\steamapps\common\MarvelRivals\MarvelRivals_Launcher.exe"

    if os.path.exists(path):
        return path

    return ""


def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def load_config():

    if os.path.exists(CONFIG_FILE):

        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)

    else:

        cfg = {
            "ini_path": "",
            "exe_path": ""
        }

    # FIRST RUN DETECTION

    if not cfg["ini_path"]:
        detected = detect_game_user_settings()
        if detected:
            cfg["ini_path"] = detected

    if not cfg["exe_path"]:
        detected = detect_launcher()
        if detected:
            cfg["exe_path"] = detected

    save_config(cfg)

    return cfg


config = load_config()

# -----------------------------
# READONLY CONTROL
# -----------------------------

def remove_readonly(path):

    try:
        os.chmod(path, 0o666)
        subprocess.run(["attrib", "-r", path], shell=False)
    except:
        pass


def set_readonly(path):

    try:
        subprocess.run(["attrib", "+r", path], shell=False)
    except:
        pass


if config["ini_path"]:
    remove_readonly(config["ini_path"])

# -----------------------------
# RESOLUTION EDIT
# -----------------------------

def set_resolution(path, width, height):

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_section = False

    for i, line in enumerate(lines):

        if line.strip() == SECTION:
            in_section = True
            continue

        if in_section and line.startswith("["):
            break

        if in_section:

            if line.startswith("ResolutionSizeX"):
                lines[i] = f"ResolutionSizeX={width}\n"

            if line.startswith("ResolutionSizeY"):
                lines[i] = f"ResolutionSizeY={height}\n"

            if line.startswith("LastUserConfirmedResolutionSizeX"):
                lines[i] = f"LastUserConfirmedResolutionSizeX={width}\n"

            if line.startswith("LastUserConfirmedResolutionSizeY"):
                lines[i] = f"LastUserConfirmedResolutionSizeY={height}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)


# -----------------------------
# UI FUNCTIONS
# -----------------------------

def update_resolutions(event=None):

    ratio = aspect_var.get()
    options = RESOLUTIONS_BY_ASPECT.get(ratio, [])

    resolution_combo["values"] = options

    if options:
        resolution_var.set(options[0])


def save_resolution():

    res = resolution_var.get()
    w, h = res.split("x")

    set_resolution(config["ini_path"], w, h)

    set_readonly(config["ini_path"])

    root.destroy()


def save_and_launch():

    res = resolution_var.get()
    w, h = res.split("x")

    set_resolution(config["ini_path"], w, h)

    set_readonly(config["ini_path"])

    subprocess.Popen([config["exe_path"]])

    root.destroy()


# -----------------------------
# SETTINGS WINDOW
# -----------------------------

def open_settings():

    win = tk.Toplevel(root)
    win.title("Settings")
    win.geometry("520x200")
    win.resizable(False, False)

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="GameUserSettings.ini").grid(row=0, column=0, sticky="w")

    ini_var = tk.StringVar(value=config.get("ini_path", ""))

    ini_entry = ttk.Entry(frame, textvariable=ini_var, width=50)
    ini_entry.grid(row=1, column=0, padx=(0,10))

    def browse_ini():
        path = filedialog.askopenfilename(filetypes=[("INI", "*.ini")])
        if path:
            ini_var.set(path)

    ttk.Button(frame, text="Browse", command=browse_ini).grid(row=1, column=1)

    ttk.Label(frame, text="MarvelRivals_Launcher.exe").grid(row=2, column=0, sticky="w", pady=(15,0))

    exe_var = tk.StringVar(value=config.get("exe_path", ""))

    exe_entry = ttk.Entry(frame, textvariable=exe_var, width=50)
    exe_entry.grid(row=3, column=0, padx=(0,10))

    def browse_exe():
        path = filedialog.askopenfilename(filetypes=[("EXE", "*.exe")])
        if path:
            exe_var.set(path)

    ttk.Button(frame, text="Browse", command=browse_exe).grid(row=3, column=1)

    def save_paths():

        config["ini_path"] = ini_var.get()
        config["exe_path"] = exe_var.get()

        save_config(config)

        win.destroy()

    ttk.Button(frame, text="Save", command=save_paths).grid(row=4, column=1, pady=15)

# -----------------------------
# MAIN WINDOW
# -----------------------------

root = tk.Tk()
root.title("Marvel Rivals Resolution Tool")
root.geometry("360x200")
root.resizable(False, False)

main = ttk.Frame(root, padding=20)
main.pack(fill="both", expand=True)

# settings cog
ttk.Button(main, text="⚙", width=3, command=open_settings).pack(anchor="ne")

# aspect ratio
ttk.Label(main, text="Aspect Ratio").pack(pady=(5,5))

aspect_var = tk.StringVar(value="16:9")

aspect_combo = ttk.Combobox(
    main,
    textvariable=aspect_var,
    values=["16:9", "16:10"],
    state="readonly",
    width=20
)

aspect_combo.pack()

aspect_combo.bind("<<ComboboxSelected>>", update_resolutions)

# resolution
ttk.Label(main, text="Resolution").pack(pady=(12,5))

resolution_var = tk.StringVar()

resolution_combo = ttk.Combobox(
    main,
    textvariable=resolution_var,
    state="readonly",
    width=20
)

resolution_combo.pack()

update_resolutions()

# buttons
btn_row = ttk.Frame(main)
btn_row.pack(pady=15)

ttk.Button(btn_row, text="Save", command=save_resolution).pack(side="left", padx=6)

ttk.Button(btn_row, text="Save + Start", command=save_and_launch).pack(side="left", padx=6)

root.mainloop()