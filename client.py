import pickle
import socket
from multiprocessing import *
import numpy as np
from pygame import *

host = ""
port = 0


def playerSender(sendQueue, server):
    print('Client running...')

    while True:
        tobesent = sendQueue.get()
        server.sendto(pickle.dumps(tobesent[0], protocol=4), tobesent[1])


def receiveMessage(messageQueue, server):
    print('Client is ready for connection!')

    while True:
        msg = server.recvfrom(16384)
        messageQueue.put(pickle.loads(msg[0]))


def draw_block(x, y, x_offset, y_offset, block_size, colour, colourIn, screen):
    draw.rect(screen, colour, (x - x_offset % 20, y - y_offset % 20, block_size, block_size))
    draw.rect(screen, colourIn, (x - x_offset % 20, y - y_offset % 20, block_size, block_size), 1)


def get_neighbours(x, y, world):
    return [world[x + 1, y], world[x - 1, y], world[x, y + 1], world[x, y - 1]]


def center(x, y, canvas_w, canvas_h, object_w, object_h):
    return (x + canvas_w // 2 - object_w // 2, y + canvas_h // 2 - object_h // 2)


class Button:
    def __init__(self, x, y, w, h, function, text):
        self.rect = Rect(x, y, w, h)
        self.text = text
        self.function = function


    def highlight(self):
        button_hover = transform.scale(image.load("textures/menu/button_hover.png"), (self.rect.w, self.rect.h))
        screen.blit(button_hover, (self.rect.x, self.rect.y))

    def mouse_down(self):
        button_pressed = transform.scale(image.load("textures/menu/button_pressed.png"), (self.rect.w, self.rect.h))
        screen.blit(button_pressed, (self.rect.x, self.rect.y))

    def idle(self):
        button_idle = transform.scale(image.load("textures/menu/button_idle.png"), (self.rect.w, self.rect.h))
        screen.blit(button_idle, (self.rect.x, self.rect.y))

    def update(self, mx, my, mb, size, unclick):

        minecraft_font = font.Font("fonts/minecraft.ttf", size)

        if self.rect.collidepoint(mx, my):
            if unclick:
                return self.function

            if mb[0] == 1:
                self.mouse_down()

            else:
                self.highlight()

        else:
            self.idle()

        text_surface = minecraft_font.render(self.text, True, (255, 255, 255))
        text_shadow = minecraft_font.render(self.text, True, (0, 0, 0))
        shadow_surface = Surface((text_surface.get_width(), text_surface.get_height()))
        shadow_surface.blit(text_shadow, (0, 0))
        shadow_surface.set_alpha(100)
        textPos = center(self.rect.x, self.rect.y, self.rect.w, self.rect.h, text_surface.get_width(), text_surface.get_height())
        screen.blit(text_shadow, (textPos[0] + 2, textPos[1] + 2))
        screen.blit(text_surface, textPos)


def menu():
    clock = time.Clock()

    wallpaper = transform.scale(image.load("textures/menu/wallpaper.png"), (955, 500))
    screen.blit(wallpaper, (0, 0))

    logo = transform.scale(image.load("textures/menu/logo.png"), (301, 51))
    screen.blit(logo, (400 - logo.get_width() // 2, 100))

    button_list = []

    button_list.append(Button(200, 175, 400, 40, 'server_picker', "Connect to server"))
    button_list.append(Button(200, 225, 400, 40, 'help', "Help"))
    button_list.append(Button(200, 275, 400, 40, 'options', "Options"))
    button_list.append(Button(200, 325, 195, 40, 'about', "About"))
    button_list.append(Button(404, 325, 195, 40, 'exit', "Exit"))

    while True:

        click = False
        unclick = False

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                click = True

            if e.type == MOUSEBUTTONUP and e.button == 1:
                unclick = True


        else:

            mx, my = mouse.get_pos()
            mb = mouse.get_pressed()

            for button in button_list:
                nav_update = button.update(mx, my, mb, 10, unclick)

                if nav_update != None:
                    return nav_update

            clock.tick(120)
            display.update()

            continue

        break


def server_picker():

    global host,port

    clock = time.Clock()

    wallpaper = transform.scale(image.load("textures/menu/wallpaper.png"), (955, 500))
    screen.blit(wallpaper, (0, 0))

    with open("config", "r") as config:
        config = config.read().split("\n")
        host = config[0]
        port = int(config[1])

    normal_font = font.Font("fonts/Text font.ttf", 14)

    IpText = normal_font.render("IP address", True, (255, 255, 255))
    PortText = normal_font.render("Port", True, (255, 255, 255))
    sizeChar = normal_font.render("SHZ", True, (255, 255, 255))

    ipfieldRect = (size[0] // 2 - 150, size[1] // 2 - 100, 300, 40)
    portRect = (size[0] // 2 - 150, size[1] // 2 - 30, 300, 40)

    fields = {"ip":"",
              "port": ""}

    currentField = "none"
    allowed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4',
               '5', '6', '7', '8', '9', '!', '"', '#', '$', '%', '&', "\\", "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', "'", "'"]

    currentField = "ip"

    button_list = []

    button_list.append(Button(200, 370, 400, 40, 'menu', "Back"))
    button_list.append(Button(200, 320, 400, 40, 'game', "Connect to server"))

    while True:
        click = False
        unclick = False

        for e in event.get():
            if e.type == QUIT:
                return 'exit'
            if e.type == KEYDOWN:
                if e.unicode in allowed:
                    fields[currentField] += e.unicode
                elif e.key == K_RETURN:
                    inputField = "none"
                elif e.key == K_BACKSPACE:
                    try:
                        fields[currentField] = fields[currentField][:-1]
                    except:
                        pass

            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                click = True

            if e.type == MOUSEBUTTONUP and e.button == 1:
                unclick = True


        screen.blit(IpText, (ipfieldRect[0], ipfieldRect[1] - IpText.get_height() - 2))
        screen.blit(PortText, (portRect[0], portRect[1] - PortText.get_height()))
        draw.rect(screen, (0, 0, 0), ipfieldRect)
        draw.rect(screen, (151, 151, 151), ipfieldRect, 2)
        draw.rect(screen, (0, 0, 0), portRect)
        draw.rect(screen, (151, 151, 151), portRect, 2)

        screen.blit(normal_font.render(fields["ip"], True, (255, 255, 255)), (ipfieldRect[0] + 3, ipfieldRect[1] + ipfieldRect[3] // 2 - sizeChar.get_height() // 2))
        screen.blit(normal_font.render(fields["port"], True, (255, 255, 255)), (portRect[0] + 3, portRect[1] + portRect[3] // 2 - sizeChar.get_height() // 2))

        mx, my = mouse.get_pos()
        ml, mm, mr = mouse.get_pressed()
        mb = mouse.get_pressed()

        for button in button_list:
            nav_update = button.update(mx, my, mb, 10, unclick)

            if nav_update != None:
                return nav_update

        if  Rect(ipfieldRect).collidepoint(mx, my) and ml == 1:
            currentField = "ip"

        elif Rect(portRect).collidepoint(mx, my) and ml == 1:
            currentField = "port"

        elif ml == 1:
            inputField = "none"

        clock.tick(120)

        display.flip()

def help():
    clock = time.Clock()

    wallpaper = transform.scale(image.load("textures/menu/wallpaper.png"), (955, 500))
    screen.blit(wallpaper, (0, 0))

    back_button = Button(200, 370, 400, 40, 'menu', "Back")

    while True:

        click = False
        unclick = False

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                click = True

            if e.type == MOUSEBUTTONUP and e.button == 1:
                unclick = True

        else:

            mx, my = mouse.get_pos()
            mb = mouse.get_pressed()

            nav_update = back_button.update(mx, my, mb, 10, unclick)

            if nav_update != None:
                return nav_update

            clock.tick(120)
            display.update()

            continue

        break


def about():
    clock = time.Clock()

    wallpaper = transform.scale(image.load("textures/menu/wallpaper.png"), (955, 500))
    screen.blit(wallpaper, (0, 0))

    back_button = Button(200, 370, 400, 40, 'menu', "Back")

    while True:

        click = False
        unclick = False

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                click = True

            if e.type == MOUSEBUTTONUP and e.button == 1:
                unclick = True

        else:

            mx, my = mouse.get_pos()
            mb = mouse.get_pressed()

            nav_update = back_button.update(mx, my, mb, 10, unclick)

            if nav_update != None:
                return nav_update

            clock.tick(120)
            display.update()

            continue

        break



def options():
    clock = time.Clock()

    wallpaper = transform.scale(image.load("textures/menu/wallpaper.png"), (955, 500))
    screen.blit(wallpaper, (0, 0))

    back_button = Button(200, 370, 400, 40, 'menu', "Back")

    while True:

        click = False
        unclick = False

        for e in event.get():
            if e.type == QUIT:
                return 'exit'

            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                click = True

            if e.type == MOUSEBUTTONUP and e.button == 1:
                unclick = True

        else:

            mx, my = mouse.get_pos()
            mb = mouse.get_pressed()

            nav_update = back_button.update(mx, my, mb, 10, unclick)

            if nav_update != None:
                return nav_update

            clock.tick(120)
            display.update()

            continue

        break



def game():

    global host,port

    sendQueue = Queue()
    messageQueue = Queue()

    wallpaper = transform.scale(image.load("textures/menu/wallpaper.png"), (955, 500))
    screen.blit(wallpaper, (0, 0))

    minecraft_font = font.Font("fonts/minecraft.ttf", 30)

    text_surface = minecraft_font.render("Connecting to %s:%i..." % (host, port), True, (255, 255, 255))
    text_shadow = minecraft_font.render("Connecting to %s:%i..." % (host, port), True, (0, 0, 0))
    shadow_surface = Surface((text_surface.get_width(), text_surface.get_height()))
    shadow_surface.blit(text_shadow, (0, 0))
    shadow_surface.set_alpha(100)
    textPos = center(0, 0, 800, 500, text_surface.get_width(),
                     text_surface.get_height())
    screen.blit(text_shadow, (textPos[0] + 2, textPos[1] + 2))
    screen.blit(text_surface, textPos)

    display.flip()

    clock = time.Clock()

    block_size = 20
    y_offset = 10 * block_size
    x_offset = 5000 * block_size

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Client connecting to %s:%i" % (host, port))

    server.sendto(pickle.dumps([0, 'Henry']), (host, port))

    sender = Process(target=playerSender, args=(sendQueue, server))
    sender.start()

    receiver = Process(target=receiveMessage, args=(messageQueue, server))
    receiver.start()

    Worldsize = messageQueue.get()

    world = np.array([[-1 for y in range(Worldsize[1])] for x in range(Worldsize[0])])

    updated = False

    sendQueue.put([[2, x_offset // block_size, y_offset // block_size], (host, port)])
    wmsg = messageQueue.get()
    world[wmsg[1] - 5:wmsg[1] + 45, wmsg[2] - 5:wmsg[2] + 31] = np.array(wmsg[3], copy=True)
    block_Select = 1

    block_highlight = Surface((block_size, block_size))
    block_highlight.fill((255, 255, 0))
    block_highlight.set_alpha(100)

    while True:
        updated = False
        for e in event.get():
            if e.type == QUIT:
                sender.terminate()
                receiver.terminate()

                return 'menu'

            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4:
                    block_Select = min(3, block_Select + 1)

                elif e.button == 5:
                    block_Select = max(0, block_Select - 1)



        else:
            display.set_caption("Minecrap Beta v0.01 FPS: " + str(round(clock.get_fps(), 2)) + " X: " + str(
                x_offset // block_size) + " Y:" + str(y_offset // block_size) + " Size:" + str(
                block_size) + "Block Selected:" + str(block_Select))

            keys = key.get_pressed()

            if keys[K_d] and x_offset // block_size < 9950:
                x_offset += 60 // block_size
                updated = True
            elif keys[K_a] and x_offset // block_size > 0:
                x_offset -= 60 // block_size
                updated = True

            if keys[K_w] and y_offset // block_size > 5:
                y_offset -= 80 // block_size
                updated = True
            elif keys[K_s] and y_offset // block_size < 70:
                y_offset += 80 // block_size
                updated = True

            DispingWorld = world[x_offset // block_size:x_offset // block_size + 41,
                           y_offset // block_size:y_offset // block_size + 26]
            updateCost = DispingWorld.flatten()
            updateCost = np.count_nonzero(updateCost == -1)

            if updated and updateCost > 3:
                sendQueue.put([[2, x_offset // block_size, y_offset // block_size], (host, port)])

            # screen.fill((0,0,255))

            try:
                wmsg = messageQueue.get_nowait()
                if wmsg[0] == 2:
                    world[wmsg[1] - 5:wmsg[1] + 45, wmsg[2] - 5:wmsg[2] + 31] = np.array(wmsg[3], copy=True)
                elif wmsg[0] == 3:
                    world[wmsg[1], wmsg[2]] = 0
                elif wmsg[0] == 4:
                    world[wmsg[1], wmsg[2]] = wmsg[3]
            except:
                pass

            mb = mouse.get_pressed()

            mx, my = mouse.get_pos()

            if mb[0] == 1:
                if world[(mx + x_offset) // block_size, (my + y_offset) // block_size] != 0:
                    sendQueue.put([[3, (mx + x_offset) // block_size, (my + y_offset) // block_size], (host, port)])
            if mb[2] == 1:
                if world[(mx + x_offset) // block_size, (my + y_offset) // block_size] == 0 and sum(
                        get_neighbours((mx + x_offset) // block_size, (my + y_offset) // block_size, world)) > 0:
                    sendQueue.put(
                        [[4, (mx + x_offset) // block_size, (my + y_offset) // block_size, block_Select], (host, port)])

            # print((mx + x_offset) // block_size, (my + y_offset) // block_size)

            for y in range(500):
                draw.line(screen, (max(30 - y, 0), max(144 - y, 100), max(255 - y, 100)), (0, y), (800, y))

            # Clear the screen
            # Redraw the level onto the screen
            for x in range(0, 821, block_size):  # Render blocks
                for y in range(0, 521, block_size):
                    if world[(x + x_offset) // block_size][(y + y_offset) // block_size] == 1:
                        draw_block(x, y, x_offset, y_offset, block_size, (0, 150, 0), (0, 100, 0), screen)

                    elif world[(x + x_offset) // block_size][(y + y_offset) // block_size] == 2:
                        draw_block(x, y, x_offset, y_offset, block_size, (129, 68, 32), (99, 38, 12), screen)

                    elif world[(x + x_offset) // block_size][(y + y_offset) // block_size] == 3:
                        draw_block(x, y, x_offset, y_offset, block_size, (150, 150, 150), (100, 100, 100), screen)

            clock.tick(120)
            display.update()
            continue

        break


if __name__ == '__main__':

    navigation = 'menu'

    display.set_caption("Nothing here")
    size = (800, 500)
    screen = display.set_mode((800, 500))

    font.init()

    while navigation != 'exit':
        if navigation == 'menu':
            navigation = menu()
        if navigation == 'server_picker':
            navigation = server_picker()
        if navigation == 'about':
            navigation = about()
        if navigation == 'options':
            navigation = options()
        if navigation == 'help':
            navigation = help()
        if navigation == 'game':
            navigation = game()

    display.quit()
    raise SystemExit
