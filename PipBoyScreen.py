import hardware
from game_loop import run
from state import create_initial_state
from ui import create_ui_context


def main():
    ui = create_ui_context()
    app_state = create_initial_state()
    hardware.setup()
    try:
        run(ui, app_state)
    finally:
        hardware.cleanup()


if __name__ == "__main__":
    main()
