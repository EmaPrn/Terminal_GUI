#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from tree import Tree, Node
import curses


class CannotDrawError(Exception):
    "Error to throw when the constraint cannot be satisfied"
    pass


class Constraint(ABC):
    pass


class PositionConstraint(Constraint):

    @abstractmethod
    def impose(self, direction, h, w, max_y, max_x):
        pass


class SizeConstraint(Constraint):

    @abstractmethod
    def impose(self, direction, max_y, max_x):
        pass


class MainScreen(object):
    def __init__(self, screen):
        self.screen = screen
        self.screen.clear()
        self.screen.refresh()

    def get_input(self):
        return self.screen.getch()

    def draw(self, y_pos, x_pos, text, *attr):
        max_y, max_x = self.get_max_yx()
        max_len = max_x - x_pos

        if max_len > 0 and x_pos < max_x and y_pos < max_y:
            if len(text) > max_len:
                text = text[:max_len]

            return self.screen.addstr(y_pos, x_pos, text, *attr)

    def draw_rectangle(self, uly, ulx, lry, lrx):
        """Draw a rectangle with corners at the provided upper-left
        and lower-right coordinates.
        """
        if uly != lry and ulx != lrx:
            self.screen.vline(uly + 1, ulx, curses.ACS_VLINE, lry - uly - 1)
            self.screen.hline(uly, ulx + 1, curses.ACS_HLINE, lrx - ulx - 1)
            self.screen.hline(lry, ulx + 1, curses.ACS_HLINE, lrx - ulx - 1)
            self.screen.vline(uly + 1, lrx, curses.ACS_VLINE, lry - uly - 1)
            self.screen.addch(uly, ulx, curses.ACS_ULCORNER)
            self.screen.addch(uly, lrx, curses.ACS_URCORNER)
            self.screen.addch(lry, lrx, curses.ACS_LRCORNER)
            self.screen.addch(lry, ulx, curses.ACS_LLCORNER)

    def get_max_yx(self):
        return self.screen.getmaxyx()

    def delete(self, y_pos, x_pos):
        return self.screen.delch(y_pos, x_pos)

    def clear(self):
        return self.screen.clear()

    def erase(self):
        return self.screen.erase()

    def refresh(self):
        return self.screen.refresh()


class WindowManager(object):
    class _WindowManager:
        def __init__(self, stdscr):
            self.screen = MainScreen(stdscr)
            self.tree = Tree("Manager", self)

        def get_input(self):
            return self.screen.get_input()

        def draw(self, y_pos, x_pos, text, *attr):
            return self.screen.draw(y_pos, x_pos, text, *attr)

        def draw_rectangle(self, uly, ulx, lry, lrx):
            return self.screen.draw_rectangle(uly, ulx, lry, lrx)

        def get_max_yx(self):
            return self.screen.get_max_yx()

        def delete(self, y_pos, x_pos):
            return self.screen.delete(y_pos, x_pos)

        def clear(self):
            return self.screen.clear()

        def erase(self):
            return self.screen.erase()

        def refresh(self):
            return self.screen.refresh()

        def display(self):
            self.erase()
            for child in self.tree.root:
                child.payload.display()
            self.refresh()

        def add_child(self, child):
            if isinstance(child, Panel):
                self.tree.root.add_child(child.node)

            else:
                raise TypeError("Only Panel or Widget objects may be children of a Window Manager")

        def _deactivate_current(self):
            node = self.tree.current
            while node:
                node.payload.is_active = False
                node = node.parent

        def activate_next(self):
            self._deactivate_current()
            self.tree.set_next()

            node = self.tree.current

            while node:
                node.payload.is_active = True
                node = node.parent

    instance = None

    def __init__(self, arg):
        if not WindowManager.instance:
            WindowManager.instance = WindowManager._WindowManager(arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)


class Panel(object):

    def __init__(self, parent, y_constraint, x_constraint, h_constraint, w_constraint, title='', has_borders=True):
        self.title = title
        self.node = Node(title, self)

        self._x_constraint = x_constraint
        self._y_constraint = y_constraint
        self._w_constraint = w_constraint
        self._h_constraint = h_constraint

        self.has_borders = has_borders

        self.is_active = False

    @property
    def parent(self):
        return self.node.parent.payload

    @property
    def children(self):
        return [child.payload for child in self.node]

    @property
    def x(self):
        max_y, max_x = self.parent.get_max_yx()
        return self._x_constraint.impose('x', self.h, self.w, max_y, max_x)

    @x.setter
    def x(self, x):
        if isinstance(x, Constraint):
            if x.nature is 'POSITION':
                self._x_constraint = x
            else:
                raise ValueError('Incorrect constraint nature. The nature of x constraint must be "POSITION".')
        else:
            raise TypeError('Incorrect x type. X must be an instance of a subclass of Constraint.')

    @property
    def y(self):
        max_y, max_x = self.parent.get_max_yx()
        return self._y_constraint.impose('y', self.h, self.w, max_y, max_x)

    @y.setter
    def y(self, y):
        if isinstance(y, Constraint):
            if y.nature is 'POSITION':
                self._y_constraint = y
            else:
                raise ValueError('Incorrect constraint nature. The nature of y constraint must be "POSITION".')
        else:
            raise TypeError('Incorrect y type. Y must be an instance of a subclass of Constraint.')

    @property
    def w(self):
        max_y, max_x = self.parent.get_max_yx()
        return self._w_constraint.impose('x', max_y, max_x)

    @w.setter
    def w(self, w):
        if isinstance(w, Constraint):
            if w.nature is 'SIZE':
                self._w_constraint = w
            else:
                raise ValueError('Incorrect constraint nature. The nature of w constraint must be "DIMENSION".')
        else:
            raise TypeError('Incorrect w type. W must be an instance of a subclass of Constraint.')

    @property
    def h(self):
        max_y, max_x = self.parent.get_max_yx()
        return self._h_constraint.impose('y', max_y, max_x)

    @h.setter
    def h(self, h):
        if isinstance(h, Constraint):
            if h.nature is 'SIZE':
                self._h_constraint = h
            else:
                raise ValueError('Incorrect constraint nature. The nature of h constraint must be "DIMENSION".')
        else:
            raise TypeError('Incorrect h type. H must be an instance of a subclass of Constraint.')

    def get_max_yx(self):
        return self.h, self.w

    def draw(self, y_pos, x_pos, text, *args):
        x = x_pos + self.x
        y = y_pos + self.y
        max_size = self.get_max_yx()[1] - x_pos

        if len(text) > max_size:
            text = text[:max_size]

        return self.parent.draw(y, x, text, *args)

    def display(self):
        try:
            if self.has_borders:
                self.draw_borders()
            self.draw_children()
        except CannotDrawError:
            pass

    def draw_rectangle(self, uly, ulx, lry, lrx):
        """Draw a rectangle with corners at the provided upper-left
        and lower-right coordinates.
        """
        return self.parent.draw_rectangle(uly + self.y, ulx + self.x, lry + self.y, lrx + self.x)

    def draw_borders(self):
        if self.is_active:
            title = "A: " + self.title
        else:
            title = self.title

        self.draw_rectangle(0,0,self.h,self.w)

        x_title = (self.w - len(title) - 2) // 2
        if x_title >= 0:
            self.draw(0, x_title, " " + title + " ")
        else:
            self.draw(0, 1, " " + title[:self.w - 3] + ". ")

    def draw_children(self):
        for elem in self.children:
            elem.display()

    def add_child(self, elem):
        if isinstance(elem, Panel):
            self.node.add_child(elem.node)
        else:
            raise TypeError("Only Panel or Widget objects may be children of a Panel")
