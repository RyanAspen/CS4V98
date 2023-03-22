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

class Environment:

    def __init__(self, file_name = None):
        if file_name is None:
            # Default
            self.size = self.width, self.height = (100, 100)
            self.map = np.zeros(self.size)
            self.objects = list()
            self.cameras = list()
            self.tracked_object = None
        else:
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

    def load_from_file(self, file_name):
        map_file_path = "maps/" + file_name
        f = open(map_file_path, "r")
        content = f.readlines()
        # Map Dimensions
        self.width, self.height = content[0].split()
        self.map = np.zeros(self.size)
        # Map Details
        i = 0
        for line in content[1:self.height + 1]:
            self.map[i] = np.array(line.split())
            i += 1
        
        # Objects
        i = self.height + 1
        objects_length = int(content[i])
        i += 1




        for line in f:
            split = line.split()
            if i == 0:
                self.width = int(split[0])
                self.height = int(split[1])
            
        
