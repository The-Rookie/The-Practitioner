########################################
#
# Data module for The Practitioner.
#
# Author: John Bullard
#
########################################


#############################################
# Imports.
#############################################

import libtcodpy as lib
import os

# Tile data.
tile_data = {}

# Descriptions data.
descriptions_data = {}

# Item data.
item_data = {}

# NPC data.
npc_data = {}

# Spell data.
spell_data = {}

# Race data.
race_data = {}

# History data.
history_data = {}

# Gender data.
gender_data = {}

# Names data.
name_data = {}

# Player data.
player_data = {}

# Config data.
config_data = {}


#############################################
# Parser/Listener.
#############################################

CURRENT_PROPERTIES = []

class Listener:
    """ Grabs values from parser. """
    
    def new_struct(self, struct, name):
        """ Grabs all scructs. """

        return True
        
    def new_flag(self, name):
        """ Grabs all flags. """
        
        print 'new flag named ', name
        return True
        
    def new_property(self,name, typ, value):
        """ Grabs all properties. """
        
        type_names = ['NONE', 'BOOL', 'CHAR', 'INT', 'FLOAT', 'STRING',
                      'COLOR', 'DICE']
        
        if typ == lib.TYPE_COLOR :
            print 'new property named ', name,' type ',type_names[typ], ' value ', value.r, value.g, value.b
            
        elif typ == lib.TYPE_DICE :
            print 'new property named ', name,' type ',type_names[typ], ' value ', value.nb_rolls, value.nb_faces, value.multiplier, value.addsub
            
        else:
            
            # Add property to properties list.
            CURRENT_PROPERTIES.append({name:value})
            
        return True
        
    def end_struct(self, struct, name):
        """ End of struct, adds data to appropriate dictionary. """
        
        global CURRENT_PROPERTIES
        
        # If struct name is 'tile'.
        if lib.struct_get_name(struct) == 'tile':
            
            # Create dictionary.
            tile_data[name] = {}
            
            # Add properties to dictionary.
            for i in range(len(CURRENT_PROPERTIES)):
            
                keys = CURRENT_PROPERTIES[i].keys()
                values = CURRENT_PROPERTIES[i].values()
                
                for key in keys:
                    
                    for value in values:
                        
                        tile_data[name][key] = value
        
        # If struct name is 'item'.
        elif lib.struct_get_name(struct) == 'item':
            
            # Create dictionary.
            item_data[name] = {}
            
            # Add properties to dictionary.
            for i in range(len(CURRENT_PROPERTIES)):
            
                keys = CURRENT_PROPERTIES[i].keys()
                values = CURRENT_PROPERTIES[i].values()
                
                for key in keys:
                    
                    for value in values:
                        
                        item_data[name][key] = value
        
        # If struct name is 'npc'.
        elif lib.struct_get_name(struct) == 'npc':
            
            # Create dictionary.
            npc_data[name] = {}
            
            # Add properties to dictionary.
            for i in range(len(CURRENT_PROPERTIES)):
            
                keys = CURRENT_PROPERTIES[i].keys()
                values = CURRENT_PROPERTIES[i].values()
                
                for key in keys:
                    
                    for value in values:
                        
                        npc_data[name][key] = value
        
        # If struct name is 'spell'.
        elif lib.struct_get_name(struct) == 'spell':
            
            # Create dictionary.
            spell_data[name] = {}
            
            # Add properties to dictionary.
            for i in range(len(CURRENT_PROPERTIES)):
            
                keys = CURRENT_PROPERTIES[i].keys()
                values = CURRENT_PROPERTIES[i].values()
                
                for key in keys:
                    
                    for value in values:
                        
                        spell_data[name][key] = value
                        
        # If struct name is 'race'.
        elif lib.struct_get_name(struct) == 'race':
            
            # Create dictionary.
            race_data[name] = {}
            
            # Add properties to dictionary.
            for i in range(len(CURRENT_PROPERTIES)):
            
                keys = CURRENT_PROPERTIES[i].keys()
                values = CURRENT_PROPERTIES[i].values()
                
                for key in keys:
                    
                    for value in values:
                        
                        race_data[name][key] = value
                        
        # If struct name is 'history'.
        elif lib.struct_get_name(struct) == 'history':
            
            # Create dictionary.
            history_data[name] = {}
            
            # Add properties to dictionary.
            for i in range(len(CURRENT_PROPERTIES)):
            
                keys = CURRENT_PROPERTIES[i].keys()
                values = CURRENT_PROPERTIES[i].values()
                
                for key in keys:
                    
                    for value in values:
                        
                        history_data[name][key] = value
                        
        # If struct name is 'gender'.
        elif lib.struct_get_name(struct) == 'gender':
            
            # Create dictionary.
            gender_data[name] = {}
            
            # Add properties to dictionary.
            for i in range(len(CURRENT_PROPERTIES)):
            
                keys = CURRENT_PROPERTIES[i].keys()
                values = CURRENT_PROPERTIES[i].values()
                
                for key in keys:
                    
                    for value in values:
                        
                        gender_data[name][key] = value
        
        # If struct name is 'names'.
        elif lib.struct_get_name(struct) == 'names':
            
            # Create dictionary.
            name_data[name] = {}
            
            # Add properties to dictionary.
            for i in range(len(CURRENT_PROPERTIES)):
            
                keys = CURRENT_PROPERTIES[i].keys()
                values = CURRENT_PROPERTIES[i].values()
                
                for key in keys:
                    
                    for value in values:
                        
                        name_data[name][key] = value
        
        # If struct name is 'player'.
        elif lib.struct_get_name(struct) == 'player':
            
            # Create dictionary.
            player_data[name] = {}
            
            # Add properties to dictionary.
            for i in range(len(CURRENT_PROPERTIES)):
            
                keys = CURRENT_PROPERTIES[i].keys()
                values = CURRENT_PROPERTIES[i].values()
                
                for key in keys:
                    
                    for value in values:
                        
                        player_data[name][key] = value
                        
        # If struct name is 'gui'.
        if lib.struct_get_name(struct) == 'gui' or lib.struct_get_name(struct) == 'key' or lib.struct_get_name(struct) == 'setting':
            
            # Create dictionary.
            config_data[name] = {}
            
            # Add properties to dictionary.
            for i in range(len(CURRENT_PROPERTIES)):
            
                keys = CURRENT_PROPERTIES[i].keys()
                values = CURRENT_PROPERTIES[i].values()
                
                for key in keys:
                    
                    for value in values:
                        
                        config_data[name][key] = value
        
        CURRENT_PROPERTIES = []
        
        return True
        
    def error(self,msg):
        """ Reads out errors. """
        
        print 'error : ', msg
        return True
  
  
