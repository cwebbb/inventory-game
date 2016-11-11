import curses
import copy
import time
import random
import os

print("\x1b[8;150;200t")  # This print line enlarges terminal to chosen size

# All of the stuff needs to be activated for curses. Read more: https://docs.python.org/3/howto/curses.html
stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)
curses.curs_set(False)

level = 0
level_change = 0


# TU MAMY PARY KOLORÓW POTRZEBNYCH DO KOLOROWANIE curses.init_pair (a, b, c) gdzie a - numer pary, b - kolor znaku, c - kolor tła
# NUMERY KOLORÓW Z PLIKU KTÓRY WYŚLĘ! PRZYKŁAD UŻYCIA - PATRZ LINIJKA 153
curses.init_color(0, 0, 0, 0)# RGB COLOR FOR BLACK

curses.init_pair(1, 9, -1)
curses.init_pair(2, curses.COLOR_BLUE, -1)
curses.init_pair(3, 0, 186)# kolor body invenory
curses.init_pair(4, curses.COLOR_BLACK, -1)

#shades of green
green = [47, 48, 49, 11, 198, curses.COLOR_GREEN]
green2 = [83, 84, 77, 78]
get_random_greens = []
get_random_greens2 = []
green_add = 0
for item in green:
    curses.init_pair(5 + green_add, item, -1)
    get_random_greens.append(green_add+5)
    green_add += 1

curses.init_pair(12, 186, -1)

green_add = 0
for item in green2:
    curses.init_pair(13 + green_add, item, -1)
    get_random_greens2.append(green_add + 13)
    green_add += 1

curses.init_pair(30, 21, -1)# blue for waves
curses.init_pair(100, 247, -1)# grey
curses.init_pair(101, curses.COLOR_RED, -1)


board = [['🔰'] * 50 for x in range(51)]
# inv = {'key': 0, 'gold coin': 42, 'dagger': 1, 'arrow': 12, 'diamond of wisdom': 1
inv = {'key': 0, 'diamond of wisdom':0, 'iron ore': 0}
items = {'diamond of wisdom': (20, 5), 'key': (100, 1), 'iron ore': (20, 5)}

for i in range(2, 49):
    for y in range(2, 48):
        board[i][y] = " "

board_copy = copy.deepcopy(board)

loot = 0
item1 = 0

reachable_symbols = [' ', '💎','📛', '🏡', '🗝', '⛩', '🕍', '🐲']

# 👹
def menu():

    logo = [("                                  /   \       "),
    (" _                        )      ((   ))     ("),
    ("(@)                      /|\      ))_((     /|\\"),
    ("|-|                     / | \    (/\|/\)   / | \                             (@)"),
    ("| |--------------------/--|-voV---\`|'/--Vov-|--\----------------------------|-|"),
    ("|-| _                      _'^`   (o|o)  '^`                                 | |"),
    ("| |(_)_ ____   _____ _ __ | |_ ___`v_v'_ _   _    __ _  __ _ _ __ ___   ___  |-|"),
    ("|-|| | '_ \ \ / / _ \ '_ \| __/ _ \| '__| | | |  / _` |/ _` | '_ ` _ \ / _ \ | |"),
    ("| || | | | \ V /  __/ | | | || (_) | |  | |_| | | (_| | (_| | | | | | |  __/ |-|"),
    ("|-||_|_| |_|\_/ \___|_| |_|\__\___/|_|   \__, |  \__, |\__,_|_| |_| |_|\___| | |"),
    ("| |                                                                          |-|"),
    ("|_|_________________________________________________________________________ | |"),
    ("(@)              l   /\ /         ( (       \ /\   l                       `\|-|"),
    ("                 l /   V           \ \       V   \ l                         (@)"),
    ("                 l/                _) )_          \I"),
    ("                                   `\ /'"),
    ("                                     v")]

    menu_text = ["¸,ø¤º°`°º¤ø,¸¸,ø¤º° START: PRESS 1 °º¤ø,¸¸,ø¤º°`°º¤ø,¸ ", "¸,ø¤º°`°º¤ø,¸¸,ø¤º°HELP: PRESS 2°º¤ø,¸¸,ø¤º°`°º¤ø,¸",
                "¸,ø¤º°`°º¤ø,¸¸,ø¤º°CREDITS: PRESS 3°º¤ø,¸¸,ø¤º°`°º¤ø,¸"]

    for i in range(len(logo)):
        stdscr.addstr(i, int(dims[1] * 1/2 - 40), logo[i], curses.color_pair(1))
    for i in range(len(menu_text)):
        stdscr.addstr(len(logo) + 2* i, int(dims[1]/2 - 1/2 * len(menu_text[i])), menu_text[i] + '\n')


