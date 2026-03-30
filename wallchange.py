#!/usr/bin/env python3
"""wallChange — automatic wallpaper rotator for Windows."""

import ctypes
import os
import random
import signal
import sys
import time
import winreg

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "wallrc.toml")
THEMES_DIR = os.path.join(SCRIPT_DIR, "themes")
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")

try:
    import tomllib
except ModuleNotFoundError:
    print("Python 3.11+ is required (for tomllib).")
    sys.exit(1)  # 1 = missing dependency

# Windows wallpaper styles: registry values for WallpaperStyle + TileWallpaper
# https://learn.microsoft.com/en-us/windows/win32/controls/themes-overview
SCALING_MAP = {
    #                (WallpaperStyle, TileWallpaper)
    "fill":    ("10", "0"),
    "fit":     ("6",  "0"),
    "stretch": ("2",  "0"),
    "center":  ("0",  "0"),
    "tile":    ("0",  "1"),
    "span":    ("22", "0"),
}

SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02


def load_config():
    defaults = {
        "general": {
            "minutes": 0.25,
            "theme": "default",
            "shuffle": False,
            "scaling": "fill",
        },
    }
    if not os.path.exists(CONFIG_PATH):
        print(f"Config not found at {CONFIG_PATH}, using defaults.")
        return defaults
    with open(CONFIG_PATH, "rb") as f:
        user = tomllib.load(f)
    for section in defaults:
        if section in user:
            defaults[section].update(user[section])
    return defaults


def get_wallpapers(theme):
    theme_dir = os.path.join(THEMES_DIR, theme)
    if not os.path.isdir(theme_dir):
        print(f"Theme '{theme}' not found in {THEMES_DIR}")
        available = list_themes()
        if available:
            print(f"Available themes: {', '.join(available)}")
        else:
            print(f"No themes found. Create a folder in {THEMES_DIR} with images.")
        sys.exit(2)  # 2 = theme not found
    images = [
        os.path.join(theme_dir, f)
        for f in os.listdir(theme_dir)
        if f.lower().endswith(IMAGE_EXTENSIONS)
    ]
    if not images:
        print(f"No images found in theme '{theme}'")
        sys.exit(3)  # 3 = no images in theme
    images.sort()
    return images


def list_themes():
    if not os.path.isdir(THEMES_DIR):
        return []
    return sorted(
        d for d in os.listdir(THEMES_DIR)
        if os.path.isdir(os.path.join(THEMES_DIR, d)) and not d.startswith(".")
    )


def set_scaling(scaling):
    style, tile = SCALING_MAP.get(scaling, ("10", "0"))
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Control Panel\Desktop",
        0,
        winreg.KEY_SET_VALUE,
    )
    winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, style)
    winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, tile)
    winreg.CloseKey(key)


def set_wallpaper(path, scaling):
    path = os.path.abspath(path)
    set_scaling(scaling)
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )
    if not result:
        print(f"Failed to set wallpaper: {path}")


def main():
    config = load_config()
    general = config["general"]
    minutes = general["minutes"]
    theme = general["theme"]
    shuffle = general["shuffle"]
    scaling = general["scaling"]

    if scaling not in SCALING_MAP:
        print(f"Unknown scaling '{scaling}', defaulting to 'fill'")
        scaling = "fill"

    wallpapers = get_wallpapers(theme)

    print(
        f"wallChange started — theme: {theme}, interval: {minutes}m, "
        f"scaling: {scaling}, images: {len(wallpapers)}, shuffle: {shuffle}"
    )

    if shuffle:
        random.shuffle(wallpapers)

    running = True

    def handle_signal(sig, frame):
        nonlocal running
        print("\nwallChange stopped.")
        running = False

    signal.signal(signal.SIGINT, handle_signal)

    idx = 0
    while running:
        wall = wallpapers[idx % len(wallpapers)]
        set_wallpaper(wall, scaling)
        idx += 1
        if shuffle and idx % len(wallpapers) == 0:
            random.shuffle(wallpapers)
        deadline = time.time() + minutes * 60
        while running and time.time() < deadline:
            time.sleep(min(1.0, deadline - time.time()))


if __name__ == "__main__":
    main()
