########################################
#
# Object module for The Practitioner.
#
# Author: John Bullard
#
########################################


class Object:
    """ A object in the game. """
    
    def __init__(self, x, y, name, solid, blocks_sight, always_visible, image, color, inventory = [], explored = False, 
                 interaction = None, living = None, spell = None, item = None):
        """ Initiate object class. """
        
        self.x = x
        self.y = y
        self.name = name
        self.startname = name
        self.solid = solid
        self.blocks_sight = blocks_sight
        self.always_visible = always_visible
        self.image = image
        self.startimage = image
        self.color = color
        self.startcolor = color
        self.inventory = inventory
        self.explored = explored
        self.interaction = interaction
        self.living = living
        self.spell = spell
        self.item = item
        
        
class Living:
    """ Living component to the object class. """
    
    def __init__(self, health, energy, damage, speed, ai, status = 'NORMAL', death_function = None):
        """ Initiate living class. """
        
        self.health = health
        self.energy = energy
        self.damage = damage
        self.speed = speed
        self.ai = ai
        self.status = status
        self.death_function = death_function
        
    def restore_health(self, amount):
        """ Restores some energy. """
        
        self.health[0] += amount
        
        if self.health[0] > self.health[1]:
        
            self.health[0] = self.health[1]
             
    def restore_energy(self, amount):
        """ Restores some energy. """
        
        self.energy[0] += amount
        
        if self.energy[0] > self.energy[1]:
        
            self.energy[0] = self.energy[1]

            
class Spell:
    """ Spell component to the object class. """
    
    def __init__(self, damage, effect, caster, target_x, target_y):
        """ Initiate spell class. """
        
        self.damage = damage
        self.effect = effect
        self.caster = caster
        self.target_x = target_x
        self.target_y = target_y
        
            
class Item:
    """ Item component to the object class. """
    
    def __init__(self, use_function, use_message):
        """ Initiate item class. """
        
        self.use_function = use_function
        self.use_message = use_message
        
        
        
        
