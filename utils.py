"""

This file contains utility methods used elsewhere in the code.

"""

import constants
import copy
import numpy as np
from queue import Queue


"""
    
Inputs:
- start -> starting position as a 2-tuple of (x,y)
- end -> ending position as a 2-tuple of (x,y)
- environment -> the environment containing the start and end positions

Output:
- Boolean value indicating whether start is visible from end (whether there are any opaque tiles between the start and end positions)

Description:
This function determines whether a camera positioned at start can see end. It is a modified version of Bresenham's Line Algorithm, except
that it checks every tile marked by the algorithm to see if it is a wall or not.

"""
def is_pos_visible_from_pos(start, end, environment):

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


"""
    
Inputs:
- environment -> the environment containing the start and end positions

Output:
- N/A

Description:
This function updates the vision ranges of every camera within environment. It uses is_pos_visible_from_pos along with a
Breadth-First Search approach to only test tiles that could feasibly be visible from the camera's position.

"""

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
                
"""
    
Inputs:
- camera -> a camera
- object -> an object
- environment -> the environment containing camera and object

Output:
- 2D array describing the object's visual appearance from the camera's point of view

Description:
This function takes the object's true visual appearance and removes (override to 0) all pixels that aren't visible to the camera

"""
def get_object_appearance(camera, object, environment):
    cx, cy = int(object.pos[0]), int(object.pos[1])
    appearance = copy.deepcopy(object.visual)
    for x in range(cx, cx + object.width):
        for y in range(cy, cy + object.height):
            end = x,y
            if not is_pos_visible_from_pos(camera.pos, end, environment):
                appearance[cx - x, cy - y] = 0
    return appearance

"""
    
Inputs:
- camera -> a camera
- object -> an object
- environment -> the environment containing camera and object

Output:
- Boolean value indicating whether camera can see any part of the object

Description:
This function makes use get_object_appearance and checks if the output has any nonzero value.

"""
def can_camera_see_object(camera, object, environment):
    return not np.all((get_object_appearance(camera, object, environment) == 0))

"""
    
Inputs:
- sender -> the camera sending the handshake
- receiver -> the camera receiving the handshake
- object -> an object
- environment -> the environment containing the cameras and object

Output:
- N/A

Description:
This function creates a handshake given sender's view of object to reciever.

"""
def send_handshake(sender, receiver, object, environment):
    appearance = get_object_appearance(sender, object, environment)
    pos = guess_new_position(object)
    receiver.handshake = pos, appearance

"""
    
Inputs:
- cameras -> a list of all cameras in the environment

Output:
- N/A

Description:
This function sets all cameras to have an empty handshake. This is called to make sure
that cameras don't use outdated handshakes.

"""
def reset_handshakes(cameras):
    for camera in cameras:
        camera.handshake = None

"""
    
Inputs:
- camera -> a camera
- objects -> a list of all objects in the environment
- environment -> the environment containing the camera and objects

Output:
- The object that matches best with the camera's handshake. The output is None if no object is visible to camera
or the camera has an empty handshake.

Description:
This function takes the camera's handshake and uses get_best_object_match() to get the object that best matches it.

"""
def find_object_with_handshake(camera, objects, environment):
    if camera.handshake is not None:
        previous_pos, previous_appearance = camera.handshake
        best_object = get_best_object_match(camera, objects, previous_pos, previous_appearance, environment)
        return best_object
    return None

"""
    
Inputs:
- tracked_object -> an object

Output:
- A 2-tuple of (x,y) describing the most likely position of the tracked_object in the next frame

"""
def guess_new_position(tracked_object):
    prev_x, prev_y = tracked_object.prev_pos
    curr_x, curr_y = tracked_object.pos
    diff_x = curr_x - prev_x
    diff_y = curr_y - prev_y 
    new_pos = (curr_x + diff_x), (curr_y + diff_y)
    return new_pos

"""
    
Inputs:
- camera -> a camera
- object1 -> the object to compare against the handshake
- target_appearance -> the appearance derived from the handshake
- environment -> the environment containing the camera and objects

Output:
- A value corresponding to the difference in size of the bounding boxes around the two objects

"""
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

"""
    
Inputs:
- camera -> a camera
- object1 -> the object to compare against the handshake
- target_appearance -> the appearance derived from the handshake
- environment -> the environment containing the camera and objects

Output:
- A value corresponding to the normalized pixel difference of the appearances around the two objects

"""
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

"""
    
Inputs:
- camera -> a camera
- object -> the object to compare against the handshake
- target_pos -> the position derived from the handshake
- target_appearance -> the appearance derived from the handshake
- environment -> the environment containing the camera and objects
- verbose -> if True, print out difference values

Output:
- A value corresponding to the difference between the given object and handshake.

Description:
The value returned by this algorithm is the weighted average of the position difference, appearance difference,
and size difference as determined by POS_CONST, APPEARANCE_CONST, and SIZE_CONST.

"""
def get_object_match(camera, object, target_pos, target_appearance, environment, verbose = True):
    pos_diff = abs(target_pos[0] - object.pos[0]) + abs(target_pos[1] - object.pos[1])
    appearance_diff = get_appearance_difference(camera, object, target_appearance, environment)
    size_diff = get_size_difference(camera, object, target_appearance, environment)
    if verbose:
        print("Pos Diff =", pos_diff, "Appearance Diff =", appearance_diff, "Size Diff =", size_diff)
    return pos_diff*constants.POS_CONST + appearance_diff*constants.APPEARANCE_CONST + size_diff*constants.SIZE_CONST

"""
    
Inputs:
- camera -> a camera
- objects -> the object to compare against the handshake
- target_pos -> the position derived from the handshake
- target_appearance -> the appearance derived from the handshake
- environment -> the environment containing the camera and objects
- verbose -> if True, print out difference values

Output:
- The object that has the least difference with the handshake object

"""
def get_best_object_match(camera, objects, target_pos, target_appearance, environment, verbose = True):
    best_object = None
    best_match = 100000
    if verbose:
        print("-------------------")
    for object in objects:
        match = get_object_match(camera, object, target_pos, target_appearance, environment, verbose)
        if verbose:
           print("Total match for id ", object.id, "=", match)
        if match < best_match:
            best_object = object
            best_match = match
            if verbose:
                print("New Best match =", best_object.id)
    if verbose:
        print("-------------------")
    return best_object