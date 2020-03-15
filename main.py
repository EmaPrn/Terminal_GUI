from constraints import RelativePosition, CenteredPosition, RelativeSize, AbsoluteSize
from panels import Panel

from terminal_gui import TerminalApp


class MyApp(TerminalApp):
    def design(self):
        panel_1 = Panel(RelativePosition(0.2), CenteredPosition(), RelativeSize(.4), AbsoluteSize(30), "Panel1", "Test")
        self.add_element(panel_1)
        panel_2 = Panel(RelativePosition(.2), CenteredPosition(), RelativeSize(.25), AbsoluteSize(10), "Panel2", "Test")
        panel_1.add_child(panel_2)
        panel_3 = Panel(RelativePosition(.6), CenteredPosition(), RelativeSize(.25), AbsoluteSize(10), "Panel3", "Test")
        panel_1.add_child(panel_3)

    def main(self):
        self.clear()
        self.refresh()

        k = 0

        screen_y = 0
        screen_x = 0

        self.get_next()

        while k != ord('q'):

            if k == ord('a'):
                self.get_next()
                self.display()

            old_screen_y = screen_y
            old_screen_x = screen_x
            screen_y, screen_x = self.get_max_yx()

            if screen_y != old_screen_y or screen_x != old_screen_x:
                self.display()

            # Wait for next input
            k = self.get_input()


if __name__ == "__main__":
    app = MyApp()
    app.run()
