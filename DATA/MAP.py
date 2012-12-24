########################################
#
# Map module for The Practitioner.
#
# Author: John Bullard
#
########################################


class Location:
    """ A location in the game. """

    def __init__(self, id, MAP = None, objects = []):
        """ Initiate location class. """

        self.id = id
        self.objects = objects
        
        
class Room:
    """ A room in the game. """

    def __init__(self, x, y, w, h):
        """ Initiate the room. """

        self.x1 = x
        self.y1 = y
        self.x2 = x + w 
        self.y2 = y + h

    def center(self):
        """ Gets center coords of room. """
        
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) /2

        return (center_x, center_y)

    def intersect(self, other):
        """ Checks for intersects with other rooms. """

        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
