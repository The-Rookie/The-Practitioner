########################################
#
# Widget module for The Practitioner.
#
# Author: John Bullard
#
########################################


class Button():
    """ A button in the game. """
    
    def __init__(self, x, y, text, color, light_color, click_action):
        """ Initiate button class. """
        
        self.x = x
        self.y = y
        self.width = x+(len(text)/2)+1
        self.height = y+1
        self.text = text
        self.color = color
        self.start_color = color
        self.light_color = light_color
        self.click_action = click_action
        
        # Set type.
        self.type = 'Button'
    
    
    def collision(self, x, y):
        """ Detects collisions with button. """
        
        if x <= self.width and x >= self.x-(len(self.text)/2)-1 and y <= self.height and y >= self.y-1:
        
            return True
        
        return False
        
        
class Input:
    """ A input box in the game. """
    
    def __init__(self, x, y, width, height, text, color, light_color, click_action):
        """ Initiate input class. """
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.start_color = color
        self.light_color = light_color
        self.click_action = click_action
        self.tick = 0
        self.cursor = False
        
        # Set type.
        self.type = 'Input'
        
        
class Checkbox:
    """ A checkbox in the game. """
    
    def __init__(self, x, y, text, color, light_color, click_action, selected = False, group = None):
        """ Initiate checkbox class. """
        
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.start_color = color
        self.light_color = light_color
        self.click_action = click_action
        self.selected = selected
        self.group = group
        
        # Set type.
        self.type = 'Checkbox'
    
    
    def collision(self, x, y):
        """ Detects collisions with checkbox. """
        
        if x <= self.x+7+len(self.text) and x >= self.x+1 and y <= self.y+1 and y >= self.y-1:
            
            return True
        
        return False
    