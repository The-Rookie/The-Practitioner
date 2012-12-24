########################################
#
# Title: The Practitioner
#
# Genre: Roguelike
#
# Author: John Bullard
#
# Created: 9/18/2012
#
# Build: 2 (Started 10/31/2012)
#
########################################


#############################################
# Imports.
#############################################

import DATA.libtcodpy as lib
import DATA.Widget as Widget
import DATA.Object as Object
import DATA.MAP as Map
import DATA.DATA as DATA
import textwrap, math


#############################################
# Global varaibles.
#############################################

# Load data.
PLAYER_DATA = DATA.player_data
NPC_DATA = DATA.npc_data
SPELL_DATA = DATA.spell_data
ITEM_DATA = DATA.item_data
TILE_DATA = DATA.tile_data
DESCRIPTION_DATA = DATA.descriptions_data
CONFIG_DATA = DATA.config_data
RACE_DATA = DATA.race_data
HISTORY_DATA = DATA.history_data
GENDER_DATA = DATA.gender_data
NAME_DATA = DATA.name_data

# Screen size.
SCREEN_W = 112
SCREEN_H = 56

# Map creation variables.
MAP_W = SCREEN_W
MAP_H = 41
ROOM_MIN_SIZE = CONFIG_DATA['ROOM_MIN_SIZE']['AMOUNT']
ROOM_MAX_SIZE = CONFIG_DATA['ROOM_MAX_SIZE']['AMOUNT']
MAX_ROOMS = CONFIG_DATA['MAX_ROOMS']['AMOUNT']

# FOV variables.
FOV_ALGO = 0  
FOV_LIGHT_WALLS = True
TORCH_RADIUS = CONFIG_DATA['TORCH_RADIUS']['AMOUNT']

# GUI.
# Side Panel.
SIDE_PANEL_W = 32
SIDE_PANEL_X = SCREEN_W - SIDE_PANEL_W

# Message panel.
MSG_PANEL_H = 15
MSG_PANEL_Y = SCREEN_H - MSG_PANEL_H
MSG_X = 1
MSG_PANEL_W = SCREEN_W - SIDE_PANEL_W
MSG_H = MSG_PANEL_H - 2

# Health bar width.
BAR_W = 15

# FPS limit.
FPS_LIMIT = CONFIG_DATA['FPS']['AMOUNT']

# Set quick slots, current slot and mouse varibles.
QUICK_SLOT = {1:'', 2:'', 3:''}
CURRENT_SLOT = 1
LEFT_MOUSE_ACTION = 'MOVE'


#############################################
# Map creation functions.
#############################################


def is_blocked(x, y):
    """ Tests if object or tile is blocked. """

    # Check for solid objects and return true if found.
    for obj in objects_list:

        if obj.solid and obj.x == x and obj.y == y:

            return True
        
        elif obj.living and obj.x == x and obj.y == y:
            
            return True

    # Return false if not blocked.
    return False


def create_room(room):
    """ Creates a new room on the map. """

    # Go through objects and make them unblocked.
    for x in range(room.x1 + 1, room.x2):

        for y in range(room.y1 + 1, room.y2):
        
            for obj in objects_list:
                
                if obj.x == x and obj.y == y and obj != player:
                    
                    # Unblock object.
                    obj.solid = False
                    obj.blocks_sight = False
                    
                    # Set color, image and name.
                    obj.color = eval(TILE_DATA['Dirt Floor']['COLOR'])
                    obj.startcolor = obj.color[0]
                    obj.image = '.'
                    obj.name = 'Dirt Floor'

                    
def create_h_tunnel(x1, x2, y):
    """ Creates a horizontal tunnel to a room. """

    # Carve out tunnel to room.
    for x in range(min(x1, x2), max(x1, x2) + 1):
    
        for obj in objects_list:
            
            if obj.x == x and obj.y == y and obj != player:
                
                # Unblock object.
                obj.solid = False
                obj.blocks_sight = False
                
                # Set color, image and name.
                obj.color = eval(TILE_DATA['Dirt Floor']['COLOR'])
                obj.startcolor = obj.color[0]
                obj.image = '.'
                obj.name = 'Dirt Floor'

                
def create_v_tunnel(y1, y2, x):
    """ Creates a vertical tunnel to a room. """

    # Carve out tunnel to room.
    for y in range(min(y1, y2), max(y1, y2) + 1):

        for obj in objects_list:
            
            if obj.x == x and obj.y == y and obj != player:
                
                # Unblock object.
                obj.solid = False
                obj.blocks_sight = False
                
                # Set color, image and name.
                obj.color = eval(TILE_DATA['Dirt Floor']['COLOR'])
                obj.startcolor = obj.color[0]
                obj.image = '.'
                obj.name = 'Dirt Floor'


def place_objects(node):
    """ Places objects in level. """
    
    global flooded
    
    x, y = node
    
    if is_blocked(x, y) or (x, y) in flooded:
        
        return
    
    flooded.append((x, y))
    
    # Place NPC.
    if lib.random_get_int(0, 1, 100) == 1:
            
        # Choose random NPC.
        strings = NPC_DATA.keys()
        choice = strings[lib.random_get_int(0, 0, len(strings)-1)]
        
        # Create living component.
        living_component = Object.Living(health = [NPC_DATA[choice]['HEALTH'], NPC_DATA[choice]['HEALTH']], energy = [NPC_DATA[choice]['ENERGY'], NPC_DATA[choice]['ENERGY']],
                                         damage = NPC_DATA[choice]['DAMAGE'], speed = NPC_DATA[choice]['SPEED'], ai = NPC_DATA[choice]['AI'], status = NPC_DATA[choice]['STATUS'],
                                         death_function = NPC_DATA[choice]['DEATH_FUNCTION'])
        
        # Create NPC.
        npc = Object.Object(x, y, choice, NPC_DATA[choice]['SOLID'], NPC_DATA[choice]['BLOCKS_SIGHT'], NPC_DATA[choice]['ALWAYS_VISIBLE'],
                            NPC_DATA[choice]['IMAGE'], eval(NPC_DATA[choice]['COLOR']), living = living_component)
        
        if npc.name == 'Vampire':
            
            # Choose random gender.
            gender = GENDER_DATA.keys()[lib.random_get_int(0, 0, len(GENDER_DATA.keys())-1)]
            
            # Choose random name.
            npc.name = get_random_name(gender)
            npc.image = '@'
            npc.color = [lib.yellow, lib.yellow]
        
        elif npc.name == 'Mimic':
        
            # Choose random item.
            strings = ITEM_DATA.keys()
            choice = strings[lib.random_get_int(0, 0, len(strings)-1)]
            
            npc.name = choice
            npc.image = ITEM_DATA[choice]['IMAGE']
            npc.color = eval(ITEM_DATA[choice]['COLOR'])

        objects_list.append(npc)
        
    # Place item.
    elif lib.random_get_int(0, 1, 100) == 1:
            
        # Choose random item.
        strings = ITEM_DATA.keys()
        choice = strings[lib.random_get_int(0, 0, len(strings)-1)]

        # Create item component.
        item_component = Object.Item(use_function = ITEM_DATA[choice]['USE'], use_message = ITEM_DATA[choice]['USE_MESSAGE'])

        # Create item.
        item = Object.Object(x, y, choice, ITEM_DATA[choice]['SOLID'], ITEM_DATA[choice]['BLOCKS_SIGHT'], ITEM_DATA[choice]['ALWAYS_VISIBLE'],
                             ITEM_DATA[choice]['IMAGE'], eval(ITEM_DATA[choice]['COLOR']), interaction = ITEM_DATA[choice]['INTERACTION'], item = item_component)

        objects_list.append(item)
        
    place_objects((x+1, y))
    place_objects((x, y+1))
    place_objects((x-1, y))
    place_objects((x, y-1))
    place_objects((x+1, y+1))
    place_objects((x-1, y+1))
    place_objects((x-1, y-1))
    place_objects((x+1, y-1))

    return

    
def create_map():
    """ Creates an area in the game. """
    
    # Set globals.
    global objects_list, flooded, stairsup, stairsdown
    
    # Object container.
    objects_list = [player]
    
    # Fill map with blocked tiles.
    for y in range(MAP_H):
        
        for x in range(MAP_W):
            
            objects_list.append(Object.Object(x = x, y = y, name = 'Stone Wall', solid = TILE_DATA['Stone Wall']['SOLID'], 
                                blocks_sight = TILE_DATA['Stone Wall']['BLOCKS_SIGHT'], always_visible = TILE_DATA['Stone Wall']['ALWAYS_VISIBLE'], 
                                image = TILE_DATA['Stone Wall']['IMAGE'], color = eval(TILE_DATA['Stone Wall']['COLOR'])))
    
    # Room container.
    rooms = []
    
    # Reset room count.
    num_rooms = 0
    
    # Create rooms until max number of rooms is reached.
    for r in range(MAX_ROOMS+1):
        
        # Get random width and height for room.
        w = lib.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = lib.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)

        # Get random position for room.
        x = lib.random_get_int(0, 0, MAP_W - w - 1)
        y = lib.random_get_int(0, 3, MAP_H - h - 1)
        
        # Create new room.
        new_room = Map.Room(x, y, w, h)
        
        # Check for intersects between rooms.
        failed = False
        for other_room in rooms:

            if new_room.intersect(other_room):

                failed = True
                break
        
        # If no intersects are detected, create room.
        if not failed:
        
            # Create new room.
            create_room(new_room)

            # Grab center room coords.
            (new_x, new_y) = new_room.center()
            
            # If this is not the first room.
            if num_rooms != 0:

                # Get center coords of previous room.
                (prev_x, prev_y) = rooms[num_rooms-1].center()

                # Flip a coin to determine hallway path.
                if lib.random_get_int(0, 0, 1) == 1:

                    # Move horizontal first, then vertical.
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)

                else:

                    # Move vertical first, then horizontal.
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)
            
            # Append the new room to list.
            rooms.append(new_room)
            num_rooms += 1
    
    # Grab first room center coords.
    first_x, first_y = rooms[0].center()
    
    # Move player to center of first room.
    player.x = first_x
    player.y = first_y
                
    # Grab last room center coords.
    last_x, last_y = rooms[num_rooms-1].center()
    
    # Place stairs.
    stairsdown = Object.Object(x = last_x, y = last_y, name = 'Stairs Down', solid = TILE_DATA['Stairs Down']['SOLID'], 
                               blocks_sight = TILE_DATA['Stairs Down']['BLOCKS_SIGHT'], always_visible = TILE_DATA['Stairs Down']['ALWAYS_VISIBLE'], 
                               image = TILE_DATA['Stairs Down']['IMAGE'], color = eval(TILE_DATA['Stairs Down']['COLOR']))
    objects_list.append(stairsdown)
    
    if depth != 1:
                
        stairsup = Object.Object(x = first_x+1, y = first_y+1, name = 'Stairs Up', solid = TILE_DATA['Stairs Up']['SOLID'], 
                                 blocks_sight = TILE_DATA['Stairs Up']['BLOCKS_SIGHT'], always_visible = TILE_DATA['Stairs Up']['ALWAYS_VISIBLE'], 
                                 image = TILE_DATA['Stairs Up']['IMAGE'], color = eval(TILE_DATA['Stairs Up']['COLOR']))
        objects_list.append(stairsup)
                
    # Place objects.
    flooded = []
    place_objects((player.x+1, player.y+1))
    
    # Send all NPCs to front of list for rendering.
    for obj in objects_list:
        
        if obj.living:
            
            send_to_front(obj)
    
    # Save location.
    location = Map.Location(id = depth, objects = objects_list)
    locations_list.append(location)

    
