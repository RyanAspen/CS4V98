"""

A camera is defined by a point within an environment that can used to detect objects
within a defined vision range. Depending on the situation, a camera may either have an
empty handshake (None) or a non-empty handshake (tuple of x,y position and object appearance).

Cameras are initialized with load_from_file() in environment.py and initialize_vision_ranges()
in utils.py.

"""

class Camera:

    def __init__(self, id, x, y):
        self.id = id
        self.pos = self.x, self.y = x, y
        self.vision_range = None
        self.handshake = None 
        
        

    