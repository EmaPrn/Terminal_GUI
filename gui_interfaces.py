#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from tree import Node


class Canvas(ABC):
    @abstractmethod
    def get_max_yx(self):
        pass

    @abstractmethod
    def draw(self, y_pos, x_pos, text, *args):
        pass

    @abstractmethod
    def draw_rectangle(self, uly, ulx, lry, lrx):
        pass


class Drawable(Canvas):

    @abstractmethod
    def display(self):
        pass

class NodeDrawable(Drawable):
    @abstractmethod
    @property
    def node(self) -> Node:
        pass