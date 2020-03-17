#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports used for type hints
from __future__ import annotations
from typing import List, Tuple

from gui_elements import GuiElement, IPositionConstraint, TextStyles, CannotDrawError
from constraints import size_constraint


class RadioButton(GuiElement):
    def __init__(self, y_constraint: IPositionConstraint, x_constraint: IPositionConstraint, box_id: str, text: str):

        super().__init__(y_constraint, x_constraint, size_constraint("absolute", 1),
                         size_constraint("relative", 1), box_id, min_w=len(text) + 4)

        self.toggle = False
        self._text = text
        self._is_visible = False

    def interact(self, value: int = 0) -> None:
        if not self.toggle:
            for brother in self.parent.node:
                if isinstance(brother.payload, RadioButton):
                    brother.payload.toggle = False
            self.toggle = True
            self.parent.render()

    def render(self) -> None:
        if self.toggle:
            text = "(x) "
        else:
            text = "( ) "

        text = text + self._text

        try:
            if self.is_active:
                self.draw(0, 0, text, TextStyles.CYAN)
            else:
                self.draw(0, 0, text)

            if self.parent.is_visible:
                self.is_visible = True
            else:
                self.is_visible = False

        except CannotDrawError:
            self.is_visible = False
