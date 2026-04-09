# Capstone-Pip-Boy-OS
The Operating system for a Raspberry Pi wrist mounted computer, inspired by the Fallout video game series.   

## Project Structure
- `PipBoyScreen.py`: app entrypoint
- `data_loader.py`: game/player data loading helpers
- `state.py`: animation and app state models
- `graphics.py`: all drawing/rendering functions
- `game_loop.py`: input handling and update/render loop
- `ui.py`: pygame setup and UI context creation
- `config.py`: window and color constants

## Testing Command
python -m unittest tests/test_hardware.py -v