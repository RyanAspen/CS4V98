"""

Class to describe a object. It consists of the following fields:
- Id
- Position
- Visual Properties (For 2D, we treat the object as some set of pixels with particular colors)
- Path and Rotations 

The object should have functions to move and rotate. 
"""

import numpy as np
import pygame

class Object:

    def __init__(self):
        self.id = 0
        self.pos = self.x, self.y = (0,0)
        self.rotation = 0
        self.size = self.width, self.height = (5,5)
        self.initial_visual = np.zeros(self.size)
        self.visual = self.initial_visual
        self.initial_path = list()
        self.path = list() # List of tuples (newX, newY, time, orientation)
        self.time_until_change = 0

    def rotate(self, degrees): # Must be divisible by 90
        if degrees == 0:
            return self.initial_visual
        elif degrees == 90:
            return np.rot90(self.initial_visual, 1)   
        elif degrees == 180:
            return np.rot90(self.initial_visual, 2)   
        elif degrees == 270:
            return np.rot90(self.initial_visual, 3)   
        else:
            return None

    def update(self, screen):
        if len(self.path) > 0 and self.time_until_change == 0:
            self.x, self.y, self.time_until_change, self.rotation = self.path[0]
            self.visual = self.rotate(self.rotation)
            self.path = self.path[1:]
        elif self.time_until_change > 0:
            self.time_until_change -= 1
        for y in range(self.visual.shape[1]):
            for x in range(self.visual.shape[0]):
                if self.visual[x,y] > 0:
                    pygame.draw.rect(
                        screen,
                        self.visual[x,y] * (20, 20, 20),
                        (self.x + x*5, self.y + y*5, 5, 5)
                    )
        


