"""
This file contains convenience functions used several times in our game. they range from graphics centering to screen
prep.

Main Rahmish Developers: Henry Tu & Syed Safwaan
"""

# Modules to import
from pygame import *  # to allow use of graphics
from random import *  # to allow use of random generators
from math import *  # to allow use of trigonometric functions

# Function to control printing in game code (purely for dev purposes)
def rahprint(*text):
    """ A general convenience print statement used for debugging. """

    # Boolean to evaluate whether printing is wanted
    printing = False  # must be manually changed in file

    # If user wants to print, stuff gets printed
    if printing:
        print(*text)


# Function to create loading screen
def rah_screen(screen):
    """ Creates a Rahmish loading screen. """

    # Fill the screen with red (commie red)
    screen.fill((212, 0, 0))

    # Generate logo image and text
    logo = transform.scale(image.load('textures/menu/rahcraftdev.png'), (200, 200))  # load image
    logo_font = font.Font("fonts/Lato-Black.ttf", 60)  # load Font object
    logo_text = logo_font.render("RAHCRAFT DEV", True, (255, 204, 0))  # render the text

    # Blit the logo and text to the screen
    screen.blit(logo,
                center(-10, -50, screen.get_width(), screen.get_height(), logo.get_width(), logo.get_height()))
    screen.blit(logo_text, center(0, 100, screen.get_width(), screen.get_height(), logo_text.get_width(),
                                  logo_text.get_height()))

    # Update the screen to display the Rahmish screen
    display.update()


# Function to size wallpaper in background
def wallpaper(screen, size):
    """ Resizes wallpaper in menu background. """

    # Fill the screen with black to clear it
    screen.fill((0, 0, 0))

    # Check to see which axis to scale on

    if size[0] < size[1]:  # if width is greater than height

        # Scale up according to x-axis
        wpw = size[0]
        wph = int(500 / 955 * size[0])

    else:  # if height is greater than width

        # Scale up according to height
        wph = size[1]
        wpw = int(955 / 500 * size[1])

    # Load wallpaper and scale it according to the values made above
    wallpaper = transform.scale(image.load("textures/menu/wallpaper.png"), (wpw, wph))

    # Blit the wallpaper to the screen
    screen.blit(wallpaper, (0, 0))


# Function to make Minecraft-style text
def text(text, size):
    """ Generates and returns Minecraft-style text. """

    # Load the Minecraft Font object
    minecraft_font = font.Font("fonts/minecraft.ttf", size)

    # Make the background and surface text
    text_surface = minecraft_font.render(text, True, (255, 255, 255))  # surface text
    text_shadow = minecraft_font.render(text, True, (0, 0, 0))  # background text

    # Create the surfaces for blitting and blit to them
    shadow_surface = Surface((text_surface.get_width(), text_surface.get_height()))  # create surface
    shadow_surface.blit(text_shadow, (0, 0))  # blit text shadow to surface
    shadow_surface.set_alpha(100)  # make text shadow surface slightly transparent

    # Create the master text surface
    text_surface_final = Surface((text_surface.get_width() + 2, text_surface.get_height() + 2), SRCALPHA)

    # Blit the text shadow and text surface to the master surface
    text_surface_final.blit(text_shadow, (2, 2))  # text shadow
    text_surface_final.blit(text_surface, (0, 0))  # text surface

    # Return the final surface for use in the outer scope
    return text_surface_final


# Function to load and play sound immediately
def load_sound(sound_list):
    """ Loads and plays a sound instantly. """

    # Load the sound as a Sound object
    sound_object = mixer.Sound(choice(sound_list))

    # Play the sound
    sound_object.play(0)


# Function to center a surface on another surface
def center(x, y, canvas_w, canvas_h, object_w, object_h):
    """ Returns a positional tuple that will centre a surface on another surface. """

    # Do some math and return a positional tuple for use in the outer scope
    return x + canvas_w // 2 - object_w // 2, y + canvas_h // 2 - object_h // 2


# Function to center a surface on a given point
def point_center(point_x, point_y, object_w, object_h):
    """ Returns a positional tuple that will centre a surface on a point. """

    # Do some more math and return a positional tuple for use in the outer scope
    return point_x - (object_w // 2), point_y - (object_h // 2)


# Function to centrally rotate a surface
def joint_rotate(surf, angle):
    """ Returns a rotated surface independent of the original supplied surface. """

    # Create a copy of the supplied surface
    new_surf = surf.copy()

    # Return the rotated copy to the outer scope
    return transform.rotate(new_surf, -degrees(angle))
