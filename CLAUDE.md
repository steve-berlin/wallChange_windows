# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Windows port of [wallChange](https://github.com/steve-berlin/wallChange) — an automatic wallpaper rotator. Single-script Python app, zero pip dependencies (stdlib only, requires Python 3.11+ for `tomllib`).

## Running

```
python wallchange.py
```

Requires `themes/<theme_name>/` with images and optionally a `wallrc.toml` (copy from `wallrc.example.toml`).

## Architecture

Single file (`wallchange.py`) with this flow:
1. Load TOML config (defaults if missing)
2. Discover images in `themes/<theme>/`
3. Loop: set wallpaper via Win32 API, sleep for interval, repeat

Wallpaper is set through `ctypes.windll.user32.SystemParametersInfoW`. Scaling modes (fill/fit/stretch/center/tile/span) are applied by writing `WallpaperStyle` and `TileWallpaper` to the registry via `winreg`.

## Exit codes

- 0: Normal exit (Ctrl+C)
- 1: Missing dependency (Python 3.11+)
- 2: Theme directory not found
- 3: No images in theme

## Auto-start

`install.bat` creates a Windows Task Scheduler entry. `install.bat uninstall` removes it.

## Key constraints

- Windows-only (`ctypes.windll`, `winreg`)
- No `.webp` support (Windows wallpaper API doesn't handle it natively)
- `wallrc.toml` and `themes/` are gitignored — user-local config