#############################################
# Data parser.
#############################################


# Create parser.
parser = lib.parser_new()

# Create structs
tile_type_struct = lib.parser_new_struct(parser, 'tile')
item_type_struct = lib.parser_new_struct(parser, 'item')
npc_type_struct = lib.parser_new_struct(parser, 'npc')
spell_type_struct = lib.parser_new_struct(parser, 'spell')
race_type_struct = lib.parser_new_struct(parser, 'race')
history_type_struct = lib.parser_new_struct(parser, 'history')
gender_type_struct = lib.parser_new_struct(parser, 'gender')
names_type_struct = lib.parser_new_struct(parser, 'names')
player_type_struct = lib.parser_new_struct(parser, 'player')

# Add flags.
lib.struct_add_flag(tile_type_struct, 'abstract')

# Add properties.
# Tile properties.
lib.struct_add_property(tile_type_struct, 'IMAGE', lib.TYPE_CHAR, True)
lib.struct_add_property(tile_type_struct, 'SOLID', lib.TYPE_BOOL, True)
lib.struct_add_property(tile_type_struct, 'BLOCKS_SIGHT', lib.TYPE_BOOL, True)
lib.struct_add_property(tile_type_struct, 'ALWAYS_VISIBLE', lib.TYPE_BOOL, True)
lib.struct_add_property(tile_type_struct, 'COLOR', lib.TYPE_STRING, True)
lib.struct_add_property(tile_type_struct, 'DESCRIPTION', lib.TYPE_STRING, True)

# Item properties.
lib.struct_add_property(item_type_struct, 'IMAGE', lib.TYPE_CHAR, True)
lib.struct_add_property(item_type_struct, 'SOLID', lib.TYPE_BOOL, True)
lib.struct_add_property(item_type_struct, 'BLOCKS_SIGHT', lib.TYPE_BOOL, True)
lib.struct_add_property(item_type_struct, 'ALWAYS_VISIBLE', lib.TYPE_BOOL, True)
lib.struct_add_property(item_type_struct, 'COLOR', lib.TYPE_STRING, True)
lib.struct_add_property(item_type_struct, 'INTERACTION', lib.TYPE_STRING, True)
lib.struct_add_property(item_type_struct, 'USE', lib.TYPE_STRING, True)
lib.struct_add_property(item_type_struct, 'USE_MESSAGE', lib.TYPE_STRING, True)
lib.struct_add_property(item_type_struct, 'DESCRIPTION', lib.TYPE_STRING, True)