#############################################
# Rendering functions.
#############################################


def clear_objects():
    """ Clears objects at their last position. """
    
    for obj in objects_list:
        
        if lib.map_is_in_fov(fov_map, obj.x, obj.y):

            lib.console_put_char(con, obj.x, obj.y, ' ', lib.BKGND_NONE)
            
            
def render_objects():
    """ Renders all objects. """
    
    # Render objects.
    for obj in objects_list:
        
        mouse = lib.mouse_get_status()
        
        if lib.map_is_in_fov(fov_map, obj.x, obj.y):
            
            if obj.x == mouse.cx and obj.y == mouse.cy:
            
                lib.console_put_char_ex(con, obj.x, obj.y, obj.image, obj.color[0], eval(CONFIG_DATA['SELECTED']['COLOR']))
            
            else:
            
                lib.console_put_char_ex(con, obj.x, obj.y, obj.image, obj.color[0], None)
                
            obj.explored = True
            
        else:
            
            if obj.explored == True and obj.always_visible == True:
                
                if obj.x == mouse.cx and obj.y == mouse.cy:
                    
                    lib.console_put_char_ex(con, obj.x, obj.y, obj.image, obj.color[0], eval(CONFIG_DATA['SELECTED']['COLOR']))
                
                else:
                    
                    lib.console_put_char_ex(con, obj.x, obj.y, obj.image, obj.color[1], None)
    
    # Render player.
    lib.console_set_default_foreground(con, player.color[0])
    lib.console_put_char(con, player.x, player.y, player.image, lib.BKGND_NONE)


def render_widgets(widgets_list):
    """ Renders all widgets. """
    
    for widget in widgets_list:
            
        if widget.type == 'Button':
            
            lib.console_set_default_foreground(0, widget.color)
            lib.console_print_ex(0, widget.x, widget.y, lib.BKGND_NONE, lib.CENTER, widget.text)
            
            for i in range(3):
                
                if str(i+1)+':' == widget.text:
                
                    lib.console_print_ex(0, widget.x+len(widget.text)-1, widget.y, lib.BKGND_NONE, lib.LEFT, QUICK_SLOT[i+1])
                    
        elif widget.type == 'Input':
                
            create_border(widget.width, widget.height, widget.color, 0, widget.x, widget.y, widget.x, widget.y)
            lib.console_set_default_foreground(0, widget.color)
            lib.console_print_ex(0, widget.x+1, widget.y+1, lib.BKGND_NONE, lib.LEFT, widget.text)
            if widget.tick == 40: 
                if widget.cursor == False:
                    widget.cursor = True
                else:
                    widget.cursor = False
                widget.tick = 0
            else:
                widget.tick += 1
            if widget.cursor == True:
                lib.console_print_ex(0, widget.x+1+len(widget.text), widget.y+1, lib.BKGND_NONE, lib.LEFT, chr(179))
            
        elif widget.type == 'Checkbox':
                
            lib.console_set_default_foreground(0, widget.color)
            lib.console_print_ex(0, widget.x+2, widget.y, lib.BKGND_NONE, lib.LEFT, '(')
            if widget.selected == True:
                lib.console_print_ex(0, widget.x+3, widget.y, lib.BKGND_NONE, lib.LEFT, 'X')
            lib.console_print_ex(0, widget.x+4, widget.y, lib.BKGND_NONE, lib.LEFT, ')')
            lib.console_print_ex(0, widget.x+6, widget.y, lib.BKGND_NONE, lib.LEFT, widget.text)
            
  
def render_gui(menu_open = False):
    """ Renders gui elements. """
    
    # Player health, energy.
    draw_bar(0, 1, 1, BAR_W, player.living.health[0], player.living.health[1], eval(CONFIG_DATA['BAR']['HEALTH_FRONT']), eval(CONFIG_DATA['BAR']['HEALTH_BACK']))
    draw_bar(0, BAR_W+2, 1, BAR_W, player.living.energy[0], player.living.energy[1], eval(CONFIG_DATA['BAR']['ENERGY_FRONT']), eval(CONFIG_DATA['BAR']['ENERGY_BACK']))
    
    # Clear side_panel console.
    lib.console_clear(side_panel)
    
    # Targets.
    targets_list = mouse_get_targets()
    if len(targets_list) > 0:
        
        for target in targets_list:
            
            # Display target's name, bars and description if in FOV and a object.
            if menu_open == False and target in objects_list:
                
                if target.living is not None and target.living.ai is not None:
                    
                    if target.living.status != 'DISGUISED':
                    
                        draw_bar(side_panel, 0, 2, BAR_W, target.living.health[0], target.living.health[1], eval(CONFIG_DATA['BAR']['HEALTH_FRONT']), eval(CONFIG_DATA['BAR']['HEALTH_BACK']))
                        draw_bar(side_panel, BAR_W+1, 2, BAR_W, player.living.energy[0], player.living.energy[1], eval(CONFIG_DATA['BAR']['ENERGY_FRONT']), eval(CONFIG_DATA['BAR']['ENERGY_BACK']))
                    
                        lib.console_set_default_background(side_panel, lib.black)
                
                lib.console_set_default_foreground(side_panel, eval(CONFIG_DATA['TEXT']['COLOR']))
                lib.console_print_ex(side_panel, SIDE_PANEL_W/2-1, 0, lib.BKGND_NONE, lib.CENTER, targets_list[0].name)
                
                if targets_list[0].name in DESCRIPTION_DATA:
                
                    text = textwrap.wrap(DESCRIPTION_DATA[targets_list[0].name], SIDE_PANEL_W-1)
                    
                    if targets_list[0].living is not None:
                    
                        y = 4
                        
                    else:
                        
                        y = 3
                        
                    for line in text:
                    
                        lib.console_print_ex(side_panel, 0, y, lib.BKGND_NONE, lib.LEFT, line)
                        y += 1
            
            # Display target's name and description if a widget.
            elif target in widgets_list:
                
                if target.text in DESCRIPTION_DATA:
                
                    lib.console_set_default_foreground(side_panel, eval(CONFIG_DATA['TEXT']['COLOR']))
                    lib.console_print_ex(side_panel, SIDE_PANEL_W/2-1, 0, lib.BKGND_NONE, lib.CENTER, target.text)
                    text = textwrap.wrap(DESCRIPTION_DATA[target.text], SIDE_PANEL_W-1)
                    y = 4
                    for line in text:
                    
                        lib.console_print_ex(side_panel, 0, y, lib.BKGND_NONE, lib.LEFT, line)
                        y += 1
                
                else:
                    
                    for i in range(3):
                    
                        if str(i+1)+':' == target.text and QUICK_SLOT[i+1] in DESCRIPTION_DATA:
                    
                            lib.console_set_default_foreground(side_panel, eval(CONFIG_DATA['TEXT']['COLOR']))
                            lib.console_print_ex(side_panel, SIDE_PANEL_W/2-1, 0, lib.BKGND_NONE, lib.CENTER, QUICK_SLOT[i+1])
                            text = textwrap.wrap(DESCRIPTION_DATA[QUICK_SLOT[i+1]], SIDE_PANEL_W-1)
                            y = 4
                            for line in text:
                    
                                lib.console_print_ex(side_panel, 0, y, lib.BKGND_NONE, lib.LEFT, line)
                                y += 1
    
    # Blit contents of side_panel console to root console.
    lib.console_blit(side_panel, 0, 0, SIDE_PANEL_W, MSG_PANEL_H, 0, SIDE_PANEL_X, MSG_PANEL_Y)
    
    # Render widgets.
    render_widgets(widgets_list)
        
    # Message panel.
    # Clear panel.
    lib.console_set_default_background(msg_panel, lib.black)
    lib.console_clear(msg_panel)
    
    # Display messages.
    y = 1
    for (line, color) in game_msgs:

        lib.console_set_default_foreground(msg_panel, color)
        lib.console_print_ex(msg_panel, MSG_X, y, lib.BKGND_NONE, lib.LEFT, line)
        y += 1
    
    # Blit contents of msg_panel console to root console.
    lib.console_blit(msg_panel, 0, 0, MSG_PANEL_W, MSG_PANEL_H, 0, 0, MSG_PANEL_Y)

        
def draw_bar(console, x, y, total_width, value, maximum, bar_color, back_color):
    """ Draws a bar. """

    # Calculate the width of the bar.
    bar_width = int(float(value) / maximum * total_width)

    # Draw background.
    lib.console_set_default_background(console, back_color)
    lib.console_rect(console, x, y, total_width, 1, False, lib.BKGND_SET)

    # Draw bar on top.
    lib.console_set_default_background(console, bar_color)

    # Make sure width is greater than 0.
    if bar_width > 0:

        lib.console_rect(console, x, y, bar_width, 1, False, lib.BKGND_SET)

    # Draw text over top.
    lib.console_set_default_foreground(console, lib.white)
    lib.console_print_ex(console, x + total_width/2 , y, lib.BKGND_NONE, lib.CENTER, str(value)+'/'+str(maximum))
    

