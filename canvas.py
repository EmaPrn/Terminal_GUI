#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class ICanvas(ABC):
    @abstractmethod
    def get_max_yx(self):
        """Compute and returns the boundaries for x and y positions."""
        pass

    @abstractmethod
    def draw(self, y_pos, x_pos, text, *args):
        """Draw a string of text at a given (relative) position.

        Parameters:
            y_pos (int): The relative y position to start drawing the text.
            x_pos (int): The relative x position to start drawing the text.
            text (str): The text to draw.
            args: Optional parameters to specify text styles.
        """
        pass

    @abstractmethod
    def draw_rectangle(self, uly, ulx, lry, lrx):
        """Draw a rectangle with corners at the provided upper-left and lower-right coordinates.

        Parameters:
            uly: y position of the Upper-Left corner of the rectangle
            ulx: x position of the Upper-Left corner of the rectangle
            lry: y position of the Lower-Right corner of the rectangle
            lrx: x position of the Lower-Right corner of the rectangle

        """
        pass