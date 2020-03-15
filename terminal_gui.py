#!/usr/bin/env python
# -*- coding: utf-8 -*-
# imports used for type hints
from typing import Tuple

# allows the definition of interfaces
from abc import abstractmethod

import curses
from window_manager import WindowManager
from curses_window import CursesWindow


class TerminalApp(WindowManager):
    """

    """

    @abstractmethod
    def design(self):
        pass

    @abstractmethod
    def main(self):
        pass

    def run(self):

        def set_screen(screen):
            self.window = CursesWindow(screen)
            self.design()
            self.main()

        curses.wrapper(set_screen)