def mouse_get_targets():
    """ Grabs objects under mouse and returns them. """
    
    # Get mouse coords.
    mouse = lib.mouse_get_status()

    templist = []
    # Get objects under mouse.
    for obj in objects_list:

        # Mouse is over object.
        if obj.x == mouse.cx and obj.y == mouse.cy:
            
            if obj.explored == True and obj.always_visible == True or lib.map_is_in_fov(fov_map, obj.x, obj.y):

                # Object blocks.
                if obj.solid:

                    return [obj]

                # Doesn't.
                else:

                    templist.append(obj)
    
    for widget in widgets_list:
            
        if mouse.cx <= widget.width and mouse.cx >= widget.x-(len(widget.text)/2)-1 and mouse.cy <= widget.height and mouse.cy >= widget.y-1:
            
            templist.append(widget)

    # Return objects.
    templist.reverse()
    return templist
    
    
def render_menu(width, height, color, x, y, header):
    """ Renders a menu with the given variables. """
    
    # Create off-screen console.
    window = lib.console_new(width-2, height-2)
    
    # Create window.
    lib.console_rect(window, x, y, width, height, True, lib.BKGND_NONE)
    
    # Create border.
    create_border(width, height, color, 0, 0, 0, x, y)
    create_border(3, 3, color, 0, 0, 0, x+width-3, y)
    lib.console_print_ex(0, x+width-3, y, lib.BKGND_NONE, lib.CENTER, chr(194))
    lib.console_print_ex(0, x+width-1, y+2, lib.BKGND_NONE, lib.CENTER, chr(180))
    
    # Show header.
    lib.console_set_default_foreground(0, eval(CONFIG_DATA['TEXT']['COLOR']))
    lib.console_print_ex(0, x+width/2, y, lib.BKGND_NONE, lib.CENTER, header)
    
    # Create exit widget.
    exists = False
    for widget in widgets_list:
        
        if widget.text == 'X':
            
            exists = True
            
    if exists == False:
        
        widgets_list.append(Widget.Button(x+width-2, y+1, 'X', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), None))
    
    # Blit contents of off-screen console to root console.
    lib.console_blit(window, 0, 0, width, height, 0, x+1, y+1, 1.0, 0.1)
        
        
def create_border(width, height, color, console, x, y, startx = 0, starty = 0):
    """ Creates a border for various GUI elements. """
    
    # Set color.
    lib.console_set_default_foreground(console, color)
    
    # Create border.
    # Height
    for i in range(height-2):

        lib.console_print_ex(console, startx, i+1+starty, lib.BKGND_NONE, lib.CENTER, chr(179))
        lib.console_print_ex(console, width-1+startx, i+1+starty, lib.BKGND_NONE, lib.CENTER, chr(179))
    
    # Width
    for i in range(width-1):

        lib.console_print_ex(console, i+startx, starty, lib.BKGND_NONE, lib.CENTER, chr(196))
        lib.console_print_ex(console, i+startx, height-1+starty, lib.BKGND_NONE, lib.CENTER, chr(196))
    
    # Corners.
    lib.console_print_ex(console, startx, starty, lib.BKGND_NONE, lib.CENTER, chr(218))
    lib.console_print_ex(console, width-1+startx, starty, lib.BKGND_NONE, lib.CENTER, chr(191))
    lib.console_print_ex(console, width-1+startx, height-1+starty, lib.BKGND_NONE, lib.CENTER, chr(217))
    
    
    lib.console_print_ex(console, startx, height-1+starty, lib.BKGND_NONE, lib.CENTER, chr(192))
    
    
def create_message(text, color):
    """ Create a message and display it in the message panel. """
    
    # Split message if necessary.
    new_msg_lines = textwrap.wrap(text, MSG_PANEL_W)

    # Display messages, remove oldest one if full.
    num = 1
    for line in new_msg_lines:

        if len(game_msgs) == MSG_PANEL_H:

            del game_msgs[0]
        
        if num == 1:
        
            game_msgs.append(('- '+line, color))
            num += 1
            
        else:
            game_msgs.append((line, color))
   
   
def render_all():
    """ Render everything in the game. """
    
    # Set globals.
    global fov_recompute
    
    # Recompute FOV if needed.
    if fov_recompute:
        
        fov_recompute = False
        lib.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
        lib.console_clear(con)
            
    # Render objects.
    render_objects()
    
    # Blit contents of off-screen console to root console.
    lib.console_blit(con, 0, 0, MAP_W, MAP_H, 0, 0, 0)
    
    # Render GUI.
    render_gui() 
    
    
##############################################
# Menu functions.
#############################################


def inventory_menu_handler():
    """ Handles inventory menu. """
    
    # Set globals.
    global turns 
    
    # Min, max, refresh for inventory scrolling.
    min = 0
    if len(player.inventory)-1 > 8:
        max = 8  
    else:
        max = len(player.inventory)
    
    refresh = True
            
    # Loopage.
    while not lib.console_is_window_closed():
        
        # Create item widgets.
        if refresh == True:
            
            cleanup_widgets()
            
            if len(player.inventory[min:max]) == 0:
                    
                    refresh = False
                    
            else:
            
                for i in range(len(player.inventory[min:max])):
                    
                    widgets_list.append(Widget.Button(SCREEN_W/3+3, SCREEN_H/4-4+(i*3), player.inventory[min:max][i].name, 
                                        eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), None))
                    widgets_list.append(Widget.Button(SCREEN_W/2+13, SCREEN_H/4-4+(i*3), 'Use', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                        eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), player.inventory[min:max][i].item.use_function+'('+str(i+min)+')'))
                    widgets_list.append(Widget.Button(SCREEN_W/2+19, SCREEN_H/4-4+(i*3), 'Drop', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                        eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'drop_item('+str(i+min)+')'))
                    
                    if i == len(player.inventory[min:max])-1:
                    
                        refresh = False
                
        # Render everything.
        render_menu(50, 30, eval(CONFIG_DATA['BORDER']['COLOR']), SCREEN_W/4+3, SCREEN_H/4-8, 'Inventory')
        render_gui(True)
        lib.console_flush()
        
        # Grab key events.
        mouse, key = check_for_key_events()
        
        # If inventory menu hotkey is pressed, delete created widgets and exit menu.
        if key.c == eval(CONFIG_DATA['INVENTORY']['KEY']) or key.vk == eval(CONFIG_DATA['INVENTORY']['KEY']):
            
            cleanup_widgets()
            return
        
        # If mouse wheel moves down, scroll menu down.
        elif mouse.wheel_down:
            
            if max < len(player.inventory):
                
                min += 1
                max += 1
                refresh = True
        
        # If mouse wheel moves up, scroll menu up.
        elif mouse.wheel_up:
            
            if max > 8:
                
                min -= 1
                max -= 1
                refresh = True
            
        # Loop through widgets to find the inventory widget, if it is clicked, exit menu.
        for widget in widgets_list:
            
            if mouse.cx <= widget.width and mouse.cx >= widget.x-(len(widget.text)/2)-1 and mouse.cy <= widget.height and mouse.cy >= widget.y-1:
            
                if widget.text != str(CURRENT_SLOT)+':':
            
                    widget.color = widget.light_color
            
                if mouse.lbutton_pressed:
                    
                    if widget.text == 'Inventory' or widget.text == 'X':
                        
                        # Delete created widgets and break loop.
                        cleanup_widgets()    
                        return
                        
                    elif widget.text != 'Character' and widget.text != 'Spells' and widget.click_action is not None:
                        
                        refresh = True
                        cleanup_widgets()
                        eval(widget.click_action)
                        
                        if widget.text != '1:' and widget.text != '2:' and widget.text != '3:':

                            turns += 1
                            move_objects()
                            render_objects()
                    
                    else:
                        
                        cleanup_widgets()
                        render_all()
                        eval(widget.click_action)
                        return

            else:
                    
                if widget.text != str(CURRENT_SLOT)+':':
            
                    widget.color = widget.start_color

                
def character_menu_handler():
    """ Handles character menu. """
    
    # Loopage.
    while not lib.console_is_window_closed():
        
        # Render everything.
        render_menu(30, 30, eval(CONFIG_DATA['BORDER']['COLOR']), SCREEN_W/3+5, SCREEN_H/4-8, player.name)
        render_gui(True)
        lib.console_flush()
        
        # Grab key events.
        mouse, key = check_for_key_events()
        
        # Character stuff.
        lib.console_set_default_foreground(0, eval(CONFIG_DATA['TEXT']['COLOR']))
        lib.console_print_ex(0, SCREEN_W/2-9, 13, lib.BKGND_NONE, lib.LEFT, 'Race      -    '+player_race)
        lib.console_print_ex(0, SCREEN_W/2-9, 16, lib.BKGND_NONE, lib.LEFT, 'History   -    '+player_history)
        lib.console_print_ex(0, SCREEN_W/2-9, 19, lib.BKGND_NONE, lib.LEFT, 'Gender    -    '+player_gender)
        lib.console_print_ex(0, SCREEN_W/2-9, 22, lib.BKGND_NONE, lib.LEFT, 'Turns     -    '+str(turns))
        lib.console_print_ex(0, SCREEN_W/2-9, 25, lib.BKGND_NONE, lib.LEFT, 'Depth     -    '+str(depth))
        lib.console_print_ex(0, SCREEN_W/2-9, 28, lib.BKGND_NONE, lib.LEFT, 'Aurum     -    '+str(aurum))
        
        # If character menu hotkey is pressed, delete created widgets and exit menu.
        if key.c == eval(CONFIG_DATA['CHARACTER']['KEY']) or key.vk == eval(CONFIG_DATA['CHARACTER']['KEY']):
            
            cleanup_widgets()
            return
            
        # Loop through widgets to find the character widget, if it is clicked, exit menu.
        for widget in widgets_list:
            
            if mouse.cx <= widget.width and mouse.cx >= widget.x-(len(widget.text)/2)-1 and mouse.cy <= widget.height and mouse.cy >= widget.y-1:
            
                if widget.text != str(CURRENT_SLOT)+':':
            
                    widget.color = widget.light_color
            
                if mouse.lbutton_pressed:
                    
                    if widget.text == 'Character' or widget.text == 'X':
                        
                        # Delete created widgets and break loop.
                        cleanup_widgets()    
                        return
                    
                    else:
                        
                        cleanup_widgets()
                        eval(widget.click_action)
                        
                        if widget.text != '1:' and widget.text != '2:' and widget.text != '3:':
                        
                            return
                        
            else:
                    
                if widget.text != str(CURRENT_SLOT)+':':
            
                    widget.color = widget.start_color
 

