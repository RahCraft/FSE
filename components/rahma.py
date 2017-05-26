import time as t
from pygame import *
from random import *

def install_modules():
    try:
        import numpy as np

    except ImportError:
        print("Module Numpy wasn't found")
        try:
            if platform.system() == "Windows":
                Popen(['cmd.exe', 'python -m pip install numpy'])
                print("Numpy installed successfully")
            else:
                bash_command = "pip3 install numpy"
                Popen(split(bash_command), stdout=PIPE)
                print("Numpy installed successfully")
        except:
            print("Failed to install numpy")
            quit()

def load_sound(sound_list):
    sound_object = mixer.Sound(choice(sound_list))
    sound_object.play(0)

def rahprint(text):
    printing = False

    if printing:
        print(text)

def center(x, y, canvas_w, canvas_h, object_w, object_h):
    return x + canvas_w // 2 - object_w // 2, y + canvas_h // 2 - object_h // 2


def rah(screen):
    screen.fill((255, 255, 255))
    splash = image.load('textures/menu/splash.png')
    screen.blit(splash, center(0, 0, 800, 500, splash.get_width(), splash.get_height()))
    display.flip()

    t.sleep(0.1)


def wallpaper(screen, size):
    if size[0] < size[1]:
        wpw = size[0]
        wph = int(500 / 955 * size[0])

    else:
        wph = size[1]
        wpw = int(955 / 500 * size[1])

    wallpaper = transform.scale(image.load("textures/menu/wallpaper.png"), (wpw, wph))
    screen.blit(wallpaper, (0, 0))


def text(text, size):
    minecraft_font = font.Font("fonts/minecraft.ttf", size)
    text_surface = minecraft_font.render(text, True, (255, 255, 255))
    text_shadow = minecraft_font.render(text, True, (0, 0, 0))

    shadow_surface = Surface((text_surface.get_width(), text_surface.get_height()))
    shadow_surface.blit(text_shadow, (0, 0))
    shadow_surface.set_alpha(100)

    text_surface_final = Surface((text_surface.get_width() + 2, text_surface.get_height() + 2), SRCALPHA)

    text_surface_final.blit(text_shadow, (2, 2))
    text_surface_final.blit(text_surface, (0, 0))

    return text_surface_final
