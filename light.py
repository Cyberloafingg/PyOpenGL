import math

from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

class Light:
    def __init__(self,_pos,_angle,_color):
        self.light_pos = _pos
        self.light_angle = _angle
        self.light_color = _color
        self.constant = 1.0
        self.linear = 0.09
        self.quadratic = 0.0032