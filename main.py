""" Main function, and game logic """

import pygame
import queue
import numpy
import datetime
from ShapeGetter import ShapeGetter
import Renderer

ROWS = Renderer.ROWS
COLUMNS = Renderer.COLUMNS

playing_field = [[0 for i in range(ROWS)] for j in range(COLUMNS)]
currentScore = 0
current_shape = ShapeGetter.Shape(ROWS)
next_shape = ShapeGetter.Shape(ROWS)
game_finished = False


def shape_stuck(tetromino, x, y):
    """ Check if the given tetromino at the given position collides with anything on the playing field """
    current_column = 0
    for column in tetromino:
        current_row = 0
        for row in column:
            exact_row = x + current_row
            exact_column = y + current_column
            current_row += 1
            if row == 0 or exact_row < 0 or exact_column < 0:
                continue
            if exact_row >= ROWS or exact_column >= COLUMNS:
                return True
            if playing_field[exact_column][exact_row] != 0:
                return True
        current_column += 1
    return False


def merge_shape(shape):
    """ Merge given shape into the playing field """
    global playing_field
    tetromino = shape.get_tetromino()
    x = shape.get_x()
    y = shape.get_y()
    current_column = 0
    for column in tetromino:
        current_row = 0
        for row in column:
            exact_row = x + current_row
            exact_column = y + current_column
            current_row += 1
            if row == 0 or exact_row < 0 or exact_column < 0 or exact_row >= ROWS or exact_column >= COLUMNS:
                continue
            playing_field[exact_column][exact_row] = row
        current_column += 1


def delete_full_rows():
    """ Remove filled rows from the playing field, and move the others accordingly """
    global currentScore
    global playing_field
    deleted_rows = 0
    current_column = -1
    rows_to_delete = queue.LifoQueue()
    for column in playing_field:
        current_row = -1
        current_column += 1
        full = True
        for row in column:
            current_row += 1
            if row != 1:
                full = False
                break
        if full:
            rows_to_delete.put(current_column)
    while True:
        try:
            element = rows_to_delete.get_nowait()
            playing_field = numpy.delete(playing_field, element - deleted_rows, axis=0)
            deleted_rows += 1
        except:
            break
    currentScore += deleted_rows
    if deleted_rows > 0:
        print("Current score: ", currentScore)
        extra_lines = [[0 for i in range(ROWS)] for j in range(deleted_rows)]
        playing_field = numpy.vstack((extra_lines, playing_field))


def handle_game_events():
    """ Handle game events """
    global game_finished
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_finished = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if not shape_stuck(current_shape.get_tetromino(), current_shape.get_x() + 1, current_shape.get_y()):
                current_shape.move_right()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if not shape_stuck(current_shape.get_tetromino(), current_shape.get_x() - 1, current_shape.get_y()):
                current_shape.move_left()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if not tetromino_landed(current_shape):
                current_shape.move_down()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if not shape_stuck(current_shape.get_rotated_shape(), current_shape.get_x(), current_shape.get_y()):
                current_shape.rotate()


def tetromino_landed(tetromino):
    """ Check if given tetromino landed """
    return shape_stuck(tetromino.get_tetromino(), tetromino.get_x(), tetromino.get_y() + 1)


def handle_tetromino_landing():
    """ Merge landed tetromino into the playing field, switch current with next, generate new next """
    global current_shape
    global next_shape
    merge_shape(current_shape)
    current_shape = next_shape
    next_shape = ShapeGetter.Shape(ROWS)


def tick():
    """ Move down tetromino, and handle if it landed"""
    global game_finished
    if tetromino_landed(current_shape):
        handle_tetromino_landing()
    else:
        current_shape.move_down()
    if shape_stuck(current_shape.get_tetromino(), current_shape.get_x(), current_shape.get_y()):
        game_finished = True


def render(screen):
    """ Render the window """
    Renderer.render_background(screen)
    Renderer.render_elements_on_field(screen, playing_field, current_shape)
    Renderer.render_next_shape(screen, next_shape)


def main():
    """ Main game loop """
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    render(screen)
    last_move_time = datetime.datetime.now()
    while not game_finished:
        now = datetime.datetime.now()
        delta = now - last_move_time
        if int(delta.total_seconds()) > 1:
            last_move_time = now
            tick()
        render(screen)
        handle_game_events()
        delete_full_rows()
        pygame.display.flip()


if __name__ == "__main__":
    main()
