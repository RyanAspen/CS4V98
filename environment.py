"""

An environment is a full description of a 2D map in which the simulation
is ran. It consists of a binary 2D array describing where opaque, unmoving walls
are in the map, a list of camera positions, and a list of objects moving through
the environment.

Because environments are complex, they should be initialized with the load_from_file()
function. The load_from_file() function parses the map file defined by MAP_NAME (see 
environment_format.txt to understand the format of the map file).

"""

import constants
import numpy as np
import pygame
from camera import Camera
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

    
    """
    
    Inputs:
    - file_name -> string of a file within the maps folder

    Output:
    - N/A

    Description:
    This function reads the file described by file_name and
    initializes this environment using the parsed information.

    """
    def load_from_file(self, file_name):
        map_file_path = "maps/" + file_name
        f = open(map_file_path, "r")
        content = f.readlines()
        self.size = self.height, self.width = np.array(content[0].split()).astype(int)
        self.map = np.zeros(self.size)
        i = 0
        for line in content[1:self.height + 1]:
            self.map[i] = np.array(line.split())
            i += 1
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
            
    """
    
    Inputs:
    - screen -> The Pygame window used for display
    - tracking_camera_id -> The id of the camera currently in charge of
    tracking the relevant object
    
    Output:
    - N/A

    Description:
    This function updates screen with visuals of the environment's cameras depending
    on the cameras' handshakes. Cameras have the following colors:
    - red -> the camera currently tracking the object (overrides yellow and green)
    - yellow -> any camera that has a non-empty handshake
    - green -> any camera that has an empty handshake

    This function also draws a yellow dot on screen describing where the tracked object's
    position is predicted to move to next frame. The yellow dot only appears if handshakes are
    being generated.

    """
    def update_handshake_visual(self, screen, tracking_camera_id):
        for camera in self.cameras:
            if camera.id == tracking_camera_id:
                color = (255, 0, 0)
            elif camera.handshake is not None:
                color = (255, 165, 0)
            else:
                color = (0, 255, 0)
            pygame.draw.circle(screen, 
                color, 
                (int((camera.x + 0.5) * constants.SCALE), int((camera.y + 0.5) * constants.SCALE)),
                max(int(constants.SCALE / 2), 3)
            )
            if camera.handshake is not None:
                x,y = camera.handshake[0]
                pygame.draw.circle(screen, 
                    (255, 255, 0), 
                    (int(x * constants.SCALE), int(y * constants.SCALE)),
                    max(int(constants.SCALE / 2), 5)
                )
        for camera in self.cameras:
            if camera.handshake is not None:
                x,y = camera.handshake[0]
                pygame.draw.circle(screen, 
                    (255, 255, 0), 
                    (int(x * constants.SCALE), int(y * constants.SCALE)),
                    max(int(constants.SCALE / 2), 5)
                )

    """
    
    Inputs:
    - screen -> The Pygame window used for display
    - tracking_camera_id -> The id of the camera currently in charge of
    tracking the relevant object
    - tracking_object_id -> The id of the object currently being tracked
    
    Output:
    - N/A

    Description:
    This function progresses the simulation forward by a frame, then it updates 
    screen with visuals describing the state of the map and the environment's objects. 
    The visual colors are as follows:
    - Black -> opaque wall
    - Pink -> visual range of the current tracking camera
    - Blue Outline -> correct object to be tracked
    - Purple Outline -> object currently being tracked (only present if different from correct object to be tracked)

    """
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

        for i in range(len(self.objects)):
            if i == 0:
                self.objects[i].update(screen, True, False)
            elif i == tracking_object_id:
                self.objects[i].update(screen, False, True)
            else:
                self.objects[i].update(screen, False, False)
