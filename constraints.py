#!/usr/bin/env python
# -*- coding: utf-8 -*-

from panels import PositionConstraint, SizeConstraint, CannotDrawError
from typing import Union


class AbsolutePosition(PositionConstraint):
    def __init__(self, value: int):
        self.value: int = value

    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int) -> int:

        out: Union[None, int] = None

        if direction == "x":
            if self.value < max_x:
                out = self.value
            elif self.value >= max_x:
                raise CannotDrawError('Imposed x must be lower than parent width.')

        elif direction == "y":
            if self.value < max_y:
                out = self.value
            elif self.value >= max_y:
                raise CannotDrawError('Imposed y must be lower than parent height.')

        else:
            raise ValueError('Incorrect direction. It must be either x or y (case sensitive).')

        return int(out)


class RelativePosition(PositionConstraint):
    def __init__(self, value: float):
        if 0 <= value <= 1:
            self.value: float = value
        else:
            raise ValueError('Imposed value must be comprised between 0 and 1.')

    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int) -> int:

        if direction == "x":
            out = int(max_x * self.value)

        elif direction == "y":
            out = int(max_y * self.value)

        else:
            raise ValueError('Incorrect direction. It must be either x or y (case sensitive).')

        return int(out)


class CenteredPosition(PositionConstraint):

    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int) -> int:

        if direction is "x":
            out = (max_x - w) // 2

        elif direction is "y":
            out = (max_y - h) // 2

        else:
            raise ValueError('Incorrect direction. It must be either x or y (case sensitive).')

        return out


class AbsoluteSize(SizeConstraint):
    def __init__(self, value: int):
        self.value: int = value

    def impose(self, direction: str, max_y: int, max_x: int) -> int:

        out: Union[None, int] = None

        if direction == "x":
            if self.value < max_x:
                out = self.value
            elif self.value >= max_x:
                raise CannotDrawError('Imposed w must be lower than parent width.')

        if direction == "y":
            if self.value < max_y:
                out = self.value
            elif self.value >= max_y:
                raise CannotDrawError('Imposed h must be lower than parent height.')

        return out


class RelativeSize(SizeConstraint):
    def __init__(self, value: float):
        if 0 <= value <= 1:
            self.value = value
        else:
            raise ValueError('Imposed value must be comprised between 0 and 1.')

    def impose(self, direction: str, max_y: int, max_x: int) -> int:

        out: Union[None, float] = None

        if direction == "x":
            out = max_x * self.value

        if direction == "y":
            out = max_y * self.value

        return int(out)
