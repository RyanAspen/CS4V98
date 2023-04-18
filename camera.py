"""

Class to describe a camera. It consists of the following fields:
- Id
- Position
- Vision Range

A camera should have functions to initialize vision ranges from an environment,
determine whether a particular object is visible, get a visible object's position (for depth cameras),
get a visible object's visual appearance, etc.

"""

class Camera:

    def __init__(self, id, x, y):
        self.id = id
        self.pos = self.x, self.y = x, y
        self.vision_range = None
        self.handshake = None # tuple of pos and 1d view 
        
        

    