#!/usr/bin/env python3

import curses
from random import random


MINE_RATIO = 0.0926
MINE_SYMBOL = '☒'

def main(stdscr):
    # ==================
    # = Helper methods =
    # ==================
    paint_cell = lambda y, x, char, attr: stdscr.addstr(2 * (y + 1), 2 * (x + 1), char, attr)

    def count_bombs(current_y, current_x):
        return str(sum(
            sum(row[max(0, current_x-1):min(width,current_x+2)]) for row in bombs[
                max(0, current_y-1):min(height,current_y+2)]
        ) or ' ')

    def click(current_y, current_x, user_click=True):
        if bombs[current_y][current_x]:
            if user_click:
                raise Exception('You clicked on a bomb 😥️. BOOM 💣️. YOU LOSE!! 💀️')

        if board[current_y][current_x] != '.':
            return

        neighbors = [(current_y, current_x)]

        while neighbors:
            current_y, current_x = neighbors.pop()

            board[current_y][current_x] = count_bombs(current_y, current_x)

            if board[current_y][current_x] == ' ':
                for offset_y in (-1, 0, 1):
                    new_y = current_y + offset_y

                    if new_y < 0 or new_y > height - 1:
                        continue

                    for offset_x in (-1, 0, 1):
                        new_x = current_x + offset_x

                        if new_x < 0 or new_x > width - 1 or offset_x == 0 and offset_y == 0:
                            continue

                        if board[new_y][new_x] != '.' or bombs[new_y][new_x]:
                            continue

                        neighbors.append((new_y, new_x))

    # ===============
    # = Screen init =
    # ===============

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    # Clear screen
    stdscr.clear()

    # ===================
    # = Game state init =
    # ===================

    height, width = (curses.LINES - 2) // 2 - 1, (curses.COLS - 2) // 2 - 1
    current_y, current_x = 0, 0
    key = None

    bombs = [[random() < MINE_RATIO for x in range(0, width)] for y in range(0, height)]
    board = [['.' for x in range(0, width)] for y in range(0, height)]

    # ================
    # = Game routine =
    # ================
    finished = False
    while key != 'q' and not finished:
        finished = True

        stdscr.addstr(0, 0, '┌' + '─' * (2 * width + 1) + '┐')
        stdscr.addstr(2 * height + 1, 0, '└' + '─' * (2 * width + 1) + '┘')

        for y in range(0, height):
            stdscr.addstr(2 * (y + 1) - 1, 0, '│')
            stdscr.addstr(2 * (y + 1), 0, '│')
            stdscr.addstr(2 * (y + 1) - 1, 2 * width + 2, '│')
            stdscr.addstr(2 * (y + 1), 2 * width + 2, '│')

            for x in range(0, width):
                paint_cell(y, x, board[y][x], curses.color_pair(1) if (y, x) == (current_y, current_x) else False)

                if board[y][x] == '.' or bombs[y][x] != (board[y][x] == MINE_SYMBOL):
                    finished = False

        stdscr.refresh()
        key = stdscr.getkey()

        if key == 'KEY_LEFT':
            current_x = max(0, current_x - 1)
        elif key == 'KEY_RIGHT':
            current_x = min(width - 1, current_x + 1)
        elif key == 'KEY_UP':
            current_y = max(0, current_y - 1)
        elif key == 'KEY_DOWN':
            current_y = min(height - 1, current_y + 1)
        elif key == ' ':
            click(current_y, current_x)
        elif key == 'x':
            if board[current_y][current_x] == '.':
                board[current_y][current_x] = MINE_SYMBOL
            elif board[current_y][current_x] == MINE_SYMBOL:
                board[current_y][current_x] = '.'

    if finished:
        raise Exception('YOU WIN!! 🎉️🎉️')
    else:
        raise Exception('kthxbye')

try:
    curses.wrapper(main)
except Exception as e:
    print(e.args[0])
