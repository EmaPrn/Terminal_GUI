#!/usr/bin/env python
# -*- coding: utf-8 -*-
# imports used for type hints
from typing import Tuple

# allows the definition of interfaces
from abc import abstractmethod

from gui_elements import ICanvas, GuiElement, ElementTreeManager


class IWindow(ICanvas):
    """This interface describes a low level canvas. It is intended to wrap low level functionality and expose them
        though the interface method.
    """
    @abstractmethod
    def get_input(self) -> int:
        pass

    @abstractmethod
    def delete(self, y_pos: int, x_pos: int) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def erase(self) -> None:
        pass

    @abstractmethod
    def refresh(self) -> None:
        pass


class WindowManager(object):
    """Manages the low level API for rendering the elements displayed on the window an catch user interaction.
       It takes care of exposing the current active element and provides methods to activate a new one.

       Note:
           Be careful, it is implemented as a singleton! Only one instance of WindowManager can exist at a given time.

       Parameters:
           window (Window): The window object wrapping the low level APIs.

    """
    class _WindowManager:
        #   TODO: Implement tabs trough a cyclic list of PanelManagers.
        #   TODO: Implement popup panels trough a stack.

        def __init__(self, window: IWindow):
            self.window: IWindow = window
            self._element_tree_manager: ElementTreeManager = ElementTreeManager(window)

        def get_input(self) -> int:
            return self.window.get_input()

        def get_max_yx(self) -> Tuple[int, int]:
            return self.window.get_max_yx()

        def delete(self, y_pos: int, x_pos: int) -> None:
            self.window.delete(y_pos, x_pos)

        def clear(self) -> None:
            self.window.clear()

        def erase(self) -> None:
            self.window.erase()

        def refresh(self) -> None:
            self.window.refresh()

        def display(self) -> None:
            self.erase()
            for child in self._element_tree_manager.get_elements():
                child.render()
            self.refresh()

        def add_element(self, child: GuiElement) -> None:
            self._element_tree_manager.add_element(child)

        def get_next(self) -> GuiElement:
            return self._element_tree_manager.get_next()

        def get_active(self) -> GuiElement:
            return self._element_tree_manager.get_active()

    instance: _WindowManager = None

    def __init__(self, window):
        if not WindowManager.instance:
            WindowManager.instance = self._WindowManager(window)

    def __getattr__(self, name):
        return getattr(self.instance, name)
