#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports used for type hints
from __future__ import annotations
from typing import List

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
            if self.h > 1:
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

        self.draw_rectangle(0, 0, self.h - 1, self.w - 1)

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
