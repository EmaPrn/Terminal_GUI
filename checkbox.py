#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports used for type hints
from __future__ import annotations
from typing import List, Tuple

from gui_elements import GuiElement, IPositionConstraint, TextStyles
from constraints import size_constraint


class Checkbox(GuiElement):
    def __init__(self, y_constraint: IPositionConstraint, x_constraint: IPositionConstraint, box_id: str, text: str):

        super().__init__(y_constraint, x_constraint, size_constraint("absolute", 1),
                         size_constraint("relative", 1), box_id)

        self.toggle = False
        self._text = text
        self._is_visible = False

    def interact(self, value: int) -> None:
        if value == 343:  # Enter
            self.toggle = False if self.toggle else True
            self.render()

    def render(self) -> None:
        if self.toggle:
            text = "(x) "
        else:
            text = "( ) "

        text = text + self._text
        text = text[:self.parent.get_max_yx()[1] - 4]

        if self.is_active:
            self.draw(0, 0, text, TextStyles.CYAN)
        else:
            self.draw(0, 0, text)

        if self.parent.is_visible:
            self.is_visible = True
        else:
            self.is_visible = False
