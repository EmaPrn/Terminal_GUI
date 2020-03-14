#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Tuple
from abc import ABC, abstractmethod
from tree import Tree, Node
from gui_interfaces import NodeDrawable, Canvas


class CannotDrawError(Exception):
    """
    Error to throw when a constraint cannot be satisfied
    """
    pass


class Constraint(ABC):
    pass


class PositionConstraint(Constraint):
    @abstractmethod
    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int):
        pass


class SizeConstraint(Constraint):
    @abstractmethod
    def impose(self, direction: str, max_y: int, max_x: int):
        pass


class Panel(NodeDrawable):
    def __init__(self, y_constraint: PositionConstraint, x_constraint: PositionConstraint,
                 h_constraint: SizeConstraint, w_constraint: SizeConstraint, title: str = '', has_borders: bool = True):

        self.title: str = title
        self._node: Node = Node(title, self)

        self._x_constraint: PositionConstraint = x_constraint
        self._y_constraint: PositionConstraint = y_constraint
        self._w_constraint: SizeConstraint = w_constraint
        self._h_constraint: SizeConstraint = h_constraint

        self.has_borders: bool = has_borders

        self.is_active: bool = False

    @property
    def parent(self) -> NodeDrawable:
        return self.node.parent.payload

    @property
    def children(self) -> List[NodeDrawable]:
        return [child.payload for child in self.node]

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

    def display(self) -> None:
        try:
            if self.has_borders:
                self.draw_borders()
            self.draw_children()
        except CannotDrawError:
            pass

    def draw_rectangle(self, uly: int, ulx: int, lry: int, lrx: int) -> None:
        """
        Draw a rectangle with corners at the provided upper-left
        and lower-right coordinates.
        """
        self.parent.draw_rectangle(uly + self.y, ulx + self.x, lry + self.y, lrx + self.x)

    def draw_borders(self) -> None:
        if self.is_active:
            title = "A: " + self.title
        else:
            title = self.title

        self.draw_rectangle(0, 0, self.h, self.w)

        x_title = (self.w - len(title) - 2) // 2
        if x_title >= 0:
            self.draw(0, x_title, " " + title + " ")
        else:
            self.draw(0, 1, " " + title[:self.w - 3] + ". ")

    def draw_children(self) -> None:
        for elem in self.children:
            elem.display()

    def add_child(self, elem: NodeDrawable) -> None:
        self.node.add_child(elem.node)


class PanelManager(object):
    def __init__(self, canvas: Canvas):
        self.tree: Tree = Tree("Manager", canvas)
        self.canvas: Canvas = canvas

    def get_elements(self) -> List[Panel]:
        return [child.payload for child in self.tree.root]

    def add_child(self, child: Panel) -> None:
        self.tree.root.add_child(child.node)

    def _deactivate_current(self) -> None:
        node = self.tree.current
        while isinstance(node.payload, Panel):
            node.payload.is_active = False
            node = node.parent

    def get_active(self) -> NodeDrawable:
        return self.tree.current.payload

    def get_next(self) -> NodeDrawable:
        self._deactivate_current()
        self.tree.set_next()

        node = self.tree.current

        while isinstance(node.payload, Panel):
            node.payload.is_active = True
            node = node.parent

        return self.tree.current.payload
