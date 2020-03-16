#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gui_elements import IPositionConstraint, ISizeConstraint, CannotDrawError
from typing import Union, Any


class UnknownConstraintError(Exception):
    """Error to throw when the requested constraint is not defined."""
    pass


def position_constraint(nature: str, value: Any = None) -> IPositionConstraint:
    if nature.lower() == "absolute":
        if value != None:
            return _AbsolutePosition(value)
        else:
            raise(ValueError("A constraint value must be specified for absolute position constraints."))
    elif nature.lower() == "relative":
        if value != None:
            return _RelativePosition(value)
        else:
            raise(ValueError("A constraint value must be specified for relative position constraints."))
    elif nature.lower() == "centered":
        return _CenteredPosition()
    else:
        raise(UnknownConstraintError("Unknown type of constraint: {}".format(nature)))


def size_constraint(nature: str, value: Any = None) -> ISizeConstraint:
    if nature.lower() == "absolute":
        return _AbsoluteSize(value)
    elif nature.lower() == "relative":
        return _RelativeSize(value)
    else:
        raise(UnknownConstraintError("Unknown type of constraint: {}".format(nature)))


class _AbsolutePosition(IPositionConstraint):
    """ This constraint impose a given position to the GUI element.
        The position must respect the boundaries imposed by the parent of the element.

        Attributes:
            value (int): The absolute position to impose to the element.

    """

    def __init__(self, value: int):
        self.value: int = value

    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int) -> int:
        """Called when trying to impose the position constraint.

        Parameters:
            direction (str): Either "x" or "y".
            h (int): The height of the caller.
            w (int): The width of the caller.
            max_y (int): Bounding y value (I.e. the y size of its parent container).
            max_x (int): Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed position if possible, raise CannotDrawError otherwise.
        """

        out: Union[None, int] = None

        if direction == "x":
            if self.value < max_x:
                out = self.value
            elif self.value >= max_x:
                raise CannotDrawError('Imposed x must be lower than parent width.')
            elif self.value + w - 1 >= max_x:
                raise CannotDrawError('The GUI element must fit entirely inside its parent.')

        elif direction == "y":
            if self.value < max_y:
                out = self.value
            elif self.value >= max_y:
                raise CannotDrawError('Imposed y must be lower than parent height.')
            elif self.value + h - 1 >= max_y:
                raise CannotDrawError('The GUI element must fit entirely inside its parent.')

        else:
            raise ValueError('Incorrect direction. It must be either x or y (case sensitive).')

        return int(out)


class _RelativePosition(IPositionConstraint):
    """ This constraint impose a given position to the GUI element.
        The position must respect the boundaries imposed by the parent of the element.

        Attributes:
            value (float): The position to impose to the element expressed as fraction of the limit
                            imposed by the parent.

        Note:
            Value must be comprised between 0 and 1.

    """

    def __init__(self, value: float):
        if 0 <= value <= 1:
            self.value: float = value
        else:
            raise ValueError('Imposed value must be comprised between 0 and 1.')

    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int) -> int:
        """Called when trying to impose the position constraint.

        Parameters:
            direction (str): Either "x" or "y".
            h (int): The height of the caller.
            w (int): The width of the caller.
            max_y (int): Bounding y value (I.e. the y size of its parent container).
            max_x (int): Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed position if possible, raise CannotDrawError otherwise.
        """
        if direction == "x":
            out = int(max_x * self.value)
            if out + w - 1 >= max_x:
                raise CannotDrawError('The GUI element must fit entirely inside its parent.')

        elif direction == "y":
            out = int(max_y * self.value)
            if out + h - 1 >= max_y:
                raise CannotDrawError('The GUI element must fit entirely inside its parent.')

        else:
            raise ValueError('Incorrect direction. It must be either x or y (case sensitive).')

        return int(out)


class _CenteredPosition(IPositionConstraint):
    """ This constraint center the GUI element at the middle of its parent."""

    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int) -> int:
        """Called when trying to impose the position constraint.

        Parameters:
            direction (str): Either "x" or "y".
            h (int): The height of the caller.
            w (int): The width of the caller.
            max_y (int): Bounding y value (I.e. the y size of its parent container).
            max_x (int): Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed position if possible, raise CannotDrawError otherwise.
        """

        if direction is "x":
            out = (max_x - w) // 2

        elif direction is "y":
            out = (max_y - h) // 2

        else:
            raise ValueError('Incorrect direction. It must be either x or y (case sensitive).')

        if out < 0:
            raise CannotDrawError('The GUI element must be smaller than its parent.')

        return out


class _AbsoluteSize(ISizeConstraint):
    """ This constraint impose a given size to the GUI element.
        The size must respect the boundaries imposed by the parent of the element.

        Attributes:
            value (int): The absolute size to impose to the element.

    """

    def __init__(self, value: int):
        self.value: int = value

    def impose(self, direction: str, min_h: int, min_w: int, max_y: int, max_x: int) -> int:
        """Called when trying to impose the size constraint.

        Parameters:
            direction (str): Either "x" or "y".
            min_h (int): Minimum h value to draw the element.
            min_w (int): Minimum w value to draw the element.
            max_y: Bounding y value (I.e. the y size of its parent container).
            max_x: Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed size if possible, raise CannotDrawError otherwise.
        """

        out: Union[None, int] = None

        if direction == "x":
            if self.value < max_x:
                out = self.value

            if self.value < min_w:
                raise CannotDrawError('Imposed w must be bigger than parent min_w.')
            elif self.value >= max_x:
                raise CannotDrawError('Imposed w must be lower than parent width.')

        if direction == "y":
            if self.value < max_y:
                out = self.value

            if self.value < min_h:
                raise CannotDrawError('Imposed w must be bigger than parent min_h.')
            elif self.value >= max_y:
                raise CannotDrawError('Imposed h must be lower than parent height.')

        return out


class _RelativeSize(ISizeConstraint):
    """ This constraint impose a given size to the GUI element.
        The size must respect the boundaries imposed by the parent of the element.

        Attributes:
            value (int): The relative size to impose to the element. Expressed as a fraction of the parent size.

        Note:
            Value must be comprised between 0 and 1.

    """

    def __init__(self, value: float):
        if 0 <= value <= 1:
            self.value = value
        else:
            raise ValueError('Imposed value must be comprised between 0 and 1.')

    def impose(self, direction: str, min_h: int, min_w: int, max_y: int, max_x: int) -> int:
        """Called when trying to impose the size constraint.

        Parameters:
            direction (str): Either "x" or "y".
            min_h (int): Minimum h value to draw the element.
            min_w (int): Minimum w value to draw the element.
            max_y: Bounding y value (I.e. the y size of its parent container).
            max_x: Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed size if possible, raise CannotDrawError otherwise.
        """

        out: Union[None, float] = None

        if direction == "x":
            out = max_x * self.value
            if out < min_w:
                raise CannotDrawError('Imposed w must be bigger than parent min_w.')

        if direction == "y":
            out = max_y * self.value
            if out < min_h:
                raise CannotDrawError('Imposed h must be bigger than parent min_h.')

        return int(out)
