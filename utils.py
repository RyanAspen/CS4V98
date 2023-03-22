"""

Utility methods used by other objects.

"""

import numpy as np
from queue import Queue


# Positions should go from most recent to least recent.
def estimate_next_position(positions):
    p = len(positions)
    curr_pos = cx, cy = positions[0]
    #next

def is_pos_visible_from_pos(start, end, environment):
        """
          Draw a line between start and end
          For every position that that line passes through, check if it is a wall. If it is, return false.
          Return true.
        """

        # Using Bresenham's Line Algorithm
        x0, y0 = start
        x1, y1 = end

        def plotLineLow(x0, y0, x1, y1):
            dx = x1 - x0
            dy = y1 - y0
            yi = 1
            if dy < 0:
                yi = -1
                dy = -dy
            D = (2 * dy) - dx
            y = y0

            for x in range(x0, x1 + 1):
                if environment.map[x, y] > 0:
                    return False
                if D > 0:
                    y += yi
                    D += 2 * (dy - dx)
                else:
                    D += 2*dy
            return True

        def plotLineHigh(x0, y0, x1, y1):
            dx = x1 - x0
            dy = y1 - y0
            yi = 1
            if dx < 0:
                xi = -1
                dx = -dx
            D = (2 * dx) - dy
            x = x0

            for y in range(y0, y1 + 1):
                if environment.map[x, y] > 0:
                    return False
                if D > 0:
                    x += xi
                    D += 2 * (dx - dy)
                else:
                    D += 2*dx
            return True

        if abs(y1 - y0) < abs(x1 - x0):
            if x0 > x1:
                return plotLineLow(x1, y1, x0, y0)
            else:
                return plotLineLow(x0, y0, x1, y1)
        else:
            if y0 > y1:
                return plotLineHigh(x1, y1, x0, y0)
            else:
                return plotLineHigh(x0, y0, x1, y1)

def initialize_vision_ranges(environment):

    def is_pos_on_map(pos, environment):
        x,y = pos
        return x >= 0 and x < environment.width and y >= 0 and y < environment.height

    for camera in environment.cameras:
        camera.vision_range = np.zeros(environment.size)
        start_position = camera.pos
        position_queue = Queue()
        position_queue.put(start_position)
        """
          Start at the camera's position, then recursively build outward as follows (BFS):
          1. If the current position's value is 0 and is not a wall, check if we can draw a line from the current position to the camera's 
          position without hitting a wall. If we can, set the vision range value of that position to 1 and add neighboring positions to
          the position queue. Otherwise, set it to 2.
        """
        while not position_queue.empty():
            current_position = curr_x, curr_y = position_queue.get()
            if is_pos_on_map(current_position, environment) and camera.vision_range[curr_x, curr_y] == 0 and environment.map[curr_x, curr_y] == 0:
                if is_pos_visible_from_pos(start_position, current_position):                    
                    camera.vision_range[curr_x, curr_y] = 1
                    position_queue.put((curr_x - 1, curr_y - 1))
                    position_queue.put((curr_x, curr_y - 1))
                    position_queue.put((curr_x + 1, curr_y - 1))
                    position_queue.put((curr_x - 1, curr_y))
                    position_queue.put((curr_x + 1, curr_y))
                    position_queue.put((curr_x - 1, curr_y + 1))
                    position_queue.put((curr_x, curr_y + 1))
                    position_queue.put((curr_x + 1, curr_y + 1))
                else:
                    camera.vision_range[curr_x, curr_y] = 2
                
        

def can_camera_see_position(camera, position):
    x, y = position
    return camera.vision_range[x,y] == 1

def can_camera_see_camera(camera1, camera2):
    c2x, c2y = camera2.pos
    return camera1.vision_range[c2x, c2y] == 1

def get_object_appearance(camera, object):
    # Return an array representing the appearance of the object except every pixel that isn't visible is overridden with 0
    cx, cy = camera.pos
    appearance = object.visual
    for x in range(cx, cx + object.width):
        for y in range(cy, cy + object.height):
            end = x,y
            if is_pos_visible_from_pos(camera.pos, end):
                appearance[x,y] = 0
    return appearance

def can_camera_see_object(camera, object):
    return not np.all((get_object_appearance(camera, object) == 0))

def send_handshake(sender, receiver):
    pass