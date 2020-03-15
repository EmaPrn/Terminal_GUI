#!/usr/bin/env python
# -*- coding: utf-8 -*-

# allows the definition of interfaces
from abc import abstractmethod

import curses
from _window_manager import WindowManager
from _curses_window import CursesWindow


class CursesApp(WindowManager):

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
            self.reset_active()
            self.main()

        curses.wrapper(set_screen)