def help():
    logo = [" _   _  _____ _     ______",
            "| | | ||  ___| |    | ___ \_",
            "| |_| || |__ | |    | |_/ (_)",
            "|  _  ||  __|| |    |  __/",
            "| | | || |___| |____| |    _",
            "\_| |_/\____/\_____/\_|   (_)"]

    menu_text = ['\n', "the game is about walking and collecting stuff", "It is really cool", "believe me "]

    for i in range(len(logo)):
        stdscr.addstr(i, int(dims[1] * 1/2 - 1/2 * len(max(logo, key=len))), logo[i], curses.color_pair(1))
    for i in range(len(menu_text)):
        stdscr.addstr(len(logo) + 2 * i, int(dims[1]/2 - 1/2 * len(menu_text[i])), menu_text[i] + '\n')

    stdscr.addstr(len(logo) + 2 * len(menu_text), 30, "MAIN MENU: PRESS B")

def credits():
    logo = [" _____ ______ ___________ _____ _____ _____  ",
            "/  __ \| ___ \  ___|  _  \_   _|_   _/  ___|_ ",
            "| /  \/| |_/ / |__ | | | | | |   | | \ `--.(_)",
            "| |    |    /|  __|| | | | | |   | |  `--. \\",
            "| \__/\| |\ \| |___| |/ / _| |_  | | /\__/ /_",
            " \____/\_| \_\____/|___/  \___/  \_/ \____/(_)"]

    menu_text = ['\n', 'Authors of this beautiful game:', '°·.¸.·°¯°·.¸.·°¯°·.¸.->Paweł Kazmierski<-.¸.·°¯°·.¸.·°¯°·.¸.·°', '°·.¸.·°¯°·.¸.·°¯°·.¸.->Michał Kobiec<-.¸.·°¯°·.¸.·°¯°·.¸.·°',
                '°·.¸.·°¯°·.¸.·°¯°·.¸.-> Marcin Kieś<-.¸.·°¯°·.¸.·°¯°·.¸.·°']

    for i in range(len(logo)):
        stdscr.addstr(i, int(dims[1] * 1/2 - 1/2 * len(max(logo, key=len))), logo[i], curses.color_pair(1))
    for i in range(len(menu_text)):
        stdscr.addstr(len(logo) + 2 * i, int(dims[1]/2 - 1/2 * len(menu_text[i])), menu_text[i] + '\n')

    stdscr.addstr(len(logo) + 2 * len(menu_text), 30, "MAIN MENU: PRESS B")


