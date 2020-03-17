#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports used for type hints
from __future__ import annotations
from typing import Tuple, List, Union

# Allows the definition of interfaces
from abc import ABC, abstractmethod

# Import needed by ElementTreeManager
from _tree import Node, Tree


class TextStyles(object):
    # Flags for drawing options
    HIGHLIGHTED = 2
    UNDERLINE = 4
    BOLD = 8
    RED = 16
    GREEN = 32
    YELLOW = 64
    BLUE = 128
    MAGENTA = 256
    CYAN = 512


class CannotDrawError(Exception):
    """Error to throw when a constraint cannot be satisfied."""
    pass


class IConstraint(ABC):
    """Interface to the constraints that can be imposed to a GUI Element."""
    pass


class IPositionConstraint(IConstraint):
    """Interface to the constraints that can be imposed to the position of GUI Element."""
    @abstractmethod
    def impose(self, direction: str, h: int, w: int, max_y: int, max_x: int) -> int:
        """Called when trying to impose the position constraint.

        Parameters:
            direction (str): Either "x" or "y".
            h (int): The height of the caller. Used to impose top, bottom or centered alignments.
            w (int): The width of the caller. Used to impose left, right or centered alignments.
            max_y (int): Bounding y value (I.e. the y size of its parent container).
            max_x (int): Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed position if possible, raise CannotDrawError otherwise.
        """
        pass


class ISizeConstraint(IConstraint):
    @abstractmethod
    def impose(self, direction: str, min_h: int, min_w: int, max_y: int, max_x: int):
        """Called when trying to impose the size constraint.

        Parameters:
            direction (str): Either "x" or "y".
            min_h (int): Minimum h value to draw the element.
            min_w (int): Minimum w value to draw the element.
            max_y (int): Bounding y value (I.e. the y size of its parent container).
            max_x (int): Bounding x value (I.e. the x size of its parent container).

        Returns:
            The computed size if possible, raise CannotDrawError otherwise.
        """
        pass


class ICanvas(ABC):
    @abstractmethod
    def get_max_yx(self):
        """Compute and returns the boundaries for x and y positions."""
        pass

    @abstractmethod
    def draw(self, y_pos: int, x_pos: int, text: str, attr: int = 0):
        """Draw a string of text at a given (relative) position.

        Parameters:
            y_pos (int): The relative y position to start drawing the text.
            x_pos (int): The relative x position to start drawing the text.
            text (str): The text to draw.
            attr (int): Optional parameters to specify text styles.
        """
        pass

    @abstractmethod
    def draw_rectangle(self, uly: int, ulx: int, lry: int, lrx: int):
        """Draw a rectangle with corners at the provided upper-left and lower-right coordinates.

        Parameters:
            uly (int): y position of the Upper-Left corner of the rectangle
            ulx (int): x position of the Upper-Left corner of the rectangle
            lry (int): y position of the Lower-Right corner of the rectangle
            lrx (int): x position of the Lower-Right corner of the rectangle

        """
        pass