# NPC properties.
lib.struct_add_property(npc_type_struct, 'IMAGE', lib.TYPE_CHAR, True)
lib.struct_add_property(npc_type_struct, 'SOLID', lib.TYPE_BOOL, True)
lib.struct_add_property(npc_type_struct, 'BLOCKS_SIGHT', lib.TYPE_BOOL, True)
lib.struct_add_property(npc_type_struct, 'ALWAYS_VISIBLE', lib.TYPE_BOOL, True)
lib.struct_add_property(npc_type_struct, 'COLOR', lib.TYPE_STRING, True)
lib.struct_add_property(npc_type_struct, 'HEALTH', lib.TYPE_INT, True)
lib.struct_add_property(npc_type_struct, 'ENERGY', lib.TYPE_INT, True)
lib.struct_add_property(npc_type_struct, 'DAMAGE', lib.TYPE_INT, True)
lib.struct_add_property(npc_type_struct, 'SPEED', lib.TYPE_INT, True)
lib.struct_add_property(npc_type_struct, 'AI', lib.TYPE_STRING, True)
lib.struct_add_property(npc_type_struct, 'STATUS', lib.TYPE_STRING, True)
lib.struct_add_property(npc_type_struct, 'DEATH_FUNCTION', lib.TYPE_STRING, True)
lib.struct_add_property(npc_type_struct, 'DESCRIPTION', lib.TYPE_STRING, True)

# Spell properties.
lib.struct_add_property(spell_type_struct, 'IMAGE', lib.TYPE_CHAR, True)
lib.struct_add_property(spell_type_struct, 'COLOR', lib.TYPE_STRING, True)
lib.struct_add_property(spell_type_struct, 'DAMAGE', lib.TYPE_INT, True)
lib.struct_add_property(spell_type_struct, 'EFFECT', lib.TYPE_STRING, True)
lib.struct_add_property(spell_type_struct, 'ENERGYCOST', lib.TYPE_INT, True)
lib.struct_add_property(spell_type_struct, 'USE_MESSAGE', lib.TYPE_STRING, True)
lib.struct_add_property(spell_type_struct, 'DESCRIPTION', lib.TYPE_STRING, True)

# Race properties.
lib.struct_add_property(race_type_struct, 'DESCRIPTION', lib.TYPE_STRING, True)

# History properties.
lib.struct_add_property(history_type_struct, 'DESCRIPTION', lib.TYPE_STRING, True)

# Gender properties.
lib.struct_add_property(gender_type_struct, 'DESCRIPTION', lib.TYPE_STRING, True)

# Name properties.
lib.struct_add_list_property(names_type_struct, "NAMES", lib.TYPE_STRING, True)

# Player properties.
lib.struct_add_property(player_type_struct, 'IMAGE', lib.TYPE_CHAR, True)
lib.struct_add_property(player_type_struct, 'SOLID', lib.TYPE_BOOL, True)
lib.struct_add_property(player_type_struct, 'BLOCKS_SIGHT', lib.TYPE_BOOL, True)
lib.struct_add_property(player_type_struct, 'ALWAYS_VISIBLE', lib.TYPE_BOOL, True)
lib.struct_add_property(player_type_struct, 'COLOR', lib.TYPE_STRING, True)
lib.struct_add_property(player_type_struct, 'DESCRIPTION', lib.TYPE_STRING, True)

# Run parser.
lib.parser_run(parser, 'DATA/data.txt', Listener())

# Delete parser.
lib.parser_delete(parser)

# Grab all descriptions and place them in descriptions_data.
for key in tile_data.keys():
    
    descriptions_data[key] = tile_data[key]['DESCRIPTION']

for key in item_data.keys():
    
    descriptions_data[key] = item_data[key]['DESCRIPTION']

for key in npc_data.keys():
    
    descriptions_data[key] = npc_data[key]['DESCRIPTION']

for key in spell_data.keys():
    
    descriptions_data[key] = spell_data[key]['DESCRIPTION']
    
for key in player_data.keys():
    
    descriptions_data[key] = player_data[key]['DESCRIPTION']
   
   
#############################################
# Config parser.
#############################################


# Create parser.
parser = lib.parser_new()

# Create structs
gui_type_struct = lib.parser_new_struct(parser, 'gui')
hotkey_type_struct = lib.parser_new_struct(parser, 'key')
setting_type_struct = lib.parser_new_struct(parser, 'setting')

# Add flags.
lib.struct_add_flag(gui_type_struct, 'abstract')

# Add properties.
lib.struct_add_property(gui_type_struct, 'FONT', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'FONT_TYPE', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'FONT_LAYOUT', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'COLOR', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'NORMAL_COLOR', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'LIGHT_COLOR', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'NORMAL', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'GOOD', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'WARNING', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'HEALTH_FRONT', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'HEALTH_BACK', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'ENERGY_FRONT', lib.TYPE_STRING, False)
lib.struct_add_property(gui_type_struct, 'ENERGY_BACK', lib.TYPE_STRING, False)
lib.struct_add_property(hotkey_type_struct, 'KEY', lib.TYPE_STRING, False)
lib.struct_add_property(setting_type_struct, 'AMOUNT', lib.TYPE_INT, False)


# Run parser.
lib.parser_run(parser, 'DATA/config.txt', Listener())

# Delete parser.
lib.parser_delete(parser)