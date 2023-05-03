"""

This file contains the high-level algorithm for running a simulation with the handshake
matching algorithm. The pseudocode for the algorithm is as follows:

1) Initialize the vision ranges of each camera
2) c = arbitrary camera that can see the tracked object
3) For each frame update,
    a) If c cannot see the tracked object, check each camera c2 that recently received a handshake
        i) If c2 can see the tracked object, set c = c2 and break the loop
    b) Record the tracked object's location, velocity, and visual representation
    c) For each neighbor of c as c2,
        i) If the object is in c2's vision range, send a handshake to c2

When running this file, a Pygame window should open after a few seconds. If AUTOPLAY is off, you will
need to manually step through frames by clicking on any button while focused on the window.

"""

import constants
import pygame
import sys
import utils
from environment import Environment

# 1) Initialize the vision ranges of each camera
environment = Environment(constants.MAP_NAME)
utils.initialize_vision_ranges(environment)

pygame.init()

window = pygame.display.set_mode((environment.size[1] * constants.SCALE, environment.size[0] * constants.SCALE))
clock = pygame.time.Clock()

# 2) c = arbitrary camera that can see the tracked object
c = None
tracked_object_id = 0
for camera in environment.cameras:
    if utils.can_camera_see_object(camera, environment.objects[tracked_object_id], environment):
        c = camera
        break

# 3) For each frame update,
while True:
    # a) If c cannot see the tracked object, check each camera c2 that recently received a handshake
    if not utils.can_camera_see_object(c, environment.objects[tracked_object_id], environment):
        for camera in environment.cameras:
            # i) If c2 can see the tracked object, set c = c2 and break the loop
            if camera.handshake is not None:
                best_match = utils.get_best_object_match(camera, environment.objects, camera.handshake[0], camera.handshake[1], environment)
                if best_match is not None:
                    c = camera
                    tracked_object_id = best_match.id
                    break
    
    # b) Record the tracked object's location and visual representation
    utils.reset_handshakes(environment.cameras)
    environment.update(window, c.id, tracked_object_id)
    tracked_pos = environment.objects[tracked_object_id].pos
    tracked_visual = utils.get_object_appearance(c, environment.objects[tracked_object_id], environment)

    # c) For each neighbor of c as c2,
    for camera in environment.cameras:
        # i) If the object is in c2's vision range, send a handshake to c2
        if c.id != camera.id and utils.can_camera_see_object(camera, environment.objects[tracked_object_id], environment):
            utils.send_handshake(c, camera, environment.objects[tracked_object_id], environment)

    environment.update_handshake_visual(window, c.id)
    pygame.display.flip()
    clock.tick(constants.FPS)
    
    progress = constants.AUTOPLAY

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    while not progress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                progress = True
                break
        clock.tick(20)
    
