#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Tuple
from abc import ABC, abstractmethod
from tree import Node
from canvas import ICanvas


class CannotDrawError(Exception):
    """
    Error to throw when a constraint cannot be satisfied
    """
    pass


class IConstraint(ABC):
    pass


class IPositionConstraint(IConstraint):
    @abstractmethod
    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int):
        pass


class ISizeConstraint(IConstraint):
    @abstractmethod
    def impose(self, direction: str, max_y: int, max_x: int):
        pass


class GuiElement(ICanvas):
    def __init__(self, y_constraint: IPositionConstraint, x_constraint: IPositionConstraint,
                 h_constraint: ISizeConstraint, w_constraint: ISizeConstraint, title: str = ''):

        self.title: str = title
        self._node: Node = Node(title, self)

        self._x_constraint: IPositionConstraint = x_constraint
        self._y_constraint: IPositionConstraint = y_constraint
        self._w_constraint: ISizeConstraint = w_constraint
        self._h_constraint: ISizeConstraint = h_constraint

        self.is_active: bool = False

    @property
    def parent(self) -> GuiElement:
        return self.node.parent.payload

    @property
    def node(self) -> Node:
        return self._node

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
        return self.h, self.w

    def draw(self, y_pos: int, x_pos: int, text: str, *args) -> None:
        x = x_pos + self.x
        y = y_pos + self.y
        max_size = self.get_max_yx()[1] - x_pos

        if len(text) > max_size:
            text = text[:max_size]

        self.parent.draw(y, x, text, *args)

    def draw_rectangle(self, uly: int, ulx: int, lry: int, lrx: int) -> None:
        """
        Draw a rectangle with corners at the provided upper-left
        and lower-right coordinates.
        """
        self.parent.draw_rectangle(uly + self.y, ulx + self.x, lry + self.y, lrx + self.x)

    @abstractmethod
    def display(self) -> None:
        pass
