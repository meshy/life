import random
import time
from functools import partial
from itertools import product

from blessings import Terminal


term = Terminal()

WINDOW_WIDTH = term.width // 2
WINDOW_HEIGHT = term.height

ALIVE = 'X'
DEAD = ' '

def print_board(board):
    for i, row in enumerate(board):
        print(term.move(i, 0) + ' '.join(row), end="", flush=True)


def get_num_neighbours(board, y, x):
    above, below = y - 1, y + 1
    left, right = x - 1, x + 1

    above %= WINDOW_HEIGHT
    below %= WINDOW_HEIGHT

    left %= WINDOW_WIDTH
    right %= WINDOW_WIDTH

    combinations = list(product([above, y, below], [left, x, right]))
    combinations.remove((y, x))
    return sum(board[y][x] != DEAD for y, x in combinations)


def next_state(board, y, x):
    neighbours = get_num_neighbours(board, y, x)
    if neighbours == 3 or (board[y][x] == ALIVE and neighbours == 2):
        return ALIVE
    return DEAD


def bump_board(board):
    new_board = []
    for i in range(WINDOW_HEIGHT):
        new_states = map(partial(next_state, board, i), range(WINDOW_WIDTH))
        new_board.append(''.join(new_states))
    return new_board


def random_row():
    return ''.join([random.choice([DEAD, ALIVE]) for _ in range(WINDOW_WIDTH)])


if __name__ == '__main__':
    board = [random_row() for _ in range(WINDOW_HEIGHT)]

    print(term.clear)
    with term.fullscreen():
        while True:
            print_board(board)
            time.sleep(.07)
            board = bump_board(list(map(str, board)))
