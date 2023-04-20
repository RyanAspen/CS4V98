"""

Utility methods used by other objects.

"""

import numpy as np
from queue import Queue
import constants
import copy

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
            if environment.map[y, x] > 0:
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
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        D = (2 * dx) - dy
        x = x0

        for y in range(y0, y1 + 1):
            if environment.map[y, x] > 0:
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
            # Error on next line with (8,0)
            if is_pos_on_map(current_position, environment) and camera.vision_range[curr_y, curr_x] == 0 and environment.map[curr_y, curr_x] == 0:
                if is_pos_visible_from_pos(start_position, current_position, environment):                    
                    camera.vision_range[curr_y, curr_x] = 1
                    position_queue.put((curr_x - 1, curr_y - 1))
                    position_queue.put((curr_x, curr_y - 1))
                    position_queue.put((curr_x + 1, curr_y - 1))
                    position_queue.put((curr_x - 1, curr_y))
                    position_queue.put((curr_x + 1, curr_y))
                    position_queue.put((curr_x - 1, curr_y + 1))
                    position_queue.put((curr_x, curr_y + 1))
                    position_queue.put((curr_x + 1, curr_y + 1))
                else:
                    camera.vision_range[curr_y, curr_x] = 2
                
        

def can_camera_see_position(camera, position):
    x, y = int(position[0]), int(position[1])
    return camera.vision_range[x,y] == 1 

def can_camera_see_camera(camera1, camera2):
    c2x, c2y = camera2.pos
    return camera1.vision_range[c2x, c2y] == 1

def get_object_appearance(camera, object, environment):
    # Return an array representing the appearance of the object except every pixel that isn't visible is overridden with 0
    cx, cy = int(object.pos[0]), int(object.pos[1])
    appearance = copy.deepcopy(object.visual)
    for x in range(cx, cx + object.width):
        for y in range(cy, cy + object.height):
            end = x,y
            if not is_pos_visible_from_pos(camera.pos, end, environment):
                appearance[cx - x, cy - y] = 0
    return appearance

def can_camera_see_object(camera, object, environment):
    return not np.all((get_object_appearance(camera, object, environment) == 0))

def send_handshake(sender, receiver, object, environment):
    appearance = get_object_appearance(sender, object, environment)
    pos = guess_new_position(object)
    receiver.handshake = pos, appearance

def reset_handshakes(cameras):
    for camera in cameras:
        camera.handshake = None

def find_object_with_handshake(camera, objects, environment):
    if camera.handshake is not None:
        previous_pos, previous_appearance = camera.handshake
        best_object = get_best_object_match(camera, objects, previous_pos, previous_appearance, environment)
        return best_object
    return None

def guess_new_position(tracked_object):
    if tracked_object.time_until_change == tracked_object.path[tracked_object.path_progress][2]:
        last_path_x = tracked_object.path[tracked_object.path_progress - 1][0]
        last_path_y = tracked_object.path[tracked_object.path_progress - 1][1]
        speed = tracked_object.path[tracked_object.path_progress - 1][2]
        prev_x = tracked_object.x - (tracked_object.x - last_path_x) / speed
        prev_y = tracked_object.y - (tracked_object.y - last_path_y) / speed
    else:
        last_path_x = tracked_object.path[tracked_object.path_progress][0]
        last_path_y = tracked_object.path[tracked_object.path_progress][1]
        speed = tracked_object.path[tracked_object.path_progress][2]
        prev_x = tracked_object.x - (tracked_object.x - last_path_x) / (speed - tracked_object.time_until_change)
        prev_y = tracked_object.y - (tracked_object.y - last_path_y) / (speed - tracked_object.time_until_change)
    prev_pos = prev_x, prev_y
    curr_pos = tracked_object.pos
    diff_x = (curr_pos[0] - prev_pos[0]) / tracked_object.path[tracked_object.path_progress - 1][2]
    diff_y = (curr_pos[1] - prev_pos[1]) / tracked_object.path[tracked_object.path_progress - 1][2]
    new_pos = (curr_pos[0] + diff_x), (curr_pos[1] + diff_y)
    return new_pos

def get_size_difference(camera, object1, target_appearance, environment):
    appearance1 = get_object_appearance(camera, object1, environment)
    appearance2 = target_appearance
    
    # Remove outside zero rows
    extra_rows = np.sum(~appearance2.any(1))
    
    # Remove outside zero columns
    extra_columns = 0
    for i in range(appearance1.shape[1]):
        is_all_zeros = True
        for j in range(appearance1.shape[0]):
            if appearance1[j,i] != 0:
                is_all_zeros = False
                break
        if is_all_zeros:
            extra_columns += 1

    height = appearance1.shape[0] - extra_rows
    width = appearance1.shape[1] - extra_columns
    return abs(height - appearance2.shape[0]) + abs(width - appearance2.shape[1])

def get_appearance_difference(camera, object1, target_appearance, environment):
    appearance1 = get_object_appearance(camera, object1, environment)
    appearance2 = target_appearance
    combined_height = max(appearance1.shape[0], appearance2.shape[0])
    combined_width = max(appearance1.shape[1], appearance2.shape[1])

    def get_pixel(x, y, appearance):
        if y >= appearance.shape[0] or x >= appearance.shape[1]:
            return 0
        return appearance[y][x]

    sum = 0.0
    for y in range(combined_height):
        for x in range(combined_width):
            val1 = get_pixel(x,y, appearance1)
            val2 = get_pixel(x,y, appearance2)
            sum += abs(val2 - val1)
    normalized_sum = sum / (combined_height * combined_width)

    return normalized_sum

def get_object_match(camera, object, target_pos, target_appearance, environment):
    # Use a function to calculate the match between the object and the camera
    pos_diff = abs(target_pos[0] - object.pos[0]) + abs(target_pos[1] - object.pos[1])
    appearance_diff = get_appearance_difference(camera, object, target_appearance, environment)
    size_diff = get_size_difference(camera, object, target_appearance, environment)
    print("Target pos =", target_pos, "Object pos =", object.pos)
    print("Pos Diff =", pos_diff, "Appearance Diff =", appearance_diff, "Size Diff =", size_diff)
    return pos_diff*constants.POS_CONST + appearance_diff*constants.APPEARANCE_CONST + size_diff*constants.SIZE_CONST


def get_best_object_match(camera, objects, target_pos, target_appearance, environment):
    best_object = None
    best_match = 100000
    print("-------------------")
    for object in objects:
        match = get_object_match(camera, object, target_pos, target_appearance, environment)
        print("Total match for id ", object.id, "=", match)
        if match < best_match:
            best_object = object
            best_match = match
            print("New Best match =", best_object.id)
    print("-------------------")
    return best_object