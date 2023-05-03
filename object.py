"""

An object is a physical body that moves through a pre-planned trajectory in an
environment. It consists of the full 2d representation of the object's appearance (2d array of pseudo-greyscale)
and a list of positions, orientations, and times between new positions, which the object passes
through over the course of a simulation.



"""

import constants
import numpy as np
import pygame

class Object:

    def __init__(self, id, visual, path):
        self.id = id        
        self.rotation = 0
        self.size = self.width, self.height = visual.shape
        self.visual = visual
        self.path = path 
        self.pos = self.x, self.y = float(self.path[0][0]), float(self.path[0][1]) 
        self.time_until_change = self.path[0][2]
        self.orientation = self.path[0][3]
        self.path_progress = 0
        self.prev_pos = None


    """
    
    Inputs:
    - degrees -> number of degrees to rotate the object relative to its original position (must be 0, 90, 180, or 270)

    Output:
    - A 2D array describing the object's appearance after being rotated the specified number of degrees

    """
    def rotate(self, degrees): 
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


    """
    
    Inputs:
    - N/A

    Output:
    - N/A

    Description:
    This function updates the object's position and orientation according to its
    current progress on its pre-defined path.

    """
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

    """
    
    Inputs:
    - screen -> The Pygame window used for display
    - is_tracked -> True if the object is being correctly tracked by the camera
    - is_false_tracked -> True if the object is being incorrectly tracked by the camera

    Output:
    - N/A

    Description:
    This function updates the object's position and orientation according to its current
    progress on its pre-defined path, then updates screen with the object's new state. An
    object gets a blue outline if it is being correctly tracked by the camera. An object
    gets a purple outline if it is being incorrectly tracked by the camera.

    """
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
        


