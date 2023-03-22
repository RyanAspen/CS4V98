# This is the main script to run a simulation

"""
1) Initialize a graph of cameras
2) c = camera that can see the tracked object
3) For each frame update,
    a) If c cannot see the tracked object, check each camera c2 that recently received a handshake
        i) If c2 can see the tracked object, set c = c2 and break the loop
    b) Record the tracked object's location, velocity, and visual representation
    c) For each neighbor of c as c2,
        i) If the object is in c2's vision range, send a handshake to c2
"""

from environment import Environment
import utils

file_name = None
environment = Environment(file_name)
utils.initialize_vision_ranges(environment)
cameras, objects, tracked_object = environment.cameras, environment.objects, environment.tracked_object

# 2) c = camera that can see the tracked object
c = None
for camera in cameras:
    if utils.can_camera_see_object(camera, tracked_object):
        c = camera
        break

while True:
    if not utils.can_camera_see_object(c, tracked_object):
        pass
    tracked_pos = tracked_object.pos
    tracked_visual = utils.get_object_appearance(c, tracked_object)
    next_pos = utils.get_next_position(tracked_pos)
    for camera in cameras:
        if c.id != camera.id and utils.can_camera_see_camera(c, camera):
            if utils.can_camera_see_object(camera, tracked_object):
                utils.send_handshake(c, camera)
