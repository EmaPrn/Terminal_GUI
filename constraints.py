#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gui_elements import IPositionConstraint, ISizeConstraint, CannotDrawError
from typing import Union


class AbsolutePosition(IPositionConstraint):
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
            h (int): Not requested by this constraint.
            w (int): Not requested by this constraint.
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

        elif direction == "y":
            if self.value < max_y:
                out = self.value
            elif self.value >= max_y:
                raise CannotDrawError('Imposed y must be lower than parent height.')

        else:
            raise ValueError('Incorrect direction. It must be either x or y (case sensitive).')

        return int(out)


class RelativePosition(IPositionConstraint):
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
            h (int): Not requested by this constraint.
            w (int): Not requested by this constraint.
            max_y (int): Bounding y value (I.e. the y size of its parent container).
            max_x (int): Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed position if possible, raise CannotDrawError otherwise.
        """
        if direction == "x":
            out = int(max_x * self.value)

        elif direction == "y":
            out = int(max_y * self.value)

        else:
            raise ValueError('Incorrect direction. It must be either x or y (case sensitive).')

        return int(out)


class CenteredPosition(IPositionConstraint):
    """ This constraint center the GUI element at the middle of its parent."""

    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int) -> int:
        """Called when trying to impose the position constraint.

        Parameters:
            direction (str): Either "x" or "y".
            h (int): Not requested by this constraint.
            w (int): Not requested by this constraint.
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

        return out


class AbsoluteSize(ISizeConstraint):
    """ This constraint impose a given size to the GUI element.
        The size must respect the boundaries imposed by the parent of the element.

        Attributes:
            value (int): The absolute size to impose to the element.

    """

    def __init__(self, value: int):
        self.value: int = value

    def impose(self, direction: str, max_y: int, max_x: int) -> int:
        """Called when trying to impose the size constraint.

        Parameters:
            direction (str): Either "x" or "y".
            max_y: Bounding y value (I.e. the y size of its parent container).
            max_x: Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed size if possible, raise CannotDrawError otherwise.
        """

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


class RelativeSize(ISizeConstraint):
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

    def impose(self, direction: str, max_y: int, max_x: int) -> int:
        """Called when trying to impose the size constraint.

        Parameters:
            direction (str): Either "x" or "y".
            max_y: Bounding y value (I.e. the y size of its parent container).
            max_x: Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed size if possible, raise CannotDrawError otherwise.
        """

        out: Union[None, float] = None

        if direction == "x":
            out = max_x * self.value

        if direction == "y":
            out = max_y * self.value

        return int(out)
