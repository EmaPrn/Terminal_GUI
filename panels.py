#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List
from tree import Tree
from canvas import ICanvas
from gui_elements import CannotDrawError, IPositionConstraint, ISizeConstraint, GuiElement


class Panel(GuiElement):
    def __init__(self, y_constraint: IPositionConstraint, x_constraint: IPositionConstraint, h_constraint: ISizeConstraint,
                 w_constraint: ISizeConstraint, title: str = '', has_borders: bool = True):

        super().__init__(y_constraint, x_constraint, h_constraint, w_constraint, title)

        self.has_borders: bool = has_borders

    @property
    def children(self) -> List[GuiElement]:
        return [child.payload for child in self.node]

    def display(self) -> None:
        try:
            if self.has_borders:
                self.draw_borders()
            self.draw_children()
        except CannotDrawError:
            pass

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

    def add_child(self, elem: GuiElement) -> None:
        self.node.add_child(elem.node)


class PanelManager(object):
    def __init__(self, canvas: ICanvas):
        self._tree: Tree = Tree("Manager", canvas)
        self._canvas: ICanvas = canvas

    def get_elements(self) -> List[Panel]:
        return [child.payload for child in self.tree.root]

    def add_child(self, child: Panel) -> None:
        self.tree.root.add_child(child.node)

    def _deactivate_current(self) -> None:
        node = self.tree.current
        while isinstance(node.payload, Panel):
            node.payload.is_active = False
            node = node.parent

    def get_active(self) -> GuiElement:
        return self.tree.current.payload

    def get_next(self) -> GuiElement:
        self._deactivate_current()
        self.tree.set_next()

        node = self.tree.current

        while isinstance(node.payload, Panel):
            node.payload.is_active = True
            node = node.parent

        return self.tree.current.payload