def spell_menu_handler():
    """ Handles spell menu. """
    
    # Min, max, refresh for spell scrolling.
    min = 0
    if len(player.living.spells)-1 > 8:
        max = 8 
    else:
        max = len(player.living.spells)
    
    refresh = True
    
    # Loopage.
    while not lib.console_is_window_closed():
        
        # Create spell widgets.
        if refresh == True:
            
            cleanup_widgets()
            
            if len(player.living.spells[min:max]) == 0:
                    
                    refresh = False
                    
            else:
            
                for i in range(len(player.living.spells[min:max])):
                    
                    widgets_list.append(Widget.Button(SCREEN_W/3+3, SCREEN_H/4-4+(i*3), player.living.spells[min:max][i], 
                                        eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), None))
                    widgets_list.append(Widget.Button(SCREEN_W/2, SCREEN_H/4-4+(i*3), 'Slot 1', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                        eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'player.living.spells[min:max]['+str(i+min)+']'))
                    widgets_list.append(Widget.Button(SCREEN_W/2+9, SCREEN_H/4-4+(i*3), 'Slot 2', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                        eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'player.living.spells[min:max]['+str(i+min)+']'))
                    widgets_list.append(Widget.Button(SCREEN_W/2+18, SCREEN_H/4-4+(i*3), 'Slot 3', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                        eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'player.living.spells[min:max]['+str(i+min)+']'))

                    if i == len(player.living.spells[min:max])-1:
                    
                        refresh = False
                        
        # Render everything.
        render_menu(50, 30, eval(CONFIG_DATA['BORDER']['COLOR']), SCREEN_W/4+3, SCREEN_H/4-8, 'Spell Book')
        render_gui(True)
        lib.console_flush()
        
        # Grab key events.
        mouse, key = check_for_key_events()
        
        # If spell menu hotkey is pressed, delete created widgets and exit menu.
        if key.c == eval(CONFIG_DATA['SPELL']['KEY']) or key.vk == eval(CONFIG_DATA['SPELL']['KEY']):
            
            cleanup_widgets()
            return
        
        # If mouse wheel moves down, scroll menu down.
        elif mouse.wheel_down:
            
            if max < len(player.living.spells):
                
                min += 1
                max += 1
                refresh = True
        
        # If mouse wheel moves up, scroll menu up.
        elif mouse.wheel_up:
            
            if max > 8:
                
                min -= 1
                max -= 1
                refresh = True
                
        # Loop through widgets to find the spell widget, if it is clicked, exit menu.
        for widget in widgets_list:
            
            if mouse.cx <= widget.width and mouse.cx >= widget.x-(len(widget.text)/2)-1 and mouse.cy <= widget.height and mouse.cy >= widget.y-1:
            
                if widget.text != str(CURRENT_SLOT)+':':
            
                    widget.color = widget.light_color
            
                if mouse.lbutton_pressed:
                    
                    if widget.text == 'Spells' or widget.text == 'X':
                        
                        # Delete created widgets and break loop.
                        cleanup_widgets()    
                        return
                    
                    elif 'Slot' not in widget.text and widget.text not in player.living.spells:
                        
                        if widget.text != '1:' and widget.text != '2:' and widget.text != '3:':
                            
                            cleanup_widgets()
                            render_all()
                            eval(widget.click_action)
                            return
                            
                        else:
                        
                            eval(widget.click_action) 
                
                # Check if quickslot hotkeys are pressed, if so, change active quickslot.
                for i in range(3):
                    
                    if widget.text in player.living.spells:
                    
                        if key.c == eval(CONFIG_DATA['QUICK_SLOT'+str(i+1)]['KEY']) or key.vk == eval(CONFIG_DATA['QUICK_SLOT'+str(i+1)]['KEY']):
        
                            QUICK_SLOT[i+1] = widget.text
                        
                    elif mouse.lbutton_pressed:
                        
                        if widget.text == 'Slot '+str(i+1):
                            
                            QUICK_SLOT[i+1] = eval(widget.click_action)
                    
            else:
                    
                if widget.text != str(CURRENT_SLOT)+':':
            
                    widget.color = widget.start_color

                    
def exit_menu_handler():
    """ Handles exit menu. """

    # Create widgets
    widgets_list.append(Widget.Button(SCREEN_W/2+2, SCREEN_H/4+3, 'Restart Game', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                        eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'restart_game(False)'))
    widgets_list.append(Widget.Button(SCREEN_W/2+2, SCREEN_H/4+6, 'Restart Random', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                        eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'restart_game(True)'))
    widgets_list.append(Widget.Button(SCREEN_W/2+2, SCREEN_H/4+9, 'Exit To Menu', 
                        eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), None))
                            
    # Loopage.
    while not lib.console_is_window_closed():
                  
        # Render everything.
        render_menu(21, 20, eval(CONFIG_DATA['BORDER']['COLOR']), SCREEN_W/3+10, SCREEN_H/4-3, 'Game Menu')
        render_gui(True)
        lib.console_flush()
        
        # Grab key events.
        mouse, key = check_for_key_events()
        
        # If exit menu hotkey is pressed, delete created widgets and exit menu.
        if key.c == eval(CONFIG_DATA['EXIT']['KEY']) or key.vk == eval(CONFIG_DATA['EXIT']['KEY']):
            
            cleanup_widgets()
            return
            
        # Loop through widgets and react to clicks.
        for widget in widgets_list:
            
            if mouse.cx <= widget.width and mouse.cx >= widget.x-(len(widget.text)/2)-1 and mouse.cy <= widget.height and mouse.cy >= widget.y-1:
            
                if widget.text != str(CURRENT_SLOT)+':':
            
                    widget.color = widget.light_color
            
                if mouse.lbutton_pressed:
                    
                    if widget.text == 'X':
                        
                        # Delete created widgets and break loop.
                        cleanup_widgets()
                        return
                    
                    elif widget.text == 'Exit To Menu':
                        
                        # Exit to main menu.
                        return 'EXIT'
                        
                    else:
                        
                        eval(widget.click_action)
                        
                        if widget.text != '1:' and widget.text != '2:' and widget.text != '3:':
                        
                            return
                        
            else:
                    
                if widget.text != str(CURRENT_SLOT)+':':
            
                    widget.color = widget.start_color


def restart_game(random):
    """ Restarts game with the exact same player choices. """
    
    if random == True:
        
        # Choose random race/history/gender.
        race = RACE_DATA.keys()[lib.random_get_int(0, 0, len(RACE_DATA.keys())-1)]
        history = HISTORY_DATA.keys()[lib.random_get_int(0, 0, len(HISTORY_DATA.keys())-1)]
        gender = GENDER_DATA.keys()[lib.random_get_int(0, 0, len(GENDER_DATA.keys())-1)]
        
        # Choose random name.
        name = get_random_name(gender)
        
        # Start new game.
        new_game(name, race, history, gender)
    
    else:
        
        # Start new game.
        new_game(player.name, player_race, player_history, player_gender)
        

##############################################
# Widget functions.
##############################################


def cleanup_widgets():
    """ Deletes widgets created in menu's. """
    
    # Delete all created widgets.
    for i in range(len(player.inventory)):
    
        for widget in widgets_list[:]:
        
            if widget.text == player.inventory[i].name:
                
                widgets_list.remove(widget)
    
    for i in range(len(player.living.spells)):
    
        for widget in widgets_list[:]:
        
            if widget.text == player.living.spells[i]:
                
                widgets_list.remove(widget)
                
    for widget in widgets_list[:]:
        
        if widget.text == 'X' or widget.text == 'Use' or widget.text == 'Drop' or 'Slot' in widget.text:
            
            widgets_list.remove(widget)
        
        elif widget.text == 'Restart Game' or widget.text == 'Restart Random' or widget.text == 'Exit To Menu':
            
            widgets_list.remove(widget)
  

def select_widget(widget, widgets_list):
    """ Sets given widget to selected. """
    
    if widget.selected == False:
        
        for other in widgets_list:
            
            if other.type == 'Checkbox' and other.group == widget.group and other.selected == True:
                
                other.selected = False
                
        widget.selected = True
        
    else:
        
        widget.selected = False
        

def input_text(widget, letter):
    """ Inputes text into given widget. """
    
    if len(widget.text) < widget.width-3:
    
        # Add letter to input.
        widget.text += letter

        
def randomize_selections(widgets_list):
    """ Randomizes selections from given widgets list. """
    
    gender = ''
    
    # Reset selections.
    reset_selections(widgets_list)
    
    # Loop through and pick a random selection for all checkbox type widgets.
    while True:
    
        for widget in widgets_list:
        
            if widget.type == 'Checkbox':
            
                select = True
            
                for other in widgets_list:
                
                    if other.type == 'Checkbox' and other.group == widget.group and other.selected == True:
                    
                        select = False
                        
                if select == True:
                    
                    if lib.random_get_int(0, 1, 4) == 1:
                    
                        widget.selected = True
                        
                        if widget.group == 'Gender':
                            
                            gender = widget.text

        num = 0
        for widget in widgets_list:
            
            if widget.type == 'Checkbox' and widget.selected == True:
                
                num += 1
            
            elif widget.type == 'Input':
                
                widget.text = get_random_name(gender)
                
        if num == 3:
            
            break


def reset_selections(widgets_list):
    """ Resets selections from given widgets list. """

    for widget in widgets_list:
        
        if widget.type == 'Checkbox':
            
            widget.selected = False
        
        elif widget.type == 'Input':
            
            widget.text = ''
            
                
