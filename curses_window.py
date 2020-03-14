#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Tuple

import curses
from window_manager import IWindow


class CursesWindow(IWindow):
    """ Implements the IWindow interface to wrap the curses methods with APIs to interact with the terminal.

        Attributes:
            screen (curses.window): A curses window where the elements will be drawn. It also provides user inputs.

        Note:
            ideally it should be used in conjunction with curses.wrapper

    """
    def __init__(self, screen: curses.window):
        self.screen: curses.window = screen

        # Perform initialisation on the curses window
        self.screen.erase()
        self.screen.refresh()

    def get_input(self) -> int:
        return self.screen.getch()

    def draw(self, y_pos: int, x_pos: int, text: str, *attr) -> None:
        """Draw a string of text at a given (relative) position.

        Parameters:
            y_pos (int): The relative y position to start drawing the text.
            x_pos (int): The relative x position to start drawing the text.
            text (str): The text to draw.
            *attr: Optional parameters to specify text styles.
        """

        max_y, max_x = self.get_max_yx()
        max_len = max_x - x_pos

        if max_len > 0 and x_pos < max_x and y_pos < max_y:
            if len(text) > max_len:
                text = text[:max_len]

            return self.screen.addstr(y_pos, x_pos, text, *attr)

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

    def refresh(self) -> None:
        return self.screen.refresh()