def print_inventory(inventory, items):

    """Prints inventory and sum of all items"""
    logo =["|--------------------------------------------------------------------|",
           "|               ___                 _                _               |",
           "| /\_./o__ ||  |_ _|_ ___ _____ _ _| |_ ___ _ _ _  _(_) ||  __o\._/\\ |",
           "| (/^/(_^^'||   | |  ' \ V / -_) ' \  _/ _ \ '_| || |_  || '^^_)\^\) |",
           "|_.(_.)_   ||  |___|_||_\_/\___|_||_\__\___/_|  \_, (_) ||   _(._)._.|",
           "|                                               |__/                 |",
           "|--------------------------------------------------------------------|"]

    inventory_body =["|--------------------------------------------------------------------|"] + ["|                                                                    |"] * 35 + ["|--------------------------------------------------------------------|"]

    message_board = ["|MESSAGE-BOARD---------------------------------------------------|"] + ["|                                                                |"] * 5+ ["|----------------------------------------------------------------|"]






    # logo = ["""@@@@@@@@@@@@@@@@@@@@@**^^""~~~"^@@^*@*@@**@@@@@@@@@""",
    #         """@@@@@@@@@@@@@*^^'"~   , - ' '; ,@@b. '  -e@@@@@@@@@""",
    #         """@@@@@@@@*^"~      . '     . ' ,@@@@(  e@*@@@@@@@@@@""",
    #         """@@@@@^~         .       .   ' @@@@@@, ~^@@@@@@@@@@@""",
    #         """@@@~ ,e**@@*e,  ,e**e, .    ' '@@@@@@e,  "*@@@@@'^@""",
    #         """@',e@@@@@@@@@@ e@@@@@@       ' '*@@@@@@    @@@'   0""",
    #         """@@@@@@@@@@@@@@@@@@@@@',e,     ;  ~^*^'    ;^~   ' 0""",
    #         """@@@@@@@@@@@@@@@^""^@@e@@@   .'           ,'   .'  @""",
    #         """@@@@@@@@@@@@@@'    '@@@@@ '         ,  ,e'  .    ;@""",
    #         """@@@@@@@@@@@@@' ,&&,  ^@*'     ,  .  i^"@e, ,e@e  @@""",
    #         """@@@@@@@@@@@@' ,@@@@,          ;  ,& !,,@@@e@@@@ e@@""",
    #         """@@@@@,~*@@*' ,@@@@@@e,   ',   e^~^@,   ~'@@@@@@,@@@""",
    #         """@@@@@@, ~" ,e@@@@@@@@@*e*@*  ,@e  @@""@e,,@@@@@@@@@""",
    #         """@@@@@@@@ee@@@@@@@@@@@@@@@" ,e@' ,e@' e@@@@@@@@@@@@@""",
    #         """@@@@@@@@@@@@@@@@@@@@@@@@" ,@" ,e@@e,,@@@@@@@@@@@@@@""",
    #         """@@@@@@@@@@@@@@@@@@@@@@@~ ,@@@,,0@@@@@@@@@@@@@@@@@@@""",
    #         """@@@@@@@@@@@@@@@@@@@@@@@@,,@@@@@@@@@@@@@@@@@@@@@@@@@"""]

    for i in range(len(logo)):
        stdscr.addstr(1 + i, 3, logo[i], curses.color_pair(3))

    for i in range(len(inventory_body)):
        stdscr.addstr(3 + i + len(logo), 3, inventory_body[i], curses.color_pair(3))

    # stdscr.addstr(40, 20, str(len(max(logo, key=len))))

    printLine = 10 + len(logo)
    # goes through all keys and values(items and quantities) in inventory and
    # prints them
    if inventory:
        for item, quantity in inventory.items():
            stdscr.addstr(printLine, int(len(inventory_body[0])/2) - 4, "{}: {} ".format(quantity, item), curses.color_pair(3) )
            printLine += 1

        total_quantity = sum(inv.values())
        total_weight = 0
        total_value = 0
        messages = ["Total number of items:  .", "Total value of items:   vodka bottles.", "Total weight of items:{} horse shites."]
        for e in inv:
            total_value += items[e][0] * inv[e]
            total_weight += items[e][1] * inv[e]

        stdscr.addstr(printLine + 1, int(len(inventory_body[0])/2) - len(messages[0])//2, "Total number of items: {}.".format(total_quantity), curses.color_pair(3))
        stdscr.addstr(printLine + 2, int(len(inventory_body[0])/2) - len(messages[1])//2, "Total value of items: {} vodka bottles.".format(total_value), curses.color_pair(3))
        stdscr.addstr(printLine + 3, int(len(inventory_body[0])/2) - len(messages[2])//2, "Total weight of items: {} horse shites.".format(total_weight), curses.color_pair(3))

    for i in range(len(message_board)):
        stdscr.addstr(i + int(len(inventory_body[0])/2) + 3, 5, message_board[i], curses.color_pair(3))

    # stdscr.addstr(41, 35, str(get_random_greens), curses.color_pair(3))

def spawn_objects(number_of_items, symbol):
    local_board = copy.deepcopy(board)
    for i in range (number_of_items):
        while True:
            random_x = random.randint(3, 40)
            random_y = random.randint(3, 40)
            if local_board[random_x][random_y] == ' ':
                local_board[random_x][random_y] = symbol
                break
    return local_board

def make_board(size):
    number_of_obstacles = 30
    board = []
    border_size = 2
    path_size = 3           #no obstacles touching the border
    border = ('⛰', '🗻', '🌊')
    obstacles = ('🌵', '🔥', '🌴', '🌲')
    border_select = random.choice(border)
    for i in range(0, size):
        i = [border_select] * size
        board.append(i)
    for i in range (0+border_size, size-border_size):
        for j in range (0+border_size, size-border_size):
            board[i][j] = '🌳'

    count = 0
    while count < 100:                                  #render single obstacles on board
        coordinates = {'x': 0, 'y': 0}
        for e in coordinates:
            coordinates[e] = random.randrange(0+border_size, size - border_size)
        board[coordinates['x']][coordinates['y']] = random.choice(obstacles)
        count += 1

    count = 0
    obstacles += (border_select,)
    while count <= number_of_obstacles:                 #render group obstacles on board
        obstacle_type = random.choice(obstacles)

        start_point_x = random.randrange(0 + border_size + path_size, size-border_size-path_size)
        start_point_y = random.randrange(0 + border_size + path_size, size-border_size-path_size)

        size_h = random.randrange(5, 10)
        size_v = random.choice((size_h, random.randrange(10, 15)))

        end_point_x = min(start_point_x + size_h, size-border_size-path_size)
        end_point_y = min(start_point_y + size_v, size-border_size-path_size)

        for e in range(start_point_x, end_point_x):
            for i in range(start_point_y, end_point_y):
                board[e][i] = obstacle_type
        count += 1



## JESTEM KURWA GENIUSZEM
    old_number_of_roads = 0
    new_number_of_roads = 1
    iteration = 0
    board[47][25] = ' '

    while old_number_of_roads != new_number_of_roads:
        old_number_of_roads = new_number_of_roads
        for i in range(len(board)):
            for p in range(len(board[i])):
                if board[i][p] == ' ':
                    if board[i][p-1] == '🌳':
                        board[i][p-1] = ' '
                        new_number_of_roads = 1
                        old_number_of_roads = 0
                    if board[i][p+1] == '🌳':
                        new_number_of_roads = 1
                        old_number_of_roads = 0
                        board[i][p+1] = ' '
                    if board[i-1][p] == '🌳':
                        new_number_of_roads = 1
                        old_number_of_roads = 0
                        board[i-1][p] = ' '
                    if board[i+1][p] == '🌳':
                        new_number_of_roads = 1
                        old_number_of_roads = 0
                        board[i+1][p] = ' '
        iteration += 1

    return board

def print_map(stdscr):

    trees = ['🌵', '🌳', '🌴']
    stuff = ['⛰', '🗻', '🌊', '🔥' ]
    for i in range(len(board)):
        x = 76
        for p in range(len(board[i])):
            if board[i][p] == '🔰':
                stdscr.addstr(i, x, board[i][p], curses.color_pair(1))
                x += len(board[i][p]) + 1

            elif board[i][p] == "🚶":
                stdscr.addstr(i, x, board[i][p], curses.color_pair(2))
                x += len(board[i][p]) + 1

            elif board[i][p] == "💎":
                stdscr.addstr(i, x, board[i][p], curses.color_pair(2))
                x += len(board[i][p]) + 1

            elif board[i][p] in trees:
                if p % 2 == 0:
                    stdscr.addstr(i, x, board[i][p], curses.color_pair(get_random_greens[0]))
                    x += len(board[i][p]) + 1
                elif p % 3 == 0:
                    stdscr.addstr(i, x, board[i][p], curses.color_pair(get_random_greens[2]))
                    x += len(board[i][p]) + 1
                else:
                    stdscr.addstr(i, x, board[i][p], curses.color_pair(get_random_greens[3]))
                    x += len(board[i][p]) + 1

            elif board[i][p] == '🌲':
                if p % 2 == 0:
                    stdscr.addstr(i, x, board[i][p], curses.color_pair(get_random_greens2[0]))
                    x += len(board[i][p]) + 1
                elif p % 3 == 0:
                    stdscr.addstr(i, x, board[i][p], curses.color_pair(get_random_greens2[2]))
                    x += len(board[i][p]) + 1
                else:
                    stdscr.addstr(i, x, board[i][p], curses.color_pair(get_random_greens2[3]))
                    x += len(board[i][p]) + 1

            elif board[i][p] == "🔥":
                stdscr.addstr(i, x, board[i][p], curses.color_pair(12))
                x += len(board[i][p]) + 1

            elif board[i][p] == "🌊":
                if p % 2 == 0:
                    stdscr.addstr(i, x, board[i][p], curses.color_pair(30))
                    x += len(board[i][p]) + 1
                else:
                    stdscr.addstr(i, x, board[i][p], curses.color_pair(2))
                    x += len(board[i][p]) + 1

            elif board[i][p] == "🗻" and p % 2 == 0:
                    stdscr.addstr(i, x, board[i][p], curses.color_pair(100))
                    x += len(board[i][p]) + 1
            elif board[i][p] == '⛩' or board[i][p] == '🐲':
                stdscr.addstr(i, x, board[i][p], curses.color_pair(101))
                x += len(board[i][p]) + 1

            else:
                stdscr.addstr(i, x, board[i][p])
                x += len(board[i][p]) + 1

            # stdscr.refresh()



    # stdscr.addstr(30, 30, str(curses.can_change_color()))
    # stdscr.addstr(31, 30, str(hero_x_pos))
    # stdscr.addstr(32, 30, str(loot))
def print_message(message):
    message_to_print = message
    stdscr.addstr(41, 35 - int(len(message)/2), message_to_print, curses.color_pair(3))
    stdscr.refresh()
    key = stdscr.getch()

def guess_number(tries):

    def show_boss():
        boss = ['                                |                              ',
                 '                               ||                              ',
                '       -==-____        _--_   ___||___   _--_        ____-==-   ',
                '          ---__----___/ __ \--  || |  --/ __ \___----__---      ',
                '               ---__ / /  \ \   \\ /   / /  \ \ __---           ',
                '                    -\|    \ \  _\/_  / /    |/-                ',
                '                   __/ \_()/\ \//  \\/ /\()_/ \__               ',
                '                  /_ \ / ~~  `-'    '-  ~~ \ / _\              ',
                '                 |/_\ |(~/   /\  /\  /\   \~)| /_\|             ',
                '                  /_  | /   (O ` \/   O)   \ |  _\              ',
                '                  _\ \_\/\___--~~~~--___/\/_/ /_               ',
                '                  /    _/\^\ V~~V/~V~~V /^/\_    \              ',
                '                  \/\ / \ \^\  |( /    /^/ / \ /\/              ',
                '                     \\   /\^\  \\\   /^/\   //                 ',
                '                     \ | /\^\  \/  /^/\ | /                     ',
                '                         |( /\_\^__^/_/\ )|                     ',
                '                         | \\__--__--__// |                     ',
                '                        /~~~~~~~~~~~~~~~~~~\                    ',
                '                       |/|  /\  /\/\  /\  |\|                   ',
                '                       ||| | | ( () ) | | |||                   ',
                '                       |\|  \/  \/\/  \/  |/|                   ',
                '                        \__________________/                    ',
                '                        | (____------____) |                    ',
                                                                                  ]
        os.system('clear')
        for e in boss:
            print(e)

    def choose_number():
        numbers = '0123456789'
        chosen_number = ''
        range_start = 1
        while len(chosen_number) < 3:
            digit = random.randrange(range_start, 10)
            digit = str(digit)
            if digit not in chosen_number:
                chosen_number += digit
                range_start = 0
                numbers = numbers.replace(digit, '')
        return chosen_number

    number = choose_number()
    show_boss()
    print('\n\nWelcome human! You did well so far. It\'s a shame it\'s all for naught!!!')
    print("I have thought up a 3 digit number. Each digit is unique.\nYou have %s guesses to get it or YOU WILL DIE!!!" % tries )
    print(number)
    while True:
        answer = []
        guess = input('Enter your guess: ')
        if guess == number:
            print('YOU GOT LUCKY THIS TIME BASTARD!!!\n')
            break
        elif len(guess) == 3 and guess.isdigit() == True and guess[0] != '0' and guess[0] != guess[1] != guess[2]:
            tries -= 1
            if tries == 0:
                print('YOU DIED!!!\n')
                break
            count = 0
            while count < len(number):
                if guess[count] == number[count]:
                    answer.append('Hot')
                elif guess[count] in number:
                    answer.append('Warm')
                count += 1
            if answer:
                print(' '.join(sorted(answer)))
            else:
                print('Cold')

            print('You have %s tries left.' % tries)
        else:
            print("You are one of those strong but stupid heroes aren't you?!")

# stdscr.refresh()
hero_y_pos = 47
hero_x_pos = 25

board = make_board(50)
board = spawn_objects(1, '🗝')
board = spawn_objects(1, '⛩')
board = spawn_objects(4, '💎')
board = spawn_objects(4, '📛')
board_copy = copy.deepcopy(board)
board[47][25] = "🚶"
board_copy[47][25] = '🏡'
key = ''

while level < 4:
    dims = stdscr.getmaxyx()
    stdscr.refresh()
    # stdscr.addstr(int(dims[0]/2), int(dims[0]/2), str(dims))

    if level == 0:
        stdscr.clear()
        stdscr.refresh()
        menu()
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('1'):
            level = 1
            stdscr.clear()
            continue
        if key == ord('2'):
            level = -1
            continue
        if key == ord('3'):
            level = -2
            continue

    if level == -1:
        stdscr.clear()
        help()

        key = stdscr.getch()
        if key == ord('b'):
            level = 0
            stdscr.refresh()
            continue

    if level == -2:
        stdscr.clear()
        credits()

        key = stdscr.getch()
        if key == ord('b'):
            level = 0
            stdscr.refresh()
            continue
    stdscr.refresh()

    if level >= 1:
        stdscr.refresh()
        stdscr.clear()
        print_map(stdscr)
        print_inventory(inv, items)
        key = stdscr.getch()
    # stdscr.addch(20, 20, key)

        if key == ord('w'):
            if board[hero_y_pos - 1][hero_x_pos] in reachable_symbols:
                hero_y_pos -= 1
                board[hero_y_pos][hero_x_pos] = "🚶"
                board[hero_y_pos + 1][hero_x_pos] = board_copy[hero_y_pos + 1][hero_x_pos]

        elif key == ord('s'):
            if board[hero_y_pos + 1][hero_x_pos] in reachable_symbols:
                hero_y_pos += 1
                board[hero_y_pos][hero_x_pos] = "🚶"
                board[hero_y_pos - 1][hero_x_pos] = board_copy[hero_y_pos - 1][hero_x_pos]

        elif key == ord('a'):
            if board[hero_y_pos][hero_x_pos - 1] in reachable_symbols:
                hero_x_pos -= 1
                board[hero_y_pos][hero_x_pos] = "🚶"
                board[hero_y_pos][hero_x_pos + 1] = board_copy[hero_y_pos][hero_x_pos + 1]

        elif key == ord('d'):
            if board[hero_y_pos][hero_x_pos + 1] in reachable_symbols:
                hero_x_pos += 1
                board[hero_y_pos][hero_x_pos] = "🚶"
                board[hero_y_pos][hero_x_pos - 1] = board_copy[hero_y_pos][hero_x_pos - 1]

        if board[hero_y_pos][hero_x_pos] == "🚶" and board_copy[hero_y_pos][hero_x_pos] == "💎":
            board_copy[hero_y_pos][hero_x_pos] = " "

            if 'diamond of wisdom' not in inv:
                inv['diamond of wisdom'] = 1
            else:
                inv['diamond of wisdom'] += 1
            stdscr.clear()

        if board[hero_y_pos][hero_x_pos] == "🚶" and board_copy[hero_y_pos][hero_x_pos] == "📛":
            board_copy[hero_y_pos][hero_x_pos] = " "

            if 'iron ore' not in inv:
                inv['iron ore'] = 1
            else:
                inv['iron ore'] += 1
            stdscr.clear()

        if board[hero_y_pos][hero_x_pos] == "🚶" and board_copy[hero_y_pos][hero_x_pos] == "🗝":
            board_copy[hero_y_pos][hero_x_pos] = " "
            if 'key' not in inv:
                inv['key'] = 1
            else:
                inv['key'] += 1
            stdscr.clear()

        if board[hero_y_pos][hero_x_pos] == "🚶" and board_copy[hero_y_pos][hero_x_pos] == "⛩":
            if inv['key'] == 1:
                print_message("CONGRATS! YOU ARE GOING TO THE NEXT LEVEL")
                level += 1
                level_change = 0
            else:
                print_message("I can't cross, I have to find key first!")

        if board[hero_y_pos][hero_x_pos] == "🚶" and board_copy[hero_y_pos][hero_x_pos] == '🐲':
            if inv['key'] == 1:
                print_message("DRAGON:LETS FIGHT!")
                level += 1
                level_change = 0
            else:
                print_message("DRAGON:YOU CAN'T CHALLANGE ME WITHOUT THE KEY")

    if level >= 2 and level_change == 0:
        stdscr.clear()
        level_change += 1

        board = make_board(50)
        board = spawn_objects(1, '🗝')

        if level == 3:
            board = spawn_objects(1, '🐲')
        else:
            board = spawn_objects(1, '⛩')

        board = spawn_objects(4, '💎')
        board_copy = copy.deepcopy(board)
        board[47][25] = "🚶"
        board_copy[47][25] = '🕍'
        hero_y_pos = 47
        hero_x_pos = 25
        inv['key'] = 0

stdscr.keypad(0)
curses.curs_set(True)
curses.endwin()

print("hehe")
guess_number(5 + inv['diamond of wisdom'])
# if key = space print else time 3 print
# if board[hero_y_pos+1][hero_x_pos] != '#'
# while board[rnumber[0]]rnumber[1] not " "