def update_widgets_status(widgets_list, mouse, key):
    """ Checks and updates widgets status's """
    
    # Check if a widget was clicked.
    for widget in widgets_list:
            
        if widget.type == 'Button':
            
            if widget.collision(mouse.cx, mouse.cy):
                
                if widget.text != str(CURRENT_SLOT)+':':
                
                    widget.color = widget.light_color
                
                if mouse.lbutton_pressed:
                    
                    if widget.click_action != 'NEWGAME' and widget.click_action != 'EXIT':
                        
                        eval(widget.click_action)
                    
                    elif widget.click_action == 'NEWGAME':
                        
                        return 'NEWGAME'
                    
                    else:
                        
                         return 'EXIT'
            else:
            
                if widget.text != str(CURRENT_SLOT)+':':
                
                    widget.color = widget.start_color
            
        elif widget.type == 'Input':
                        
            # If key is a character add it to string.
            if key.c > 0 and key.vk != lib.KEY_ENTER and key.vk != lib.KEY_ESCAPE and key.vk != lib.KEY_BACKSPACE:
                    
                input_text(widget, chr(key.c))

            # If backspace is pressed, delete last character in string.
            elif key.vk == lib.KEY_BACKSPACE:

                # Delete last character in string.
                widget.text = widget.text[:-1]  
            
        elif widget.type == 'Checkbox':
                
            if widget.collision(mouse.cx, mouse.cy):
                    
                widget.color = widget.light_color
                    
                if mouse.lbutton_pressed:
                        
                    eval(widget.click_action)
                    
            else:
                    
                widget.color = widget.start_color
                    
    
#############################################
# Player functions.
#############################################


def check_for_key_events():
    """ Check for all key events. """
    
    # Set mouse and keys.
    mouse = lib.Mouse()
    key = lib.Key()

    # Check for events.
    lib.sys_check_for_event(lib.EVENT_KEY_PRESS | lib.EVENT_MOUSE, key, mouse)
    
    # Change to fullscreen if hotkey is pressed.
    if 'ord' in CONFIG_DATA['FULLSCREEN']['KEY']:
        
        if key.c == eval(CONFIG_DATA['FULLSCREEN']['KEY']):
        
            lib.console_set_fullscreen(not lib.console_is_fullscreen())
            
    elif key.vk == eval(CONFIG_DATA['FULLSCREEN']['KEY']):

        lib.console_set_fullscreen(not lib.console_is_fullscreen())
    
    # Return events.
    return mouse, key
    
    
def player_key_action():
    """ React to key events. """
    
    # Set globals.
    global fov_recompute, LEFT_MOUSE_ACTION, turns
    
    # Grab key events.
    mouse, key = check_for_key_events()
     
    # If exit hotkey is pressed, exit game.
    if key.c == eval(CONFIG_DATA['EXIT']['KEY']) or key.vk == eval(CONFIG_DATA['EXIT']['KEY']):
        
        exit = exit_menu_handler()
        
        return exit
            
    # If inventory hotkey is pressed, open inventory.
    elif key.c == eval(CONFIG_DATA['INVENTORY']['KEY']) or key.vk == eval(CONFIG_DATA['INVENTORY']['KEY']):
        
        inventory_menu_handler()
    
    # If character hotkey is pressed, open character menu.
    elif key.c == eval(CONFIG_DATA['CHARACTER']['KEY']) or key.vk == eval(CONFIG_DATA['CHARACTER']['KEY']):
        
        character_menu_handler()
    
    # If spell book hotkey is pressed, open spell menu.
    elif key.c == eval(CONFIG_DATA['SPELL']['KEY']) or key.vk == eval(CONFIG_DATA['SPELL']['KEY']):
        
        spell_menu_handler()
    
    # If left mouse switch hotkey is pressed, open switch current left mouse action.
    elif key.c == eval(CONFIG_DATA['LEFT_MOUSE_SWITCH']['KEY']) or key.vk == eval(CONFIG_DATA['LEFT_MOUSE_SWITCH']['KEY']):
        
        wait = 15
        lib.console_set_default_foreground(0, eval(CONFIG_DATA['TEXT']['COLOR']))
        if LEFT_MOUSE_ACTION == 'MOVE':
            
            LEFT_MOUSE_ACTION = 'ATTACK'
            
            lib.console_print_ex(0, SCREEN_W/2, SCREEN_H/2-5, lib.BKGND_NONE, lib.CENTER, 'Mouse Attacking Activated')
        
        else:
            
            LEFT_MOUSE_ACTION = 'MOVE'
            lib.console_print_ex(0, SCREEN_W/2, SCREEN_H/2-5, lib.BKGND_NONE, lib.CENTER, 'Mouse Movement Activated')
        
        while True:
            
            lib.console_flush()
            wait -= 1
            if wait == 0:
                
                break
    
    # If movement hotkeys are pressed, move the player.
    elif key.c == eval(CONFIG_DATA['MOVE_UP']['KEY']) or key.vk == eval(CONFIG_DATA['MOVE_UP']['KEY']):
        
        move_player(player.x, player.y-1)
        fov_recompute = True
        return 'TURN-TAKEN'
    
    elif key.c == eval(CONFIG_DATA['MOVE_DOWN']['KEY']) or key.vk == eval(CONFIG_DATA['MOVE_DOWN']['KEY']):
        
        move_player(player.x, player.y+1)
        fov_recompute = True
        return 'TURN-TAKEN'
        
    elif key.c == eval(CONFIG_DATA['MOVE_LEFT']['KEY']) or key.vk == eval(CONFIG_DATA['MOVE_LEFT']['KEY']):
        
        move_player(player.x-1, player.y)
        fov_recompute = True
        return 'TURN-TAKEN'
    
    elif key.c == eval(CONFIG_DATA['MOVE_RIGHT']['KEY']) or key.vk == eval(CONFIG_DATA['MOVE_RIGHT']['KEY']):
        
        move_player(player.x+1, player.y)
        fov_recompute = True
        return 'TURN-TAKEN'
        
    elif key.c == eval(CONFIG_DATA['MOVE_UP_LEFT']['KEY']) or key.vk == eval(CONFIG_DATA['MOVE_UP_LEFT']['KEY']):
        
        move_player(player.x-1, player.y-1)
        fov_recompute = True
        return 'TURN-TAKEN'
        
    elif key.c == eval(CONFIG_DATA['MOVE_UP_RIGHT']['KEY']) or key.vk == eval(CONFIG_DATA['MOVE_UP_RIGHT']['KEY']):
        
        move_player(player.x+1, player.y-1)
        fov_recompute = True
        return 'TURN-TAKEN'
    
    elif key.c == eval(CONFIG_DATA['MOVE_DOWN_LEFT']['KEY']) or key.vk == eval(CONFIG_DATA['MOVE_DOWN_LEFT']['KEY']):
        
        move_player(player.x-1, player.y+1)
        fov_recompute = True
        return 'TURN-TAKEN'
        
    elif key.c == eval(CONFIG_DATA['MOVE_DOWN_RIGHT']['KEY']) or key.vk == eval(CONFIG_DATA['MOVE_DOWN_RIGHT']['KEY']):
        
        move_player(player.x+1, player.y+1)
        fov_recompute = True
        return 'TURN-TAKEN'
                
    # Check if quickslot hotkeys are pressed, if so, change active quickslot.
    for i in range(3):
        
        if key.c == eval(CONFIG_DATA['QUICK_SLOT'+str(i+1)]['KEY']) or key.vk == eval(CONFIG_DATA['QUICK_SLOT'+str(i+1)]['KEY']):
        
            select_quick_slot(i+1)
        
    # Check and update widget_status's.
    update_widgets_status(widgets_list, mouse, key)
    
    # If left button is pressed.
    if mouse.lbutton_pressed:
        
        # Move player if activated.
        if LEFT_MOUSE_ACTION == 'MOVE':
        
            # Grab coords and convert them.
            x, y = mouse.cx, mouse.cy
            
            # Only move if coords are in FOV.
            if lib.map_is_in_fov(fov_map, x, y):
                
                startx, starty = player.x, player.y
                move_player(x, y)
                if player.x != startx or player.y != starty:
                    
                    fov_recompute = True
                    return 'TURN-TAKEN'
        
        else:
            
            if QUICK_SLOT[CURRENT_SLOT] != '' and lib.map_is_in_fov(fov_map, mouse.cx, mouse.cy):
                
                if mouse.cx != player.x or mouse.cy != player.y:
            
                    cast_spell(QUICK_SLOT[CURRENT_SLOT], player, player.x, player.y, mouse.cx, mouse.cy)
                    return 'TURN-TAKEN'
    
    # If right button is pressed, interact with object.
    elif mouse.rbutton_pressed:
        
        for obj in objects_list:
            
            if distance_to_target(player, obj) < 2 and obj.x == mouse.cx and obj.y == mouse.cy:
                
                if obj.interaction is not None:
                    
                    eval(obj.interaction)
                    turns += 1
                    return 'TURN-TAKEN'
        
        # Check for stairs.
        if distance_to_target(player, stairsdown) == 0 and stairsdown.x == mouse.cx and stairsdown.y == mouse.cy:
            
            descend()
            return 'TURN-TAKEN'
            
        elif depth > 1:
            
            if distance_to_target(player, stairsup) == 0 and stairsup.x == mouse.cx and stairsup.y == mouse.cy:
            
                ascend()
                return 'TURN-TAKEN'


def select_quick_slot(quick_slot):
    """ Selects a quick slot. """
    
    # Set globals.
    global CURRENT_SLOT
    
    CURRENT_SLOT = quick_slot

    for widget in widgets_list:
        
        if widget.text == str(quick_slot)+':':
            
            widget.color = eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR'])
        
        else:
            
            widget.color = eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR'])
            
            
def move_player(dx, dy):
    """ Moves player to given coords. """
    
    # Set globals.
    global turns
    
    # Move player and increase turns.
    while True:
        
        # Grabbed starting coords.
        startx, starty = player.x, player.y
        
        # Compute path.
        x, y = compute_path(player, dx, dy)
        
        # If step isn't blocked and path is valid, move the player.
        if not is_blocked(x, y) and x is not None:
            
            player.x, player.y = x, y
        
        # If player has moved, increase turns.
        if player.x != startx or player.y != starty:
        
            turns += 1
        
        # If living object is in view only allow one step to be taken.
        for obj in objects_list:
            
            if obj.living and lib.map_is_in_fov(fov_map, obj.x, obj.y) and obj != player and obj.living.ai is not None:
                
                if 'DisguisedAI' not in obj.living.ai:
                
                    return
         
        # Break loop if target is reached.
        if player.x == dx and player.y == dy or x is None:
            
            turns += 1
            break


