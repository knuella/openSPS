#!/usr/bin/python
# -*- coding: ascii -*-


class LinearScaler:
    
    def __init__(self, y1, y2, x1, x2):
        self._m = ((float)(y2)-(float)(y1)) / ((float)(x2)-(float)(x1))
        self._n = (float)(y1)-(float)(x1) * self._m
    
    def get_y(self, x):
        return self._m*x + self._n
    
    def get_x(self, y):
        return (y-self._n) / self._m
    
    def get_m(self):
        return self._m
    
    def get_n(self):
        return self._n

