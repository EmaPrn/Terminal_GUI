#!/usr/bin/env python
# -*- coding: utf-8 -*-
# imports used for type hints
from typing import Tuple, Union

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

    """

    #   TODO: Implement tabs through a cyclic list of PanelManagers.
    #   TODO: Implement popup panels through a stack.

    def __init__(self):
        self._window: Union[None, IWindow] = None
        self._element_tree_manager: Union[None, ElementTreeManager] = None

    @property
    def window(self) -> IWindow:
        return self._window

    @window.setter
    def window(self, window: IWindow):
        self._window: IWindow = window
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

    def render(self) -> None:
        self.erase()
        for child in self._element_tree_manager.get_elements():
            child.render()
        self.refresh()

    def add_element(self, child: GuiElement) -> None:
        self._element_tree_manager.add_element(child)

    def get_next(self) -> GuiElement:
        old = self._element_tree_manager.get_active()
        new = self._element_tree_manager.activate_next()
        old.render()
        new.render()
        return new

    def get_active(self) -> GuiElement:
        return self._element_tree_manager.get_active()

    def reset_active(self) -> GuiElement:
        old = self._element_tree_manager.get_active()
        new = self._element_tree_manager.reset_active()
        if isinstance(old, GuiElement):
            old.render()
        if isinstance(old, GuiElement):
            new.render()
        return new
