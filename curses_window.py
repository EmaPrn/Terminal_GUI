#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
from window_manager import Window


class CursesWindow(Window):
    def __init__(self, screen):
        self.screen = screen
        self.screen.clear()
        self.screen.refresh()

    def get_input(self):
        return self.screen.getch()

    def draw(self, y_pos, x_pos, text, *attr):
        max_y, max_x = self.get_max_yx()
        max_len = max_x - x_pos

        if max_len > 0 and x_pos < max_x and y_pos < max_y:
            if len(text) > max_len:
                text = text[:max_len]

            return self.screen.addstr(y_pos, x_pos, text, *attr)

    def draw_rectangle(self, uly, ulx, lry, lrx):
        """Draw a rectangle with corners at the provided upper-left
        and lower-right coordinates.
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

    def get_max_yx(self):
        return self.screen.getmaxyx()

    def delete(self, y_pos, x_pos):
        return self.screen.delch(y_pos, x_pos)

    def clear(self):
        return self.screen.clear()

    def erase(self):
        return self.screen.erase()

    def refresh(self):
        return self.screen.refresh()