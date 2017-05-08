from pygame import *
from multiprocessing import *
import socket
import rahma
import menu
import pickle
import player


def player_sender(send_queue, server):
    print('Sender running...')

    while True:
        tobesent = send_queue.get()
        server.sendto(pickle.dumps(tobesent[0], protocol=4), tobesent[1])


def receive_message(message_queue, server):
    print('Ready to receive command...')

    while True:
        msg = server.recvfrom(16384)
        message_queue.put(pickle.loads(msg[0]))


def game(username):
    print('Starting game')

    def quit_game():
        send_queue.put(((9,), _server))
        time.wait(50)
        sender.terminate()
        receiver.terminate()

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _server = (host, port)

    send_queue = Queue()
    message_queue = Queue()

    wallpaper = transform.scale(image.load("textures/menu/wallpaper.png"), (955, 500))
    screen.blit(wallpaper, (0, 0))
    #rahma.text(screen, "Connecting to %s:%i..." % (host, port), rahma.center(0, 0, 800, 500, ))

    '''
    block_list = [block.split(' // ') for block in open('block').read().split('\n')]
    
    for index in range(len(block_list)):
        block_list[index][1] = list(map(int, block_list[index][1].split(', ')))
        block_list[index][2] = list(map(int, block_list[index][2].split(', ')))
    '''

    clock = time.Clock()

    print("Client connecting to %s:%i" % _server)

    server.sendto(pickle.dumps([0, username]), _server)

    sender = Process(target=player_sender, args=(send_queue, server))
    sender.start()

    receiver = Process(target=receive_message, args=(message_queue, server))
    receiver.start()

    while True:
        first_message = message_queue.get()
        if first_message == (400,):
            sender.terminate()
            receiver.terminate()
            return "login"
        elif first_message[0] == 0:
            break

    world_size_x, world_size_y, player_x, player_y, players = first_message[1:]

    world = np.array([[-1] * world_size_y for _ in range(world_size_x)])

    hotbar_slot = 1

    inventory = [[-1] * 6 for x in range(7)]

    _inventory_keys = {str(x) for x in range(1, 10)}

    TICKEVENT = USEREVENT + 1
    tickTimer = time.set_timer(TICKEVENT, 50)

    block_request = set()
    render_request = set()

    while True:
        on_tick = False
        for e in event.get():
            if e.type == QUIT:
                quit_game()
                return 'menu'

            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True

                elif e.button == 4:
                    inventory_slot = max(-1, inventory_slot - 1)

                    if inventory_slot == -1:
                        inventory_slot = 8

                elif e.button == 5:
                    inventory_slot = min(9, inventory_slot + 1)

                    if inventory_slot == 0:
                        inventory_slot =0

            elif e.type == MOUSEBUTTONUP and e.button == 1:
                release = True

            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    if paused:
                        paused = False
                    else:
                        paused = True

                elif not paused:
                    if e.key == K_t:
                        if advanced_graphics:
                            advanced_graphics = False
                        else:
                            advanced_graphics = True
                    elif e.unicode in _inventory_keys:
                        inventory_slot = int(e.unicode) - 1

            elif e.type == TICKEVENT:
                event.clear(TICKEVENT)
                invulnerabilityTimer = time.set_timer(TickEVENT, 50)

                on_tick = True
                current_tick += 1
                if current_tick == 20:
                    current_tick = 0






if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5175

    navigation = 'login'

    size = (800, 500)
    screen = display.set_mode(size)

    rahma.rah(screen)

    init()
    font.init()

    click_cursor = ["      ..                ",
                    "     .XX.               ",
                    "     .XX.               ",
                    "     .XX.               ",
                    "     .XX.               ",
                    "     .XX.               ",
                    "     .XX...             ",
                    "     .XX.XX...          ",
                    "     .XX.XX.XX.         ",
                    "     .XX.XX.XX...       ",
                    "     .XX.XX.XX.XX.      ",
                    "     .XX.XX.XX.XX.      ",
                    "...  .XX.XX.XX.XX.      ",
                    ".XX...XXXXXXXXXXX.      ",
                    ".XXXX.XXXXXXXXXXX.      ",
                    " .XXX.XXXXXXXXXXX.      ",
                    "  .XXXXXXXXXXXXXX.      ",
                    "  .XXXXXXXXXXXXXX.      ",
                    "   .XXXXXXXXXXXXX.      ",
                    "    .XXXXXXXXXXX.       ",
                    "    .XXXXXXXXXXX.       ",
                    "     .XXXXXXXXX.        ",
                    "     .XXXXXXXXX.        ",
                    "     ...........        "]

    click_cursor_data = ((24, 24), (7, 1), *cursors.compile(click_cursor))
    mouse.set_cursor(*cursors.tri_left)

    UI = {'login': login,
          'menu': menu,
          'about': about,
          'options': options,
          'assistance': assistance,
          'game': game,
          'server_picker': server_picker,
          'custom_server_picker': custom_server_picker,
          'local_server': local_server,
          'rahmish_server': rahmish_server}

    while navigation != 'exit':
        navigation = UI[navigation]()

    display.quit()
    raise SystemExit