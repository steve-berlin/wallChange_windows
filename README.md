# wallChange for Windows

Automatic wallpaper rotator for Windows. Cycles through themed wallpaper collections at a configurable interval.

Windows port of [wallChange](https://github.com/steve-berlin/wallChange).

## Requirements

- Python 3.11+
- Windows 10/11

## Setup

1. Create a `themes/` folder and add a subfolder (e.g. `themes/default/`) with your wallpapers (`.jpg`, `.jpeg`, `.png`, `.bmp`).

2. Copy `wallrc.example.toml` to `wallrc.toml` and edit to taste:

```toml
[general]
minutes = 0.25       # Time each wallpaper is displayed
theme = "default"    # Theme folder name
shuffle = false      # Randomize order
scaling = "fill"     # fill, fit, stretch, center, tile, or span
```

3. Run it:

```
python wallchange.py
```

## Auto-start on login

```
install.bat
```

This creates a Windows Task Scheduler entry that runs wallChange at logon.

To remove:

```
install.bat uninstall
```

## Scaling modes

| Mode | Description |
|------|-------------|
| `fill` | Fill screen, may crop |
| `fit` | Fit inside screen, may letterbox |
| `stretch` | Stretch to fill (ignores aspect ratio) |
| `center` | Center at original size |
| `tile` | Tile the image |
| `span` | Span across multiple monitors |
