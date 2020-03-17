from constraints import position_constraint, size_constraint
from panels import Panel

from blessed_app import BlessedApp

class MyApp(BlessedApp):
    def design(self):
        panel_1 = Panel(position_constraint("relative", .2), position_constraint("centered"),
                        size_constraint("relative", .7), size_constraint("relative", .7), "Panel1",
                        max_w=50, title="Test")
        self.add_element(panel_1)

        panel_2 = Panel(position_constraint("relative", .2), position_constraint("centered"),
                        size_constraint("relative", .25), size_constraint("relative", .7), "Panel2",
                        max_w=40, title="Test")
        panel_1.add_child(panel_2)

        panel_3 = Panel(position_constraint("relative", .6), position_constraint("centered"),
                        size_constraint("relative", .25), size_constraint("relative", .7), "Panel3",
                        max_w=40, title="Test")
        panel_1.add_child(panel_3)

        panel_4 = Panel(position_constraint("absolute", 0), position_constraint("centered"),
                        size_constraint("relative", 1), size_constraint("relative", .7), "Panel4",
                        max_w=25, title="Test")
        panel_3.add_child(panel_4)

    def main(self):
        k = 0

        screen_y = 0
        screen_x = 0
        refresh_flag = False

        while k != 'q':

            if k == 'a':
                self.get_next()
                refresh_flag = True

            old_screen_y = screen_y
            old_screen_x = screen_x
            screen_y, screen_x = self.get_max_yx()

            if screen_y != old_screen_y or screen_x != old_screen_x:
                refresh_flag = True

            # Wait for next input
            k = self.get_input()

            if refresh_flag:
                self.refresh()
                refresh_flag = False

        self.clear()


if __name__ == "__main__":
    app = MyApp()
    app.run()