def player_death(killedby):
    """ Handles the players death. """
       
    # Refresh.
    render_all()

    # Create widget.
    widgets_list = [Widget.Button(SCREEN_W/2, SCREEN_H/2-5, 'Continue', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                  eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), None),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-2, 'Restart Game', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                  eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'restart_game(False)'),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2+1, 'Restart Random', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                  eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'restart_game(True)')]
            
    # LOOPAGE.
    while not lib.console_is_window_closed():
            
        # Show message.
        lib.console_set_default_foreground(0, eval(CONFIG_DATA['TEXT']['COLOR']))
        lib.console_print_ex(0, SCREEN_W/2, SCREEN_H/2-8, lib.BKGND_NONE, lib.CENTER, 'You will killed by a '+killedby)
                
        # Show widgets.
        for widget in widgets_list:
        
            lib.console_set_default_foreground(0, widget.color)
            lib.console_print_ex(0, widget.x, widget.y, lib.BKGND_NONE, lib.CENTER, widget.text)
            
        # Display.
        lib.console_flush()
            
        # Grab key events.
        mouse, key = check_for_key_events()
            
        # Check if widget was clicked.
        for widget in widgets_list:
        
            if mouse.cx <= widget.width and mouse.cx >= widget.x-(len(widget.text)/2)-1 and mouse.cy <= widget.height and mouse.cy >= widget.y-1:
            
                if widget.text != str(CURRENT_SLOT)+':':
            
                    widget.color = widget.light_color
            
                if mouse.lbutton_pressed:
                
                    if widget.click_action is not None:
                        
                        eval(widget.click_action)
                        return
                
                    else:
                
                        return True
        
            else:
            
                if widget.text != str(CURRENT_SLOT)+':':
            
                    widget.color = widget.start_color
    

#############################################
# Location functions.
#############################################


def descend():
    """ Handles descending stairs. """
    
    # Set globals.
    global objects_list, stairsdown, stairsup, depth
    
    # Save old location.
    locations_list[depth-1].objects = objects_list
    
    # Increase depth.
    depth += 1

    # Load old location if present.
    loaded = False
    for location in locations_list:
    
        if location.id == depth:
        
            # Show message.
            create_message('You slowly descend down the steps.', eval(CONFIG_DATA['MESSAGE']['GOOD']))
            
            # Load objects.
            objects_list = location.objects
            
            # Set stairs.
            for obj in objects_list:
                
                if obj.name == 'Stairs Down':
                    
                    stairsdown = obj
                
                elif depth > 1:
                
                    if obj.name == 'Stairs Up':
                    
                        stairsup = obj
            
            # Set player coords.
            player.x = stairsup.x+1
            player.y = stairsup.y+1
            
            # Initiate FOV.
            compute_fov()
            loaded = True
            break
    
    # Load new location if needed.
    if loaded == False:
        
        # Show message.
        create_message('You slowly descend down the steps, giving you a little time to rest.', eval(CONFIG_DATA['MESSAGE']['GOOD']))
    
        # Heal the player some.
        player.living.restore_health(5)

        # Create a new map and initiate FOV.
        create_map()
        compute_fov()           
              

def ascend():
    """ Handles ascending stairs. """
    
    global objects_list, stairsdown, stairsup, depth
    
    # Save old location.
    locations_list[depth-1].objects = objects_list
    
    # Show message.
    create_message('You ascend up the steps. ', eval(CONFIG_DATA['MESSAGE']['GOOD']))

    # Remove depth.
    depth -= 1

    # Load old location.
    loaded = False
    for location in locations_list:
        
        if location.id == depth:
            
            # Load objects.
            objects_list = location.objects
            
            # Set stairs.
            for obj in objects_list:
                
                if obj.name == 'Stairs Down':
                    
                    stairsdown = obj
                
                elif depth > 1:
                
                    if obj.name == 'Stairs Up':
                    
                        stairsup = obj
                        
            # Set player coords.
            player.x = stairsdown.x+1
            player.y = stairsdown.y+1
    
            # Initiate FOV.
            compute_fov()
            loaded = True
            break
            
    # Load new location if needed.
    if loaded == False:
    
        # Create a new map and initiate FOV.
        create_map()
        compute_fov()
    

#############################################
# Spell functions.
#############################################


def cast_spell(spell, caster, startx, starty, target_x, target_y):
    """ Casts given spell. """
    
    # Set globals.
    global turns
    
    if player.living.energy[0] >= SPELL_DATA[spell]['ENERGYCOST']:
    
        # Create spell and add it to list for drawing.
        spell_component = Object.Spell(SPELL_DATA[spell]['DAMAGE'], SPELL_DATA[spell]['EFFECT'], caster, target_x, target_y)

        spell_object = Object.Object(startx, starty, spell, False, False, False, SPELL_DATA[spell]['IMAGE'], eval(SPELL_DATA[spell]['COLOR']), 
                                    spell = spell_component)

        objects_list.append(spell_object)

        # Subtract energy.
        player.living.energy[0] -= SPELL_DATA[spell]['ENERGYCOST']
    
        # Create message and increase turns.
        create_message(SPELL_DATA[spell]['USE_MESSAGE'], eval(CONFIG_DATA['MESSAGE']['NORMAL']))
        turns += 1
    
        move_spells()


def move_spells():
    """ Moves all spells on screen. """
    
    # Loopage
    for obj in objects_list[:]:
            
        if obj.spell:
            
            # More loopage.
            while True:
                
                # Move spell.
                x, y = compute_path(obj, obj.spell.target_x, obj.spell.target_y)
                obj.x, obj.y = x,y
                
                # Refresh screen.
                render_all()
                lib.console_flush()
                
                # If target is reached.
                if obj.x == obj.spell.target_x and obj.y == obj.spell.target_y:
                    
                    # Ok, stop with the loopage.
                    for object in objects_list[:]:
                        
                        if object != obj and object.x == obj.spell.target_x and object.y == obj.spell.target_y:
                        
                            if object.living:
                        
                                # Apply damage/effect.
                                if obj.spell.effect is not None:
                                
                                    eval(obj.spell.effect)
                                    
                                take_damage(object, obj.spell.damage, obj.spell.caster)
                        
                            else:
                            
                                if object != obj and object.x == obj.spell.target_x and object.y == obj.spell.target_y:
                                
                                    # Apply effect.
                                    if obj.spell.effect is not None:
                                
                                        eval(obj.spell.effect)
                                
                    objects_list.remove(obj)
                    return
                    
                else:
                    
                    # Ok, stop with the loopage.
                    for object in objects_list[:]:
                        
                        if object != obj and object.x == obj.x and object.y == obj.y:
                        
                            if object.living:
                        
                                # Apply damage/effect.
                                if obj.spell.effect is not None:
                                
                                    eval(obj.spell.effect)
                                    
                                take_damage(object, obj.spell.damage, obj.spell.caster)
                                objects_list.remove(obj)
                                return

 
def fire_lance_effect(obj):
    """ Determines what happens when something gets hit by a fire lance. """
    
    if obj.living:
        
        if obj.living.status == 'NORMAL' or obj.living.status == 'DISGUISED':
        
            # Set object on fire.
            obj.living.status = 'BURNING'
            obj.color = [lib.red, lib.red]
        
            # Create message.
            create_message('You set the '+obj.name+' aflame!', eval(CONFIG_DATA['MESSAGE']['NORMAL']))
        
    # If fire lance collades with a object, turn it to ash.
    elif obj.item or 'Corpse' in obj.name:
        
        if obj.name != 'Ash' and obj.name != 'Aurum' and obj.name != 'Stairs' and obj.name != 'Portal':

            # Show message.
            create_message('You set the '+obj.name+' on fire turning it to ash in seconds!', eval(CONFIG_DATA['MESSAGE']['NORMAL']))

            # Create object component.
            item_component = Object.Item(use_function = ITEM_DATA['Ash']['USE'], use_message = ITEM_DATA['Ash']['USE_MESSAGE'])

            # Change object to ash.
            obj.name = 'Ash'
            obj.color = eval(ITEM_DATA['Ash']['COLOR'])
            obj.image = ITEM_DATA['Ash']['IMAGE']
            obj.interaction = 'pick_up(obj)'
            obj.item = item_component
        

##############################################
# Object functions.
##############################################


def BasicAI(obj):
    """ Basic NPC AI. """
    
    # Check if in FOV.
    if lib.map_is_in_fov(fov_map, obj.x, obj.y):
        
        # Move towards if not close enough to attack.
        if distance_to_target(obj, player) >= 2:

            x, y = compute_path(obj, player.x, player.y)
            
            if not is_blocked(x, y) and x is not None:
                
                obj.x, obj.y = x, y
                
        # If close enough, attack.
        else:
            
            take_damage(player, obj.living.damage, obj)
            create_message('The '+obj.name+' attacks you!', eval(CONFIG_DATA['MESSAGE']['NORMAL']))
   

def DisguisedAI(obj):
    """ Disguised NPC AI. """
        
    # Check if in FOV.
    if lib.map_is_in_fov(fov_map, obj.x, obj.y):

        # Check if player is close, if so, change the object into true form.
        if not distance_to_target(obj, player) >= 2:
            
            if obj.name in ITEM_DATA.keys():
            
                create_message('In an instant the '+obj.name+' changes into its true form and attacks you.', eval(CONFIG_DATA['MESSAGE']['WARNING']))
                
            else:
                
                create_message('In an instant '+obj.name+' changes into its true form and attacks you.', eval(CONFIG_DATA['MESSAGE']['WARNING']))
                
            obj.image = obj.startimage
            obj.color = obj.startcolor
            obj.name = obj.startname
            obj.living.ai = 'BasicAI(obj)'
            obj.living.status = 'NORMAL'
            take_damage(player, obj.living.damage, obj)


def RangedAI(obj):
    """ Ranged NPC AI. """
    
    # If close enough, attack.
    if lib.map_is_in_fov(fov_map, obj.x, obj.y):
    
        if distance_to_target(obj, player) <= 4 and player.living.health[0] > 0:

            # If NPC is an archer, fire an arrow.
            if 'Archer' in obj.name:

                # Create arrow and add it to list for drawing.
                arrow_component = Object.Spell(obj.living.damage, None, obj, player.x, player.y)
                arrow = Object.Object(obj.x, obj.y, 'Arrow', False, False, False, '.', [lib.white, lib.white], spell = arrow_component)
                objects_list.append(arrow)
            
                # Move spell.
                move_spells()
            
                # Create message.
                create_message('The '+obj.name+' attacked you.', eval(CONFIG_DATA['MESSAGE']['NORMAL']))

        # Move towards player if too far away.
        else:

            x, y = compute_path(obj, player.x, player.y)
            
            if not is_blocked(x, y) and x is not None:
                
                obj.x, obj.y = x, y
        
            
