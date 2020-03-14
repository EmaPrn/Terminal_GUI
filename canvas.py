#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class ICanvas(ABC):
    @abstractmethod
    def get_max_yx(self):
        pass

    @abstractmethod
    def draw(self, y_pos, x_pos, text, *args):
        pass

    @abstractmethod
    def draw_rectangle(self, uly, ulx, lry, lrx):
        pass