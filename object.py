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
import constants

class Object:

    def __init__(self, id, visual, path):
        self.id = id        
        self.rotation = 0
        self.size = self.width, self.height = visual.shape
        self.visual = visual
        self.path = path # List of tuples (newX, newY, time, orientation)
        self.pos = self.x, self.y = float(self.path[0][0]), float(self.path[0][1]) # Based on map coords, not real coords
        self.time_until_change = self.path[0][2]
        self.orientation = self.path[0][3]
        self.path_progress = 0
        self.prev_pos = None

    def rotate(self, degrees): # Must be divisible by 90
        if degrees == 0:
            return self.visual
        elif degrees == 90:
            return np.rot90(self.visual, 1)   
        elif degrees == 180:
            return np.rot90(self.visual, 2)   
        elif degrees == 270:
            return np.rot90(self.visual, 3)   
        else:
            return None

    def progress_on_path(self):
        if self.path_progress == len(self.path) - 1:
            return
        if self.path_progress < len(self.path) - 1:
            if self.time_until_change == 0:
                self.path_progress += 1
                self.time_until_change = self.path[self.path_progress][2]
            if self.path_progress == len(self.path) - 1:
                return
            prev_x, prev_y, speed, orientation = self.path[self.path_progress]
            dest_x, dest_y, _, _ = self.path[self.path_progress + 1]
            dx = (dest_x - prev_x) / speed
            dy = (dest_y - prev_y) / speed
            self.x += dx
            self.y += dy
            self.pos = (self.x, self.y)
            self.time_until_change -= 1
            self.orientation = orientation

    def update(self, screen, is_tracked, is_false_tracked):
        self.prev_pos = self.pos
        self.progress_on_path()
        x_offset = int(self.x * constants.SCALE)
        y_offset = int(self.y * constants.SCALE)
        temp_visual = self.rotate(self.orientation)
        for y in range(temp_visual.shape[1]):
            for x in range(temp_visual.shape[0]):
                if temp_visual[x,y] > 0:
                    pygame.draw.rect(
                        screen,
                        (20 * temp_visual[x,y], 20 * temp_visual[x,y], 20 * temp_visual[x,y]),
                        (int(x_offset + x * constants.SCALE), int(y_offset + y * constants.SCALE), constants.SCALE, constants.SCALE)
                    )
        if is_tracked:
            pygame.draw.rect(
                screen,
                (0, 255, 255),
                (x_offset, y_offset, constants.SCALE * temp_visual.shape[0], constants.SCALE * temp_visual.shape[1]),
                2
            )
        elif is_false_tracked:
            pygame.draw.rect(
                screen,
                (191, 64, 191),
                (x_offset, y_offset, constants.SCALE * temp_visual.shape[0], constants.SCALE * temp_visual.shape[1]),
                2
            )
        


