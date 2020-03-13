from constraints import RelativePosition, CenteredPosition, RelativeSize, AbsoluteSize
from panels import WindowManager, Panel
import curses


def draw_menu(stdscr):
    # Clear and refresh the screen for a blank canvas
    manager = WindowManager(stdscr)
    manager.clear()
    manager.refresh()

    panel_1 = Panel(manager, RelativePosition(0.2), CenteredPosition(), RelativeSize(.4), AbsoluteSize(30), "Test")

    manager.add_child(panel_1)

    panel_2 = Panel(panel_1, RelativePosition(.2), CenteredPosition(), RelativeSize(.25), AbsoluteSize(10), "Test")

    panel_1.add_child(panel_2)

    panel_3 = Panel(panel_1, RelativePosition(.6), CenteredPosition(), RelativeSize(.25), AbsoluteSize(10), "Test")

    panel_1.add_child(panel_3)

    k = 0

    screen_y = 0
    screen_x = 0

    manager.activate_next()

    while k != ord('q'):

        if k == ord('a'):
            manager.activate_next()
            manager.display()

        old_screen_y = screen_y
        old_screen_x = screen_x
        screen_y, screen_x = manager.get_max_yx()

        if screen_y != old_screen_y or screen_x != old_screen_x:
            manager.display()

        # Wait for next input
        k = manager.get_input()


def main():
    curses.wrapper(draw_menu)


if __name__ == "__main__":
    main()
