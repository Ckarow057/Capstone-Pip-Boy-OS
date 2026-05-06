# Capstone-Pip-Boy-OS

This project is a Fallout-style Pip-Boy interface built with pygame for a Raspberry Pi wearable computer capstone. It works in two modes:

- desktop simulation (keyboard only)
- Raspberry Pi build (physical buttons + rotary encoder)

The goal was to make something that feels close to the in-game Pip-Boy UI while still being practical to run and test during development.

## What It Does

When you launch the app, it opens full-screen and renders a themed Pip-Boy interface with CRT-style effects (scanlines, flicker, occasional glitch pulse), tab navigation, and optional GPIO input.

Implemented screens:

- `STAT`: player vitals, S.P.E.C.I.A.L. attributes, and body-part condition bars
- `ITEMS`: inventory table with weights, values, quantities, and total carry weight
- `DATA`: quest log with statuses, descriptions, and objective checklist
- `MAP`: world map image with blinking player position marker
- `RADIO`: station browser with signal strength, status, and animated waveform effects

Other built-in behavior:

- full-screen 1200x800 pygame display
- scanlines, flicker, and glitch-style visual effects
- multiple color themes loaded from `pip_boy_data.json`
- keyboard fallback controls for non-Raspberry Pi development
- optional Raspberry Pi GPIO input support that safely disables itself when `RPi.GPIO` is unavailable

## Requirements

- Python 3.10 or newer
- `pygame`
- Optional on Raspberry Pi: `RPi.GPIO`

The project reads all demo content from `pip_boy_data.json` and loads image assets from the `images/` directory.

## Setup

### 1. Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install pygame
```

If you are running on a Raspberry Pi and need physical GPIO input, install `RPi.GPIO` in the same environment.

## Run The App

From the project root:

```bash
python PipBoyScreen.py
```

Startup behavior:

- the app opens in full-screen mode
- the mouse cursor is hidden
- the initial screen is `STAT`
- theme data, player data, inventory, quests, map data, and radio data are loaded from `pip_boy_data.json`

To exit the program, press `Esc` or close the pygame window.

## Controls

### Keyboard controls

- `1`: open `STAT`
- `2`: open `ITEMS`
- `3`: open the `DATA` group and cycle `DATA -> MAP -> RADIO`
- `4`: open `MAP`
- `5`: open `RADIO`
- `Left Arrow` / `Right Arrow`: cycle through all screens
- `Up Arrow` / `Down Arrow`: move the selection on scrollable screens
- `X`: cycle to the next color theme
- `Esc`: quit

### Raspberry Pi hardware controls

If GPIO is available, the program listens for hardware events and mirrors the keyboard navigation with physical controls.

- Button 1 on GPIO `17`: open `STAT`
- Button 2 on GPIO `22`: open `ITEMS`
- Button 3 on GPIO `27`: cycle `DATA -> MAP -> RADIO`
- Rotary encoder CLK on GPIO `13`: scroll
- Rotary encoder DT on GPIO `19`: determines scroll direction
- Rotary encoder switch on GPIO `26`: cycle theme

Debounce timings are configured in `config.py`.

## Screen Breakdown

### STAT

- top-bar summary of level, HP, AP, XP, and radiation
- S.P.E.C.I.A.L. attributes shown with 10-step stat bars
- Vault Boy image rendered in the active color theme
- body condition percentages for head, torso, arms, and legs

### ITEMS

- category sidebar styled after the Pip-Boy inventory layout
- tabular inventory listing with name, weight, value, and quantity
- footer showing total carried weight and current caps

### DATA

- selectable quest list
- quest status highlighting for active, completed, and failed entries
- description panel and checklist-style objective display

### MAP

- theme-tinted map image
- blinking player marker using normalized coordinates from the JSON data

### RADIO

- station cards with frequency, status, DJ, and signal percentage
- active-station highlighting
- animated waveform effect for stations that are on air
- footer showing the currently tuned station

## Testing

Run all unit tests with:

```bash
python -m unittest tests/test_hardware.py tests/test_game_loop.py tests/test_state_data.py -v
```

Or run them individually:

```bash
python -m unittest tests/test_hardware.py -v
python -m unittest tests/test_game_loop.py -v
python -m unittest tests/test_state_data.py -v
```

Test coverage includes:

- `tests/test_hardware.py`: GPIO callbacks and event posting behavior (mocked)
- `tests/test_game_loop.py`: non-hardware input handling, screen cycling, and theme/selection logic
- `tests/test_state_data.py`: animation state updates, initial app-state wiring, and JSON data-loader caching behavior

All tests use mocks/stubs where needed, so they can run on a non-Pi machine.

If you only want fast feedback while working on core logic, run:

```bash
python -m unittest tests/test_game_loop.py tests/test_state_data.py -v
```

## Project Structure

- `PipBoyScreen.py`: application entry point
- `game_loop.py`: event processing, screen switching, and render loop
- `graphics.py`: shared drawing code, overlays, and screen dispatch
- `ui.py`: pygame initialization, fonts, display, and frame timing
- `state.py`: application state and animation state setup
- `data_loader.py`: cached loading helpers for `pip_boy_data.json`
- `hardware.py`: Raspberry Pi GPIO integration and pygame hardware events
- `theme.py`: active palette application
- `config.py`: window settings, asset paths, GPIO pins, and constants
- `screens/`: per-screen rendering modules for `STAT`, `ITEMS`, `DATA`, `MAP`, and `RADIO`
- `tests/test_hardware.py`: GPIO and event posting unit tests
- `tests/test_game_loop.py`: non-hardware game loop and input behavior tests
- `tests/test_state_data.py`: app state, animation, and data loader tests

## Troubleshooting

- If the app opens in full-screen and appears stuck, press `Esc` to exit.
- If you are not on a Raspberry Pi, missing `RPi.GPIO` is expected; the hardware layer will simply no-op.
- If image loading fails, confirm that `images/vault-boy.png` and `images/map.jpg` exist.
- If the window does not start, verify that `pygame` is installed in the active virtual environment.

## Notes

- This project is data-driven: most on-screen content comes from `pip_boy_data.json`.
- Themes are loaded from the same JSON file, and can be cycled in real time with `X` (or encoder press on Pi).
- Hardware support is optional during development, so you can build and test on a normal laptop first.
