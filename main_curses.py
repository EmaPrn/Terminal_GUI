from constraints import position_constraint, size_constraint
from panels import Panel
from radiobutton import RadioButton
from checkbox import Checkbox

from curses_app import CursesApp

import curses


class MyApp(CursesApp):
    def design(self):
        panel_1 = Panel(position_constraint("relative", .2), position_constraint("centered"),
                        size_constraint("relative", .7), size_constraint("relative", .7), "Main",
                        max_w=50, title="Main")
        self.add_element(panel_1)

        panel_2 = Panel(position_constraint("absolute", 0), position_constraint("relative", .05),
                        size_constraint("relative", .45), size_constraint("relative", .45), "RadioPan",
                        max_w=40, title="Radio Buttons")
        panel_1.add_child(panel_2)

        radio_1 = RadioButton(position_constraint("absolute", 1), position_constraint("absolute", 0), "rad1", "Radio 1")
        panel_2.add_child(radio_1)

        radio_2 = RadioButton(position_constraint("absolute", 3), position_constraint("absolute", 0), "rad2", "Radio 2")
        panel_2.add_child(radio_2)

        panel_3 = Panel(position_constraint("absolute", 0), position_constraint("relative", .5),
                        size_constraint("relative", .45), size_constraint("relative", .45), "Check Pan",
                        max_w=40, title="Check Boxes")
        panel_1.add_child(panel_3)

        check_1 = Checkbox(position_constraint("absolute", 1), position_constraint("absolute", 0), "chk1", "Check 1")
        panel_3.add_child(check_1)

        check_2 = Checkbox(position_constraint("absolute", 3), position_constraint("absolute", 0), "chk2", "Check 2")
        panel_3.add_child(check_2)


    def main(self):
        k = 0

        self.clear()

        while k != ord("q"): # ESC_KEY:
            while True:
                if k == ord("a"):  # KEY_TAB
                    self.get_next()
                elif k == ord("e"):
                    self.get_active().interact()

                self.render()

                # Wait for next input
                k = self.get_input()

                if k != curses.KEY_RESIZE:
                    break

                self.erase()
                self.set_max_yx()


if __name__ == "__main__":
    app = MyApp()
    app.run()
