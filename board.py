import random



# GREY = '\033[90m'
# BLUE = '\033[94m'
# GREEN = '\033[92m'
# YELLOW = '\033[93m'
# RED = '\033[91m'
# WHITE = '\033[0m'
#
# # board = [['⛰'] * 50 for x in range(51)]
# #
# # for i in range(2, 49):
# #     for y in range(2, 48):
# #         board[i][y] = " "
# #
# # board2 = [['⛰'] * 50 for x in range(51)]
# #
# # for i in range(2, 49):
# #     for y in range(2, 48):
# #         board2[i][y] = " "
#
# emojis = ('⚑', '⛰', '🌲', '🌳', '🌴', '🌵', '🏠', '🔥', '🗻', '⭐', '⚒',)


def make_board(size):
    number_of_obstacles = 30
    board = []
    border_size = 2
    path_size = 3                   #no obstacles touching the border
    border = ('⛰', '🗻', '🌊')
    obstacles = ('🌵', '🔥', '🌴', '🌲')
    border_select = random.choice(border)
    for i in range(0, size):
        i = [border_select] * size
        board.append(i)
    for i in range (0+border_size, size-border_size):
        for j in range (0+border_size, size-border_size):
            board[i][j] = ' '

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

    count = 0                                       #render paths on board
    paths = []
    path = random.randrange(size//4, size//2)
    while count < 2:
        paths.append(path)
        path += size//3
        count += 1

    for e in paths:
        for i in range(e, e + path_size):
            for j in range(0 + border_size,50-border_size):
                board[i][j] = ' '

    for e in paths:
        for i in range(0 + border_size,50-border_size):
            for j in range(e, e + path_size):
                board[i][j] = ' '

    return board



def display_board(board):
    for i in board:
        print(' '.join(i))


board = make_board(50)

display_board(board)
