"""

Class to describe a object. It consists of the following fields:
- Id
- Position
- Visual Properties (For 2D, we treat the object as some set of pixels with particular colors)
- Path and Rotations 

The object should have functions to move and rotate. 
"""

import numpy as np

class Object:

    def __init__(self):
        self.id = 0
        self.pos = self.x, self.y = (0,0)
        self.rotation = 0
        self.size = self.width, self.height = (5,5)
        self.visual = np.zeros(self.size)
        self.path = None
        self.rotations = None

    def rotate(self, degrees): # Must be divisible by 90
        if degrees == 0:
            return self.visual
        elif degrees == 90:
            pass
        elif degrees == 180:
            pass
        elif degrees == 270:
            pass
        else:
            return None

    def update(self):
        self.pos = self.path[0]
        self.rotation = self.rotations[0]
        self.path = self.path[1:]
        self.rotations = self.rotations[1:]


