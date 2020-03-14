#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List
from tree import Tree
from canvas import ICanvas
from gui_elements import CannotDrawError, IPositionConstraint, ISizeConstraint, GuiElement


class Panel(GuiElement):
    """A container for other GUI elements. Elements are handled as children of a tree node, already defined in the
        GUI element class. It is possible to render it with or without borders.

        Attributes:
            title (str): The name of the panel. Can be shown to after rendering.
            panel_id (str): The unique identifier of the panel.
            y_constraint (IPositionConstraint): Constraint for the y position of the panel.
            x_constraint (IPositionConstraint): Constraint for the x position of the panel.
            h_constraint (ISizeConstraint): Constraint for the height of the panel.
            w_constraint (ISizeConstraint): Constraint for the width of the panel.
            has_borders (bool): Set to True to draw borders. Title is rendered on the top border.

    """
    def __init__(self, y_constraint: IPositionConstraint, x_constraint: IPositionConstraint,
                 h_constraint: ISizeConstraint, w_constraint: ISizeConstraint, panel_id: str,
                 title: str = '', has_borders: bool = True):

        super().__init__(y_constraint, x_constraint, h_constraint, w_constraint, panel_id, title)

        self.has_borders: bool = has_borders

    # The use of @property allows to hide the existence of the node.
    @property
    def children(self) -> List[GuiElement]:
        return [child.payload for child in self.node]

    def render(self) -> None:
        try:
            if self.has_borders:
                self.draw_borders()
            self.draw_children()
        except CannotDrawError:
            pass

    def draw_borders(self) -> None:
        """Draw the borders around the panel. The title is displayed at the middle of the top border.
        The title is highlighted if the panel is active

        """
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
            elem.render()

    def add_child(self, elem: GuiElement) -> None:
        self.node.add_child(elem.node)


class PanelManager(object):
    """Manage a tree made of panels.
        Based the concept of active panel/element, it can step trough all the leaves of the tree to activate them.

        Note:
        Only one leaf can be active at a given time. If a leaf is active, all the panels crossed in the path
        from the root to the active leaf will be active as well.

        Attributes:
            canvas (ICanvas): The canvas where the panels will be drawn. It forms the payload of the root node
                              of the managed tree, this allows the other panels to draw on it just by calling
                              the methods of their parents.

    """
    def __init__(self, canvas: ICanvas):
        self._tree: Tree = Tree("Manager", canvas)
        self._canvas: ICanvas = canvas

    @property
    def tree(self):
        return self._tree

    def get_panels(self) -> List[Panel]:
        return [child.payload for child in self.tree.root]

    def add_panel(self, child: Panel) -> None:
        self.tree.root.add_child(child.node)

    def _deactivate_current(self) -> None:
        """ Recursively deactivate the current active node and all its parents up to the root node."""
        node = self.tree.current
        while isinstance(node.payload, GuiElement):
            node.payload.is_active = False
            node = node.parent

    def get_active(self) -> GuiElement:
        return self.tree.current.payload

    def get_next(self) -> GuiElement:
        """" This method deactivate the current active element (and all its parents) and activate the element contained
             in the next leaf. The activation process go through all the nodes in the path between the root
             node and the leaf.

             Returns:
                 The newly activated element (the one contained in the leaf).
        """
        self._deactivate_current()
        self.tree.set_next()

        node = self.tree.current

        while isinstance(node.payload, Panel):
            node.payload.is_active = True
            node = node.parent

        return self.tree.current.payload
