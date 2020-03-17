#!/usr/bin/env python
# -*- coding: utf-8 -*-

# allows the definition of interfaces
from abc import abstractmethod
from typing import Tuple

from blessed import Terminal
from _window_manager import IWindow, WindowManager
from gui_elements import TextStyles
from math import log2


class _BlessedWindow(IWindow):
    """ Implements the IWindow interface to wrap the curses methods with APIs to interact with the terminal.

        Attributes:
            screen (curses.window): A curses window where the elements will be drawn. It also provides user inputs.

        Note:
            ideally it should be used in conjunction with curses.wrapper

    """
    def __init__(self):
        self.screen = Terminal()

    def get_input(self) -> int:
        with self.screen.cbreak():
            return self.screen.inkey(timeout=1./25)

    def draw(self, y_pos: int, x_pos: int, text: str, attr=0) -> None:
        """Draw a string of text at a given (relative) position.

        Parameters:
            y_pos (int): The relative y position to start drawing the text.
            x_pos (int): The relative x position to start drawing the text.
            text (str): The text to draw.
            attr: Optional parameters to specify text styles.
        """

        max_y, max_x = self.get_max_yx()
        max_len = max_x - x_pos

        print(self.screen.normal)

        # A bitmask is used to set multiple concurrent text styles:
        if (attr & TextStyles.HIGHLIGHTED) >> int(log2(TextStyles.HIGHLIGHTED)):
            text = self.screen.reverse(text)
        if (attr & TextStyles.UNDERLINE) >> int(log2(TextStyles.UNDERLINE)):
            text = self.screen.underline(text)
        if (attr & TextStyles.BOLD) >> int(log2(TextStyles.BOLD)):
            text = self.screen.bold(text)
        if (attr & TextStyles.RED) >> int(log2(TextStyles.RED)):
            text = self.screen.red(text)
        if (attr & TextStyles.GREEN) >> int(log2(TextStyles.GREEN)):
            text = self.screen.green(text)
        if (attr & TextStyles.YELLOW) >> int(log2(TextStyles.YELLOW)):
            text = self.screen.yellow(text)
        if (attr & TextStyles.BLUE) >> int(log2(TextStyles.BLUE)):
            text = self.screen.blue(text)
        if (attr & TextStyles.MAGENTA) >> int(log2(TextStyles.MAGENTA)):
            text = self.screen.magenta(text)
        if (attr & TextStyles.CYAN) >> int(log2(TextStyles.CYAN)):
            text = self.screen.cyan(text)

        if max_len > 0 and x_pos < max_x and y_pos < max_y:
            if len(text) > max_len:
                text = text[:max_len]

            with self.screen.location(x_pos, y_pos):
                print(text)

    def draw_rectangle(self, uly: int, ulx: int, lry: int, lrx: int) -> None:
        """Draw a rectangle with corners at the provided upper-left and lower-right coordinates.

        Parameters:
            uly: y position of the Upper-Left corner of the rectangle
            ulx: x position of the Upper-Left corner of the rectangle
            lry: y position of the Lower-Right corner of the rectangle
            lrx: x position of the Lower-Right corner of the rectangle

        """
        border_bl = u'└'
        border_br = u'┘'
        border_tl = u'┌'
        border_tr = u'┐'
        border_h = u'─'
        border_v = u'│'

        if uly != lry and ulx != lrx:
            with self.screen.location(ulx, uly):
                print(border_tl + border_h * (lrx - ulx - 1) + border_tr)
            with self.screen.location(ulx, lry):
                print(border_bl + border_h * (lrx - ulx - 1) + border_br)

            for n in range(lry - uly - 1):
                with self.screen.location(ulx, uly + 1 + n):
                    print(border_v)

            for n in range(lry - uly - 1):
                with self.screen.location(lrx, uly + 1 + n):
                    print(border_v)

    def get_max_yx(self) -> Tuple[int, int]:
        return self.screen.height, self.screen.width

    def delete(self, y_pos: int, x_pos: int) -> None:
        self.draw(y_pos, x_pos, " ")

    def clear(self) -> None:
        print(self.screen.clear())

    def erase(self) -> None:
        print(self.screen.clear())


class BlessedApp(WindowManager):
    def __init__(self):
        super().__init__()
        self.window: _BlessedWindow = _BlessedWindow()

    @abstractmethod
    def design(self):
        pass

    @abstractmethod
    def main(self):
        pass

    def run(self):
        self.design()
        self.reset_active()
        with self.window.screen.hidden_cursor():
            with self.window.screen.fullscreen():
                self.main()