def distance_to_target(obj, target):
    """ Returns the distance to target. """
    
    dx = target.x - obj.x
    dy = target.y - obj.y

    return math.sqrt(dx ** 2 + dy ** 2)
    
    
def compute_path(obj, x, y):
    """ Computes given path and moves object. """

    # Create path.
    path = lib.path_new_using_map(fov_map, 1.0)

    # Compute path.
    lib.path_compute(path, obj.x, obj.y, x, y)
    testx, testy = lib.path_walk(path, False)

    # Return testx, testy.
    return testx, testy
    
    lib.path_delete(path)

    
def send_to_front(obj):
    """ Send object to front of list. """

    objects_list.remove(obj)
    objects_list.insert(len(objects_list), obj)


def move_objects():
    """ Moves all objects needed. """
    
    for obj in objects_list:
        
        if player.living.health[0] < 1:
                        
            break
            
        if obj.living and obj != player:
        
            if obj.living.ai:
                
                temp = 100
                while (temp-obj.living.speed) >= 0:
                
                    eval(obj.living.ai)
                    temp -= obj.living.speed
                    
                    if player.living.health[0] < 1:
                        
                        break
                    
                    # If object is on fire, burn it.
                    if obj.living.status == 'BURNING':
                
                        take_damage(obj, 1, player)

                        if not obj.living:
                            
                            break
                    

def take_damage(obj, dmg, attacker):
    """ Applies damage to object. """
    
    # Change diguised objects into true form.
    if obj.living.ai and 'DisguisedAI' in obj.living.ai:
        
        create_message('In an instant '+obj.name+' changes into its true form.', eval(CONFIG_DATA['MESSAGE']['WARNING']))
        obj.image = obj.startimage
        obj.color = obj.startcolor
        obj.name = obj.startname
        obj.living.ai = 'BasicAI(obj)'
        if obj.living.status == 'DISGUISED':
            obj.living.status = 'NORMAL'

    # Reduce damage if needed.
    if obj.name == 'Demon':
        
        dmg = dmg/2
        
    # Apply damage.
    obj.living.health[0] -= dmg

    # If object dies, run death function.
    if obj.living.health[0] <= 0:
        
        obj.living.health[0] = 0

        if obj.living.death_function is not None and obj != player:
        
            eval(obj.living.death_function)
            
        elif obj == player:
            
            player.killedby = attacker.name


def basic_object_death(obj):
    """ Handles what happens when a object dies. """

    # Create a message.
    create_message('The '+obj.name+' has perished.', eval(CONFIG_DATA['MESSAGE']['NORMAL']))
    
    # Change name.
    if 'Corpse' not in obj.name:

        obj.name += ' Corpse'

    # Change object to dead.
    obj.image = '%'
    obj.color = [lib.dark_red, lib.dark_red]
    obj.living = None
    obj.ai = None

    
def possessed_object_death(obj):
    """ Handles what happens when a possessed object dies. """

    possessed = False
    
    # Check for corpses.
    for corpse in objects_list:

        if 'Corpse' in corpse.name:

            if distance_to_target(obj, corpse) <= 5:

                # Possess corpse.
                corpse.living = obj.living
                corpse.living.health[0] = obj.living.health[1]/2
                corpse.ai = obj.ai
                corpse.color = obj.color
                corpse.startcolor = obj.color
                corpse.name = obj.name

                # Make other object a corpse.
                obj.image = '%'
                if obj.startname == obj.name:
                    
                    gender = GENDER_DATA.keys()[lib.random_get_int(0, 0, len(GENDER_DATA.keys())-1)]
                    obj.name = get_random_name(gender)

                else:

                    obj.name = obj.startname

                if 'Corpse' not in obj.name:

                    obj.name += ' Corpse'

                obj.color = [lib.dark_red, lib.dark_red]
                obj.living = None
                obj.ai = None

                # Show message and break loop.
                create_message('You see a dark red light shoot from the '+obj.name+' and capture a new host.', eval(CONFIG_DATA['MESSAGE']['WARNING']))
                possessed = True
                break

    # Change object to corpse.
    if possessed == False:

        # Show message.
        create_message('You see a dark red light shoot back and forth across the room as it slowly fades.', eval(CONFIG_DATA['MESSAGE']['NORMAL']))

        obj.image = '%'
        if obj.startname == obj.name:

            obj.name = 'John Doe'

        else:

            obj.name = obj.startname

        if 'Corpse' not in obj.name:

            obj.name += ' Corpse'

        obj.color = [lib.dark_red, lib.dark_red]
        obj.living= None
        obj.ai = None
        

def get_random_name(gender):
    """ Creates a random name. """
    
    name = ''
    
    if lib.random_get_int(0, 1, 4) == 1:
    
        for key in GENDER_DATA.keys():
    
            if gender == key:
        
                name = NAME_DATA[key]['NAMES'][lib.random_get_int(0, 0, len(NAME_DATA[key]['NAMES'])-1)]
    
    else:
        
        name = NAME_DATA['Neutral']['NAMES'][lib.random_get_int(0, 0, len(NAME_DATA['Neutral']['NAMES'])-1)]
        
    return name
    
    
##############################################
# Item functions.
##############################################


def pick_up(obj):
    """ Picks up given item and adds it to inventory. """
    
    player.inventory.append(obj)
    objects_list.remove(obj)
    create_message('You picked up: '+obj.name, eval(CONFIG_DATA['MESSAGE']['NORMAL']))


def add_aurum(obj):
    """ Adds given amount of aurum. """
    
    # Set globals.
    global aurum
    
    amount = (5+lib.random_get_int(0, 1, depth))*lib.random_get_int(0, 1, 3)
    aurum += amount
    objects_list.remove(obj)
    create_message('You picked up '+str(amount)+' '+obj.name, eval(CONFIG_DATA['MESSAGE']['NORMAL']))
    
    
def drop_item(item):
    """ Removes an item from the players inventory. """
    
    player.inventory[item].x, player.inventory[item].y = player.x, player.y
    objects_list.append(player.inventory[item])
    create_message('You droped: '+player.inventory[item].name, eval(CONFIG_DATA['MESSAGE']['NORMAL']))
    player.inventory.remove(player.inventory[item])


def use_vodka(item):
    """ Uses vodka. """
    
    # Add some health.
    player.living.restore_health(player.living.health[1]/2)
    
    # Create message and remove item from inventory.
    create_message(ITEM_DATA[player.inventory[item].name]['USE_MESSAGE'], eval(CONFIG_DATA['MESSAGE']['GOOD']))
    player.inventory.remove(player.inventory[item])
    
    
def use_bacon_cocktail(item):
    """ Uses a bacon cocktail. """
    
    # Add some energy.
    player.living.restore_energy(player.living.energy[1]/2)
    
    # Create message and remove item from inventory.
    create_message(ITEM_DATA[player.inventory[item].name]['USE_MESSAGE'], eval(CONFIG_DATA['MESSAGE']['GOOD']))
    player.inventory.remove(player.inventory[item])
    
    
#############################################
# Initialization, main loop and menu.
#############################################


