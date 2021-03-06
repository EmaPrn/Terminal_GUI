#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports used for type hints
from __future__ import annotations
from typing import List, Tuple

from gui_elements import CannotDrawError, IPositionConstraint, ISizeConstraint, GuiElement, TextStyles


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
                 h_constraint: ISizeConstraint, w_constraint: ISizeConstraint, panel_id: str, max_h=-1, max_w=-1,
                 title: str = '', has_borders: bool = True):

        super().__init__(y_constraint, x_constraint, h_constraint, w_constraint, panel_id,
                         max_h=max_h, max_w=max_w)

        self.has_borders: bool = has_borders
        self.title = title

        if has_borders:
            self._start_drawing_x = 1
            self._start_drawing_y = 1
            self.min_h = 2
            self.min_w = 2

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    @is_visible.setter
    def is_visible(self, is_visible) -> None:
        self._is_visible = is_visible
        if not is_visible:
            for child in self.children:
                child.is_visible = False

    # The use of @property allows to hide the existence of the node.
    @property
    def children(self) -> List[GuiElement]:
        return [child.payload for child in self.node]

    def get_max_yx(self) -> Tuple[int, int]:
        """Implements the method of the ICanvas interface.

        Returns:
            The size of the object as boundaries for its children.
        """
        if self.has_borders:
            return self.h - 2, self.w - 2
        else:
            return self.h, self.w

    def render(self) -> None:
        try:
            if self.has_borders:
                self.draw_borders()
            self.is_visible = True
            self.draw_children()
        except CannotDrawError:
            self.is_visible = False

    def draw_borders(self) -> None:
        """Draw the borders around the panel. The title is displayed at the middle of the top border.
        The title is highlighted if the panel is active

        """
        self.draw_rectangle(-1, -1, self.h - 2, self.w - 2)
        text = self.title[:self.w - 4]

        if self.is_active:
            if len(text) > 0:
                self.draw(-1, 0, " ")
                self.draw(-1, 1, text, TextStyles.BOLD | TextStyles.CYAN)
                self.draw(-1, len(text) + 1, " ")
        else:
            if len(text) > 0:
                self.draw(-1, 0, " " + text + " ")

    def draw_children(self) -> None:
        for elem in self.children:
            # Draw child only if it can fit entirely inside the panel.
            elem.render()

    def add_child(self, elem: GuiElement) -> None:
        self.node.add_child(elem.node)
