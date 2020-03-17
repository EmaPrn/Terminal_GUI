from constraints import position_constraint, size_constraint
from panels import Panel
from radiobutton import RadioButton
from checkbox import Checkbox

from blessed_app import BlessedApp
from time import sleep


class MyApp(BlessedApp):
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

        screen_y = 0
        screen_x = 0

        while k != "q": # ESC_KEY:

            if k == "a":  # KEY_TAB
                self.get_next()
            elif k == "e":
                self.get_active().interact()

            old_screen_y = screen_y
            old_screen_x = screen_x
            screen_y, screen_x = self.get_max_yx()

            # Wait for next input
            k = self.get_input()

            if screen_y != old_screen_y or screen_x != old_screen_x:
                self.render()


        self.clear()


if __name__ == "__main__":
    app = MyApp()
    app.run()
