#!/usr/bin/env python
# -*- coding: utf-8 -*-

# allows the definition of interfaces
from abc import abstractmethod
from typing import Tuple

import curses
from _window_manager import IWindow, WindowManager
from gui_elements import TextStyles
from math import log2


class _CursesWindow(IWindow):
    """ Implements the IWindow interface to wrap the curses methods with APIs to interact with the terminal.

        Attributes:
            screen (curses.window): A curses window where the elements will be drawn. It also provides user inputs.

        Note:
            ideally it should be used in conjunction with curses.wrapper

    """
    def __init__(self, screen):
        self.screen = screen

        # Perform initialisation on the curses window
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def get_input(self) -> int:
        return self.screen.getch()

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

        if max_len > 0 and x_pos < max_x and y_pos < max_y:
            if len(text) > max_len:
                text = text[:max_len]

            # A bitmask is used to set multiple concurrent text styles:
            mask = 0
            if (attr & TextStyles.HIGHLIGHTED) >> int(log2(TextStyles.HIGHLIGHTED)):
                mask = mask | curses.A_STANDOUT
            if (attr & TextStyles.UNDERLINE) >> int(log2(TextStyles.UNDERLINE)):
                mask = mask | curses.A_UNDERLINE
            if (attr & TextStyles.BOLD) >> int(log2(TextStyles.BOLD)):
                mask = mask | curses.A_BOLD
            if (attr & TextStyles.RED) >> int(log2(TextStyles.RED)):
                mask = mask | curses.color_pair(1)
            if (attr & TextStyles.GREEN) >> int(log2(TextStyles.GREEN)):
                mask = mask | curses.color_pair(2)
            if (attr & TextStyles.YELLOW) >> int(log2(TextStyles.YELLOW)):
                mask = mask | curses.color_pair(3)
            if (attr & TextStyles.BLUE) >> int(log2(TextStyles.BLUE)):
                mask = mask | curses.color_pair(4)
            if (attr & TextStyles.MAGENTA) >> int(log2(TextStyles.MAGENTA)):
                mask = mask | curses.color_pair(5)
            if (attr & TextStyles.CYAN) >> int(log2(TextStyles.CYAN)):
                mask = mask | curses.color_pair(6)

            return self.screen.addstr(y_pos, x_pos, text, mask)

    def draw_rectangle(self, uly: int, ulx: int, lry: int, lrx: int) -> None:
        """Draw a rectangle with corners at the provided upper-left and lower-right coordinates.

        Parameters:
            uly: y position of the Upper-Left corner of the rectangle
            ulx: x position of the Upper-Left corner of the rectangle
            lry: y position of the Lower-Right corner of the rectangle
            lrx: x position of the Lower-Right corner of the rectangle

        """
        if uly != lry and ulx != lrx:
            self.screen.vline(uly + 1, ulx, curses.ACS_VLINE, lry - uly - 1)
            self.screen.hline(uly, ulx + 1, curses.ACS_HLINE, lrx - ulx - 1)
            self.screen.hline(lry, ulx + 1, curses.ACS_HLINE, lrx - ulx - 1)
            self.screen.vline(uly + 1, lrx, curses.ACS_VLINE, lry - uly - 1)
            self.screen.addch(uly, ulx, curses.ACS_ULCORNER)
            self.screen.addch(uly, lrx, curses.ACS_URCORNER)
            self.screen.addch(lry, lrx, curses.ACS_LRCORNER)
            self.screen.addch(lry, ulx, curses.ACS_LLCORNER)

    def get_max_yx(self) -> Tuple[int, int]:
        return self.screen.getmaxyx()

    def delete(self, y_pos: int, x_pos: int) -> None:
        return self.screen.delch(y_pos, x_pos)

    def clear(self) -> None:
        return self.screen.clear()

    def erase(self) -> None:
        return self.screen.erase()


class CursesApp(WindowManager):

    @abstractmethod
    def design(self):
        pass

    @abstractmethod
    def main(self):
        pass

    def run(self):

        def set_screen(screen):
            self.window = _CursesWindow(screen)
            self.design()
            self.reset_active()
            self.main()

        curses.wrapper(set_screen)
