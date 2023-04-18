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


Notes:
- quadtree
- line segment objects
- closest object
"""

import sys
from environment import Environment
import utils
import pygame
import constants

environment = Environment(constants.MAP_NAME)
utils.initialize_vision_ranges(environment)

pygame.init()

window = pygame.display.set_mode((environment.size[1] * constants.SCALE, environment.size[0] * constants.SCALE))
clock = pygame.time.Clock()

# 2) c = camera that can see the tracked object
c = None
for camera in environment.cameras:
    if utils.can_camera_see_object(camera, environment.tracked_object, environment):
        c = camera
        break

while True:
    if not utils.can_camera_see_object(c, environment.tracked_object, environment):
        for camera in environment.cameras:
            if camera.handshake is not None:
                best_match = utils.get_best_object_match(camera, environment.objects, camera.handshake[0], camera.handshake[1], environment)
                if best_match is not None:
                    c = camera
                    environment.tracked_object = best_match
                    break
    
    utils.reset_handshakes(environment.cameras)
    tracked_pos = environment.tracked_object.pos
    tracked_visual = utils.get_object_appearance(c, environment.tracked_object, environment)
    for camera in environment.cameras:
        if c.id != camera.id and utils.can_camera_see_object(camera, environment.tracked_object, environment):
            if utils.can_camera_see_object(camera, environment.tracked_object, environment):
                utils.send_handshake(c, camera, environment.tracked_object, environment)
    environment.update(window, c.id)
    pygame.display.flip()
    clock.tick(20)
    progress = False
    while not progress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                progress = True
                break
        clock.tick(20)
    
