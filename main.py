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