from constraints import position_constraint, size_constraint
from panels import Panel

from curses_app import CursesApp


class MyApp(CursesApp):
    def design(self):
        panel_1 = Panel(position_constraint("relative", .2), position_constraint("centered"),
                        size_constraint("relative", .7), size_constraint("absolute", 30), "Panel1", "Test")
        self.add_element(panel_1)

        panel_2 = Panel(position_constraint("relative", .2), position_constraint("centered"),
                        size_constraint("relative", .25), size_constraint("absolute", 10), "Panel2", "Test")
        panel_1.add_child(panel_2)

        panel_3 = Panel(position_constraint("relative", .6), position_constraint("centered"),
                        size_constraint("relative", .25), size_constraint("absolute", 10), "Panel3", "Test")
        panel_1.add_child(panel_3)

        panel_4 = Panel(position_constraint("absolute", 0), position_constraint("centered"),
                        size_constraint("relative", 1), size_constraint("relative", 1.), "Panel4", "Test")
        panel_3.add_child(panel_4)

    def main(self):
        k = 0

        screen_y = 0
        screen_x = 0

        while k != ord('q'):

            if k == ord('a'):
                self.get_next()

            old_screen_y = screen_y
            old_screen_x = screen_x
            screen_y, screen_x = self.get_max_yx()

            if screen_y != old_screen_y or screen_x != old_screen_x:
                self.render()

            # Wait for next input
            k = self.get_input()


if __name__ == "__main__":
    app = MyApp()
    app.run()
