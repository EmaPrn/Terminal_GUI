#!/usr/bin/env python
# -*- coding: utf-8 -*-


class CannotDrawError(Exception):
    "Error to throw when the constraint cannot be satisfied"
    pass


class Constraint(object):
    def __init__(self, nature):
        self.nature = nature


class PositionConstraint(Constraint):
    def __init__(self):
        super().__init__(nature="POSITION")

    @staticmethod
    def check_inputs(direction, h, w, max_y, max_x):
        if not isinstance(direction, str):
            raise TypeError('Incorrect direction type. Direction type must be a String.')

        if direction is not str("x") and direction is not str("y"):
            raise ValueError('Incorrect direction. It must be either x or y (case sensitive).')

        if not isinstance(max_x, int):
            raise TypeError('Incorrect type. Max_x type must be Integer.')

        if not isinstance(max_y, int):
            raise TypeError('Incorrect type. Max_y type must be Integer.')

        if not isinstance(w, int):
            raise TypeError('Incorrect type. W type must be Integer.')

        if not isinstance(h, int):
            raise TypeError('Incorrect type. H type must be Integer.')

    def impose(self, direction, h, w, max_y, max_x):
        pass


class SizeConstraint(Constraint):
    def __init__(self):
        super().__init__(nature="SIZE")

    @staticmethod
    def check_inputs(direction, max_y, max_x):
        if not isinstance(direction, str):
            raise TypeError('Incorrect direction type. Direction type must be a String.')

        if direction is not str("x") and direction is not str("y"):
            raise ValueError('Incorrect direction. It must be either x or y (case sensitive).')

        if not isinstance(max_x, int):
            raise TypeError('Incorrect type. Max_x type must be Integer.')

        if not isinstance(max_y, int):
            raise TypeError('Incorrect type. Max_y type must be Integer.')

    def impose(self, direction, max_y, max_x):
        pass


class AbsolutePosition(PositionConstraint):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def impose(self, direction, h, w, max_y, max_x):

        self.check_inputs(direction, h, w, max_y, max_x)

        out = None

        if direction == "x":
            if self.value < max_x:
                out = self.value
            elif self.value >= max_x:
                raise CannotDrawError('Imposed x must be lower than parent width.')

        if direction == "y":
            if self.value < max_y:
                out = self.value
            elif self.value >= max_y:
                raise CannotDrawError('Imposed y must be lower than parent height.')

        return out


class RelativePosition(PositionConstraint):
    def __init__(self, value):
        super().__init__()
        if 0 <= value <= 1:
            self.value = value
        else:
            raise ValueError('Imposed value must be comprised between 0 and 1.')

    def impose(self, direction, h, w, max_y, max_x):

        self.check_inputs(direction, h, w, max_y, max_x)

        out = None

        if direction == "x":
            out = max_x * self.value

        if self.value is not None:
            out = max_y * self.value

        return int(out)


class CenteredPosition(PositionConstraint):
    def __init__(self):
        super().__init__()

    def impose(self, direction, h, w, max_y, max_x):

        self.check_inputs(direction, h, w, max_y, max_x)

        out = None

        if direction is "x":
            out = (max_x - w) // 2

        if direction is "y":
            out = (max_y - h) // 2

        return out


class AbsoluteSize(SizeConstraint):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def impose(self, direction, max_y, max_x):

        self.check_inputs(direction, max_y, max_x)

        out = None

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
    def __init__(self, value):
        super().__init__()
        if 0 <= value <= 1:
            self.value = value
        else:
            raise ValueError('Imposed value must be comprised between 0 and 1.')

    def impose(self, direction, max_y, max_x):

        self.check_inputs(direction, max_y, max_x)

        out = None

        if direction == "x":
            out = max_x * self.value

        if direction == "y":
            out = max_y * self.value

        return int(out)