def create_player():
    """ Handles player creation. """
        
    # Create widgets.
    widgets_list = [Widget.Button(6, SCREEN_H-3, '<-BACK', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'EXIT'),
                    Widget.Button(SCREEN_W/2-6, SCREEN_H-3, 'RESET', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'reset_selections(widgets_list)'),
                    Widget.Button(SCREEN_W/2+3, SCREEN_H-3, 'RANDOMIZE', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'randomize_selections(widgets_list)'),
                    Widget.Button(SCREEN_W-8, SCREEN_H-3, 'CONTINUE->', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'NEWGAME'),
                    Widget.Input(10, SCREEN_H/2-1, 24, 3, '', eval(CONFIG_DATA['INPUT']['NORMAL_COLOR']), eval(CONFIG_DATA['INPUT']['LIGHT_COLOR']), None)]
    
    y = 0
    for race in RACE_DATA.keys():
        
        widget = Widget.Checkbox(SCREEN_W/2-18, SCREEN_H/2+y, race, eval(CONFIG_DATA['CHECKBOX']['NORMAL_COLOR']), eval(CONFIG_DATA['CHECKBOX']['LIGHT_COLOR']), 
                                 'select_widget(widget, widgets_list)', group = 'Race')
        widgets_list.append(widget)
        y += 3
    y = 0
    for history in HISTORY_DATA.keys():
        
        widget = Widget.Checkbox(SCREEN_W/2+4, SCREEN_H/2+y, history, eval(CONFIG_DATA['CHECKBOX']['NORMAL_COLOR']), eval(CONFIG_DATA['CHECKBOX']['LIGHT_COLOR']), 
                                 'select_widget(widget, widgets_list)', group = 'History')
        widgets_list.append(widget)
        y += 3
    y = 0
    for gender in GENDER_DATA.keys():
        
        widget = Widget.Checkbox(SCREEN_W/2+27, SCREEN_H/2+y, gender, eval(CONFIG_DATA['CHECKBOX']['NORMAL_COLOR']), eval(CONFIG_DATA['CHECKBOX']['LIGHT_COLOR']), 
                                 'select_widget(widget, widgets_list)', group = 'Gender')
        widgets_list.append(widget)
        y += 3
                            
    # Title.
    title = """
______ _                         _____                _   _             
| ___ \ |                       /  __ \              | | (_)            
| |_/ / | __ _ _   _  ___ _ __  | /  \/_ __ ___  __ _| |_ _  ___  _ __  
|  __/| |/ _` | | | |/ _ \ '__| | |   | '__/ _ \/ _` | __| |/ _ \| '_ \ 
| |   | | (_| | |_| |  __/ |    | \__/\ | |  __/ (_| | |_| | (_) | | | |
\_|   |_|\__,_|\__, |\___|_|     \____/_|  \___|\__,_|\__|_|\___/|_| |_|
                __/ |                                                   
               |___/                                                    

               """
    
    # LOOPAGE.
    while not lib.console_is_window_closed():
        
        # Clear screen.
        lib.console_set_default_background(0, lib.black)
        lib.console_clear(0)
    
        # Render title/race/history/gender.
        lib.console_set_default_foreground(0, eval(CONFIG_DATA['TEXT']['COLOR']))
        lib.console_print_ex(0, SCREEN_W/2+2, SCREEN_H/2-20, lib.BKGND_NONE, lib.CENTER, title)
        lib.console_print_ex(0, SCREEN_W/5, SCREEN_H/2-4, lib.BKGND_NONE, lib.CENTER, '-NAME-')
        lib.console_print_ex(0, SCREEN_W/2-12, SCREEN_H/2-4, lib.BKGND_NONE, lib.CENTER, '-RACE-')
        lib.console_print_ex(0, SCREEN_W/2+11, SCREEN_H/2-4, lib.BKGND_NONE, lib.CENTER, '-HISTORY-')
        lib.console_print_ex(0, SCREEN_W/2+34, SCREEN_H/2-4, lib.BKGND_NONE, lib.CENTER, '-GENDER-')
        
        # Render widgets.
        render_widgets(widgets_list)
        
        # Grab key events.
        mouse, key = check_for_key_events()
        
        # Display descriptions.
        for widget in widgets_list:
            
            if mouse.cx <= widget.x+7+len(widget.text) and mouse.cx >= widget.x+1 and mouse.cy <= widget.y+1 and mouse.cy >= widget.y-1:
                
                if widget.type == 'Checkbox':
                
                    if widget.group == 'Race':
                    
                        text = RACE_DATA[widget.text]['DESCRIPTION']
                
                    elif widget.group == 'History':
                    
                        text = HISTORY_DATA[widget.text]['DESCRIPTION']
                
                    else:
                    
                        text = GENDER_DATA[widget.text]['DESCRIPTION']
                
                    y = 1
                    text = textwrap.wrap(text, SCREEN_W-25)
                    for line in text:
                    
                        lib.console_set_default_foreground(0, eval(CONFIG_DATA['TEXT']['COLOR']))
                        lib.console_print_ex(0, 12, SCREEN_H-15+y, lib.BKGND_NONE, lib.LEFT, line)  
                        y += 1
                    
        # Flush *heh* screen.
        lib.console_flush()
        
        # Check if exit hotkey is pressed if so, exit to main menu.
        if key.c == eval(CONFIG_DATA['EXIT']['KEY']) or key.vk == eval(CONFIG_DATA['EXIT']['KEY']):
            
            break
        
        # Check and update widget status's.
        action = update_widgets_status(widgets_list, mouse, key)
                  
        # Start new game.
        if action == 'NEWGAME':
            
            num = 0
            
            while True:
                
                # Grab selections.
                for widget in widgets_list:
                
                    if widget.type == 'Input':
                    
                        name = widget.text
                
                    elif widget.type == 'Checkbox':
                    
                        if widget.group == 'Race' and widget.selected == True:
                        
                            race = widget.text
                            num += 1
                        
                        elif widget.group == 'History' and widget.selected == True:
                        
                            history = widget.text
                            num += 1
                        
                        elif widget.group == 'Gender' and widget.selected == True:
                        
                            gender = widget.text
                            num += 1
                
                # Randomize selections they are not selected.
                if num != 3:
                
                    randomize_selections(widgets_list)
                
                else:
                    
                    break
            
            # Choose random name if one is not given.
            if name == '':
                
                name = get_random_name(gender)
            
            # Start game.
            new_game(name, race, history, gender)
            play_game()
            break
        
        # Exit.
        if action == 'EXIT':
            
            break
                

def new_game(name, race, history, gender):
    """ Creates a new game. """
    
    # Set globals.
    global game_msgs, objects_list, widgets_list, player, turns, depth, aurum, locations_list, QUICK_SLOT, CURRENT_SLOT, LEFT_MOUSE_ACTION
    global player_race, player_history, player_gender
    
    # Game message container.
    game_msgs = []
    create_message('You come as you hear movement in the darkness and feel something warm running down your leg.', eval(CONFIG_DATA['MESSAGE']['WARNING']))
    
    # Fill widget container.
    widgets_list = [Widget.Button(SCREEN_W/2-20, 1, '1:', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                  eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'select_quick_slot(1)'),
                    Widget.Button(SCREEN_W/2-4, 1, '2:', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                  eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'select_quick_slot(2)'),
                    Widget.Button(SCREEN_W/2+12, 1, '3:', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                  eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'select_quick_slot(3)'),
                    Widget.Button(SCREEN_W-25, 1, 'Inventory', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                  eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'inventory_menu_handler()'),
                    Widget.Button(SCREEN_W-14, 1, 'Character', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                  eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'character_menu_handler()'),
                    Widget.Button(SCREEN_W-4, 1, 'Spells', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), 
                                  eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'spell_menu_handler()')]
                                  
    # Set the first quick slot to active.
    widgets_list[0].color = widgets_list[0].light_color
    
    # Quick slot widgets have a wider width.
    widgets_list[0].width += 11
    widgets_list[1].width += 11
    widgets_list[2].width += 11
    
    # Create player's components.
    living = Object.Living([10, 10], [100, 100], 0, 100, None)
    
    # Create player.
    player = Object.Object(1, 1, name, False, False, True, PLAYER_DATA['Player']['IMAGE'], eval(PLAYER_DATA['Player']['COLOR']), [], living = living)
    
    # Spells.
    player.living.spells = ['Fire Lance']
    
    # Race/gender/history.
    player_race = race
    player_history = history
    player_gender = gender
    
    # Reset turns, depth, aurum.
    turns = 0
    depth = 1
    aurum = 100
    
    # Locations.
    locations_list = []
    
    # Reset quick slot/mouse variables.
    QUICK_SLOT = {1:'', 2:'', 3:''}
    CURRENT_SLOT = 1
    LEFT_MOUSE_ACTION = 'MOVE'
    
    # Loading.
    lib.console_set_default_background(0, lib.black)
    lib.console_clear(0)
    lib.console_print_ex(0, SCREEN_W/2, SCREEN_H/2-2, lib.BKGND_NONE, lib.CENTER, 'LOADING...')
    lib.console_flush()
    
    # Create map.
    create_map()
    
    # Compute FOV.
    compute_fov()
    
       
def compute_fov():
    """ Computes FOV. """

    # Set globals.
    global fov_recompute, fov_map

    fov_recompute = True

    # Create FOV map.
    fov_map = lib.map_new(MAP_W, MAP_H)
    for y in range(MAP_H):

        for x in range(MAP_W):
           
            for obj in objects_list:
                
                if obj.x == x and obj.y == y:
                
                    lib.map_set_properties(fov_map, x, y, not obj.blocks_sight, not obj.solid)

    # Clear console.
    lib.console_clear(con)
    
    
def play_game():
    """ Starts the game. """
    
    # LOOPAGE.
    while not lib.console_is_window_closed():
    
        # Render everything.
        render_all()
        
        # Flush *heh* screen.
        lib.console_flush()
        
        # Clear objects.
        clear_objects()
        
        # Get players action.
        action = player_key_action()
        
        if action == 'TURN-TAKEN':
            
            move_objects()
            
        elif action == 'EXIT':
            
            break
        
        # If player dies, run player_death.
        if player.living.health[0] <= 0:
            
            exit = player_death(player.killedby)
            
            if exit == True:
                
                break
        
 
def main_menu():
    """ Starts main menu. """
        
    # Widget container.
    widgets_list = [Widget.Button(SCREEN_W/2, SCREEN_H/2-2, 'START GAME', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'create_player()'),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2+1, 'QUIT', eval(CONFIG_DATA['BUTTON']['NORMAL_COLOR']), eval(CONFIG_DATA['BUTTON']['LIGHT_COLOR']), 'EXIT')]
    
    # Title.
    title = """
        
 _____ _           ______               _   _ _   _                       
|_   _| |          | ___ \             | | (_) | (_)                      
  | | | |__   ___  | |_/ / __ __ _  ___| |_ _| |_ _  ___  _ __   ___ _ __ 
  | | | '_ \ / _ \ |  __/ '__/ _` |/ __| __| | __| |/ _ \| '_ \ / _ \ '__|
  | | | | | |  __/ | |  | | | (_| | (__| |_| | |_| | (_) | | | |  __/ |   
  \_/ |_| |_|\___| \_|  |_|  \__,_|\___|\__|_|\__|_|\___/|_| |_|\___|_|   
                                                                          
                                                                                                          
"""

    # LOOPAGE.
    while not lib.console_is_window_closed():
    
        # Clear screen.
        lib.console_set_default_background(0, lib.black)
        lib.console_clear(0)
        
        # Render title and build version.
        lib.console_set_default_foreground(0, eval(CONFIG_DATA['TEXT']['COLOR']))
        lib.console_print_ex(0, SCREEN_W/2+2, SCREEN_H/2-20, lib.BKGND_NONE, lib.CENTER, title)
        lib.console_print_ex(0, SCREEN_W/2, SCREEN_H/2-11, lib.BKGND_NONE, lib.CENTER, 'Build #2')
        
        # Render widgets.
        render_widgets(widgets_list)
        
        # Flush *heh* screen.
        lib.console_flush()
        
        # Grab key events.
        mouse, key = check_for_key_events()
        
        # Check if exit hotkey is pressed if so, exit.
        if key.c == eval(CONFIG_DATA['EXIT']['KEY']) or key.vk == eval(CONFIG_DATA['EXIT']['KEY']):
            
            break
        
        # Check and update widgets status's.
        exit = update_widgets_status(widgets_list, mouse, key)
        
        # Exit if needed.
        if exit:
            
            break

                
# Set font.
lib.console_set_custom_font(CONFIG_DATA['FONT']['FONT'], eval(CONFIG_DATA['FONT']['FONT_TYPE']) | eval(CONFIG_DATA['FONT']['FONT_LAYOUT']))

# Initiate main window.
lib.console_init_root(SCREEN_W, SCREEN_H, 'The Practitioner: Build #2', False)

# Set renderer.
lib.sys_set_renderer(lib.RENDERER_SDL)

# Set FPS limit.
lib.sys_set_fps(FPS_LIMIT)

# Create offscreen console.
con = lib.console_new(MAP_W, MAP_H)

# GUI consoles.
side_panel = lib.console_new(SIDE_PANEL_W, MSG_PANEL_H)
msg_panel = lib.console_new(MSG_PANEL_W, MSG_PANEL_H)

# Start game.
main_menu()