class GuiElement(ICanvas):
    """Generic Element that can be drawn on the screen.
        Implements the ICanvas interface as it is possible to draw other elements on top of it.

        Attributes:
            title (str): The name of the element. Can be shown after rendering.
            element_id (str): The unique identifier of the element.
            y_constraint (IPositionConstraint): Constraint for the y position of the element.
            x_constraint (IPositionConstraint): Constraint for the x position of the element.
            h_constraint (ISizeConstraint): Constraint for the height of the element.
            w_constraint (ISizeConstraint): Constraint for the width of the element.
            is_active (bool): Internal state of the element. Useful to allow actions on it.
                              Can modify the appearance on screen of the element.
    """
    def __init__(self, y_constraint: IPositionConstraint, x_constraint: IPositionConstraint,
                 h_constraint: ISizeConstraint, w_constraint: ISizeConstraint, element_id: str, min_h: int = 0,
                 min_w: int = 0, max_h: int = -1, max_w: int = -1, title: str = ''):

        self.title: str = title

        # Each element is associated to a node.
        # It allows to invoke its parent drawing functions up to the window render itself.
        self._node: Node = Node(element_id, self)

        self._x_constraint: IPositionConstraint = x_constraint
        self._y_constraint: IPositionConstraint = y_constraint
        self._w_constraint: ISizeConstraint = w_constraint
        self._h_constraint: ISizeConstraint = h_constraint

        self.is_active: bool = False
        self._is_visible: bool = False

        self._start_drawing_x = 0
        self._start_drawing_y = 0

        self.min_h = min_h
        self.min_w = min_w

        self.max_h = max_h
        self.max_w = max_w

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    @is_visible.setter
    def is_visible(self, is_visible) -> None:
        self._is_visible = is_visible

    # The use of @property allows to hide the existence of the node.
    @property
    def parent(self) -> GuiElement:
        return self._node.parent.payload

    # The node should be not modified, it lives together with the GUI element.
    @property
    def node(self) -> Node:
        return self._node

    # x position, y position, width and height can be obtained through properties.
    # Each time that the property is called the corresponding constraint is imposed and the calculated result returned.

    @property
    def x(self) -> int:
        max_y, max_x = self.parent.get_max_yx()
        return self._x_constraint.impose('x', self.h, self.w, max_y, max_x)

    @property
    def y(self) -> int:
        max_y, max_x = self.parent.get_max_yx()
        return self._y_constraint.impose('y', self.h, self.w, max_y, max_x)

    @property
    def w(self) -> int:
        max_y, max_x = self.parent.get_max_yx()
        if self.max_w >= 0:
            return min(self.max_w, self._w_constraint.impose('x', self.min_h, self.min_w, max_y, max_x))
        else:
            return self._w_constraint.impose('x', self.min_h, self.min_w, max_y, max_x)

    @property
    def h(self) -> int:
        max_y, max_x = self.parent.get_max_yx()
        if self.max_h >= 0:
            return min(self.max_h, self._h_constraint.impose('y', self.min_h, self.min_w, max_y, max_x))
        else:
            return self._h_constraint.impose('y', self.min_h, self.min_w, max_y, max_x)

    def get_max_yx(self) -> Tuple[int, int]:
        """Implements the method of the ICanvas interface.

        Returns:
            The size of the object as boundaries for its children.
        """
        return self.h, self.w

    def draw(self, y_pos: int, x_pos: int, text: str, attr: int = 0) -> None:
        """Implements the method of the ICanvas interface."""
        x = x_pos + self._start_drawing_x + self.x
        y = y_pos + self._start_drawing_y + self.y
        max_size = self.get_max_yx()[1] - x_pos

        if len(text) > max_size:
            text = text[:max_size]

        self.parent.draw(y, x, text, attr)

    def draw_rectangle(self, uly: int, ulx: int, lry: int, lrx: int) -> None:
        """Implements the method of the ICanvas interface."""
        self.parent.draw_rectangle(uly + self._start_drawing_y + self.y, ulx + self._start_drawing_x + self.x,
                                   lry + self._start_drawing_y + self.y, lrx + self._start_drawing_x + self.x)

    @abstractmethod
    def render(self) -> None:
        """Render the given GUI element.
            It should use the draw method."""
        pass


class ElementTreeManager(object):
    """Manage a tree made of panels.
        Based the concept of active element, it can step trough all the leaves of the tree to activate them.

        Note:
        Only one leaf can be active at a given time.

        Attributes:
            canvas (ICanvas): The canvas where the elements will be drawn. It forms the payload of the root node
                              of the managed tree, this allows the other elements to draw on it just by calling
                              the methods of their parents.

    """
    def __init__(self, canvas: ICanvas):
        self._tree: Tree = Tree("Manager", canvas)
        self._canvas: ICanvas = canvas

    @property
    def tree(self):
        return self._tree

    def get_elements(self) -> List[GuiElement]:
        return [child.payload for child in self.tree.root]

    def add_element(self, child: GuiElement) -> None:
        self.tree.root.add_child(child.node)

    def _deactivate_current(self) -> None:
        """ Recursively deactivate the current active node and all its parents up to the root node."""
        self.tree.current.is_active = False

    def reset_active(self) -> GuiElement:
        """" This method deactivate the current active element and activate the element contained
             in the first leaf.

             Returns:
                 The newly activated element (the one contained in the first leaf).
        """

        self.tree.current.payload.is_active = False
        self.tree.reset_current()

        first_node = self.tree.set_next()
        counter = 0
        while not first_node.payload.is_visible and counter <= len(self.tree.leaves):
            first_node = self.tree.set_next()
            counter += 1

        if counter != len(self.tree.leaves):
            first_node.payload.is_active = True
            return self.tree.current.payload
        else:
            return None

    def get_active(self) -> GuiElement:
        return self.tree.current.payload

    def activate_next(self) -> Union[None, GuiElement]:
        """" This method deactivate the current active element and activate the element contained
             in the next leaf.

             Returns:
                 The newly activated element (the one contained in the leaf).
        """
        self.tree.current.payload.is_active = False

        next_node = self.tree.set_next()
        counter = 0
        while not next_node.payload.is_visible and counter <= len(self.tree.leaves):
            next_node = self.tree.set_next()
            counter +=1

        if counter != len(self.tree.leaves):
            next_node.payload.is_active = True
            return self.tree.current.payload
        else:
            return None
