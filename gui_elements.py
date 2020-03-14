#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Tuple
from abc import ABC, abstractmethod
from tree import Node
from canvas import ICanvas


class CannotDrawError(Exception):
    """Error to throw when a constraint cannot be satisfied."""
    pass


class IConstraint(ABC):
    """Interface to the constraints that can be imposed to a GUI Element."""
    pass


class IPositionConstraint(IConstraint):
    """Interface to the constraints that can be imposed to the position of GUI Element."""
    @abstractmethod
    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int) -> int:
        """Called when trying to impose the position constraint.

        Parameters:
            direction (str): Either "x" or "y".
            h (int): The height of the caller. Used to impose top, bottom or centered alignments.
            w (int): The width of the caller. Used to impose left, right or centered alignments.
            max_y: Bounding y value (I.e. the y size of its parent container).
            max_x: Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed position if possible, raise CannotDrawError otherwise.
        """
        pass


class ISizeConstraint(IConstraint):
    @abstractmethod
    def impose(self, direction: str, max_y: int, max_x: int):
        """Called when trying to impose the size constraint.

        Parameters:
            direction (str): Either "x" or "y".
            max_y: Bounding y value (I.e. the y size of its parent container).
            max_x: Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed size if possible, raise CannotDrawError otherwise.
        """
        pass


class GuiElement(ICanvas):
    """Generic Element that can be drawn on the screen.
        Implements the ICanvas interface as it is possible to draw other elements on top of it.

        Attributes:
            title (str): The name of the element. Can be shown after rendering.
            element_id (str): The unique identifier of the element.
            y_constraint (IPositionConstraint): Constraint for the y position of the element.
            x_constraint (IPositionConstraint): Constraint for the x position of the element.
            h_constraint (ISizeConstraint): Constraint for the height of the element.
            w_constraint (ISizeConstraint): Constraint for the width of the element.
            is_active (bool): Internal state of the element. Useful to allow actions on it.
                              Can modify the appearance on screen of the element.
    """
    def __init__(self, y_constraint: IPositionConstraint, x_constraint: IPositionConstraint,
                 h_constraint: ISizeConstraint, w_constraint: ISizeConstraint, element_id: str, title: str = ''):

        self.title: str = title

        # Each element is associated to a node.
        # It allows to invoke its parent drawing functions up to the window render itself.
        self._node: Node = Node(element_id, self)

        self._x_constraint: IPositionConstraint = x_constraint
        self._y_constraint: IPositionConstraint = y_constraint
        self._w_constraint: ISizeConstraint = w_constraint
        self._h_constraint: ISizeConstraint = h_constraint

        self.is_active: bool = False

    # The use of @property allows to hide the existence of the node.
    @property
    def parent(self) -> GuiElement:
        return self._node.parent.payload

    # The node should be not modified, it lives together with the GUI element.
    @property
    def node(self) -> Node:
        return self._node

    # x position, y position, width and height can be obtained through properties.
    # Each time that the property is called the corresponding constraint is imposed and the calculated result returned.

    @property
    def x(self) -> int:
        max_y, max_x = self.parent.get_max_yx()
        return self._x_constraint.impose('x', self.h, self.w, max_y, max_x)

    @property
    def y(self) -> int:
        max_y, max_x = self.parent.get_max_yx()
        return self._y_constraint.impose('y', self.h, self.w, max_y, max_x)

    @property
    def w(self) -> int:
        max_y, max_x = self.parent.get_max_yx()
        return self._w_constraint.impose('x', max_y, max_x)

    @property
    def h(self) -> int:
        max_y, max_x = self.parent.get_max_yx()
        return self._h_constraint.impose('y', max_y, max_x)

    def get_max_yx(self) -> Tuple[int, int]:
        """Implements the method of the ICanvas interface.

        Returns:
            The size of the object as boundaries for its children.
        """
        return self.h, self.w

    def draw(self, y_pos: int, x_pos: int, text: str, *args) -> None:
        """Implements the method of the ICanvas interface."""
        x = x_pos + self.x
        y = y_pos + self.y
        max_size = self.get_max_yx()[1] - x_pos

        if len(text) > max_size:
            text = text[:max_size]

        self.parent.draw(y, x, text, *args)

    def draw_rectangle(self, uly: int, ulx: int, lry: int, lrx: int) -> None:
        """Implements the method of the ICanvas interface."""
        self.parent.draw_rectangle(uly + self.y, ulx + self.x, lry + self.y, lrx + self.x)

    @abstractmethod
    def render(self) -> None:
        """Render the given GUI element.
            It should use the draw method."""
        pass
