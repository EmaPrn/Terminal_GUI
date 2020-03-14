from constraints import RelativePosition, CenteredPosition, RelativeSize, AbsoluteSize
from panels import Panel
from window_manager import WindowManager
from curses_window import CursesWindow
import curses


def draw_menu(stdscr):
    # Clear and refresh the screen for a blank canvas
    manager = WindowManager(CursesWindow(stdscr))
    manager.clear()
    manager.refresh()

    panel_1 = Panel(RelativePosition(0.2), CenteredPosition(), RelativeSize(.4), AbsoluteSize(30), "Panel1", "Test")

    manager.add_element(panel_1)

    panel_2 = Panel(RelativePosition(.2), CenteredPosition(), RelativeSize(.25), AbsoluteSize(10), "Panel2", "Test")

    panel_1.add_child(panel_2)

    panel_3 = Panel(RelativePosition(.6), CenteredPosition(), RelativeSize(.25), AbsoluteSize(10), "Panel3", "Test")

    panel_1.add_child(panel_3)

    k = 0

    screen_y = 0
    screen_x = 0

    manager.get_next()

    while k != ord('q'):

        if k == ord('a'):
            manager.get_next()
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
