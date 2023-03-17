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

    def __init__(self):
        self.size = self.width, self.height = (100, 100)
        self.map = np.zeros(self.size)
        self.objects = list()
        self.cameras = list()
        self.tracked_object = None

    def save_to_file(self, file_name):
        map_file_path = "maps/" + file_name
        if os.path.exists(map_file_path):
            os.remove(map_file_path)
        f = open(map_file_path, "x")
        f.write(str(self.width) + " " + str(self.height) + "\n")
        for y in range(self.height):
            s = ""
            for x in range(self.width):
                s = s + str(int(self.map[x][y])) + " "
            f.write(s + "\n")
        f.write(str(len(self.objects)) + "\n")
        for object in self.objects:
            pass
        f.write(str(len(self.cameras)) + "\n")
        for camera in self.cameras:
            pass

    def load_from_file(self, file_name):
        pass
