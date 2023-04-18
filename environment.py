"""

Class to describe an environment. It consists of the following fields:
- Size
- Obstacles / Walls
- Objects
- Cameras

The environment should have an updateFrame function, which updates every object after some time has passed, 
as well as some loadEnvironment function which loads in a file used to initialize.
"""

import numpy as np
import os
import pygame
from camera import Camera
import constants

from object import Object

class Environment:

    def __init__(self, file_name = None):
        self.size = self.width, self.height = (100, 100)
        self.map = np.zeros(self.size)
        self.objects = list()
        self.cameras = list()
        if file_name is not None:
            # Load from file (should always be this case)
            self.load_from_file(file_name)

    def save_to_file(self, file_name):
        map_file_path = "maps/" + file_name
        if os.path.exists(map_file_path):
            os.remove(map_file_path)
        f = open(map_file_path, "x")
        f.write(str(self.width) + " " + str(self.height) + "\n")
        for y in range(self.height):
            s = ""
            for x in range(self.width):
                s += str(int(self.map[x][y])) + " "
            f.write(s + "\n")
        f.write(str(len(self.objects)) + "\n")
        for object in self.objects:
            # Requires 2d array for visual representation and path. First object is tracked
            f.write(str(object.width) + " " + str(object.height))
            for y in range(object.height):
                s = ""
                for x in range(object.width):
                    s += str(int(self.initial_visual[x,y])) + " "
                f.write(s + "\n")
            f.write(str(len(object.initial_path)) + "\n")
            for x, y, speed, orientation in object.initial_path:
                f.write(str(x) + " " + str(y) + " " + str(speed) + " " + str(orientation))

        f.write(str(len(self.cameras)) + "\n")
        for camera in self.cameras:
            # Just requires position
            f.write(str(camera.x) + " " + str(camera.y) + "\n")
        f.close()

    #TODO
    def load_from_file(self, file_name):
        map_file_path = "maps/" + file_name
        f = open(map_file_path, "r")
        content = f.readlines()
        # Map Dimensions
        self.size = self.height, self.width = np.array(content[0].split()).astype(int)
        self.map = np.zeros(self.size)
        # Map Details
        i = 0
        for line in content[1:self.height + 1]:
            self.map[i] = np.array(line.split())
            i += 1
        # Objects
        i = self.height + 1
        self.objects = list()
        objects_length = int(content[i])
        i += 1

        objects_processed = 0
        while objects_processed < objects_length:
            object_width, object_height = np.array(content[i].split()).astype(int)

            i += 1
            initial_visual = np.zeros((object_width, object_height))
            a = 0
            for line in content[i:object_height + i]:
                initial_visual[a] = np.array(content[i].split()).astype(int)
                a += 1
                i += 1
            object_path_length = int(content[i])
            i += 1
            initial_path = list()
            for line in content[i:object_path_length + i]:
                initial_path.append(np.array(content[i].split()).astype(int))
                i += 1
            o = Object(objects_processed, initial_visual, initial_path)
            self.objects.append(o)
            objects_processed += 1

        cameras_length = int(content[i])
        self.cameras = list()
        cameras_processed = 0
        for line in content[i + 1: cameras_length + i + 1]:
            x, y = np.array(line.split()).astype(int)
            self.cameras.append(Camera(cameras_processed, x,y))
            cameras_processed += 1
            
    def update(self, screen, tracking_camera_id, tracking_object_id):
        screen.fill((255, 255, 255))
        for y in range(self.map.shape[0]):
            for x in range(self.map.shape[1]):
                if self.map[y,x] > 0:
                    pygame.draw.rect(
                        screen,
                        (0, 0, 0),
                        (x*constants.SCALE, y*constants.SCALE, constants.SCALE, constants.SCALE)
                    )
                elif self.cameras[tracking_camera_id].vision_range[y,x] == 1:
                    pygame.draw.rect(
                        screen,
                        (255, 114, 118),
                        (x*constants.SCALE, y*constants.SCALE, constants.SCALE, constants.SCALE)
                    )
        for camera in self.cameras:
            if camera.id == tracking_camera_id:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
            pygame.draw.circle(screen, 
                color, 
                (int((camera.x + 0.5) * constants.SCALE), int((camera.y + 0.5) * constants.SCALE)),
                max(int(constants.SCALE / 2), 3)
            )
        for i in range(len(self.objects)):
            if i == 0:
                self.objects[i].update(screen, True, False)
            elif i == tracking_object_id:
                self.objects[i].update(screen, False, True)
            else:
                self.objects[i].update(screen, False, False)
