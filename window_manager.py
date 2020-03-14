#!/usr/bin/env python
# -*- coding: utf-8 -*-

from panels import Panel, PanelManager
from abc import abstractmethod
from gui_interfaces import Canvas


class Window(Canvas):
    @abstractmethod
    def get_input(self):
        pass

    @abstractmethod
    def delete(self, y_pos: int, x_pos: int):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def erase(self):
        pass

    @abstractmethod
    def refresh(self):
        pass


class WindowManager(object):
    class _WindowManager:
        def __init__(self, window):
            self.window = window
            self.panel_manager = PanelManager(window)

        def get_input(self):
            return self.window.get_input()

        def draw(self, y_pos, x_pos, text, *attr):
            self.window.draw(y_pos, x_pos, text, *attr)

        def draw_rectangle(self, uly, ulx, lry, lrx):
            self.window.draw_rectangle(uly, ulx, lry, lrx)

        def get_max_yx(self):
            return self.window.get_max_yx()

        def delete(self, y_pos, x_pos):
            self.window.delete(y_pos, x_pos)

        def clear(self):
            self.window.clear()

        def erase(self):
            self.window.erase()

        def refresh(self):
            self.window.refresh()

        def display(self):
            self.erase()
            for child in self.panel_manager.get_elements():
                child.display()
            self.refresh()

        def add_panel(self, child: Panel):
            self.panel_manager.add_child(child)

        def get_next(self):
            return self.panel_manager.get_next()

    instance = None

    def __init__(self, arg):
        if not WindowManager.instance:
            WindowManager.instance = self._WindowManager(arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)
