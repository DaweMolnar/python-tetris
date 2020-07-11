import pygame
import queue
import numpy
import datetime
from ShapeGetter import ShapeGetter

TOP_LEFT_POSITION = 30
TOP_RIGHT_POSITION = 30
PLAY_FIELD_WIDTH = 400
PLAY_FIELD_HEIGHT = 640
NEXT_SHAPE_FIELD_WIDTH = 100
NEXT_SHAPE_FIELD_HEIGHT = 60
TETROMINO_BLOCK_SIZE = 40
BACKGROUND_COLOR = (255, 255, 255)
STATIONARY_TETROMINO_COLOR = (255, 0, 0)
MOVING_TETROMINO_COLOR = (0, 255, 0)
ROWS = 10
COLUMNS = 16

PlayField = [[0 for i in range(ROWS)] for j in range(COLUMNS)]
currentScore = 0
Done = False


def render_background(screen):
    """ Render the background of the game's fields """
    color = BACKGROUND_COLOR
    field_rect = pygame.Rect(TOP_LEFT_POSITION, TOP_RIGHT_POSITION, PLAY_FIELD_WIDTH, PLAY_FIELD_HEIGHT)
    pygame.draw.rect(screen, color, field_rect)
    pygame.draw.rect(screen, color,
                     pygame.Rect(TOP_LEFT_POSITION + PLAY_FIELD_WIDTH + 10
                                 , TOP_RIGHT_POSITION
                                 , NEXT_SHAPE_FIELD_WIDTH
                                 , NEXT_SHAPE_FIELD_HEIGHT))


def render_next_shape(screen, shape):
    """ Render the next tetromino to the next shape field """
    current_column = 0
    for column in shape.getShape():
        current_row = 0
        for row in column:
            if row == 1:
                pygame.draw.rect(screen, STATIONARY_TETROMINO_COLOR,
                                 pygame.Rect(TOP_LEFT_POSITION + PLAY_FIELD_WIDTH + 20 + current_row * int(TETROMINO_BLOCK_SIZE / 2)
                                             , TOP_RIGHT_POSITION + 10 + current_column * int(TETROMINO_BLOCK_SIZE / 2)
                                             , int(TETROMINO_BLOCK_SIZE / 2)
                                             , int(TETROMINO_BLOCK_SIZE / 2)))
            current_row += 1
        current_column += 1


def render_current_shape(screen, shape):
    """ Render the current movable tetromino """
    current_shape = shape.getShape()
    x = shape.getX()
    y = shape.getY()
    current_column = 0
    for column in current_shape:
        current_row = 0
        for row in column:
            exact_row = x + current_row
            exact_column = y + current_column
            current_row += 1
            if row == 0 or exact_row < 0 or exact_column < 0 or exact_row >= ROWS or exact_column >= COLUMNS:
                continue
            pygame.draw.rect(screen, MOVING_TETROMINO_COLOR,
                             pygame.Rect(TOP_LEFT_POSITION + exact_row * TETROMINO_BLOCK_SIZE
                                         , TOP_RIGHT_POSITION + exact_column * TETROMINO_BLOCK_SIZE
                                         , TETROMINO_BLOCK_SIZE
                                         , TETROMINO_BLOCK_SIZE))
        current_column += 1


def render_elements_on_field(screen, table, shape):
    """ Render the tetrominos of the playing field """
    current_column = 0
    for column in table:
        current_row = 0
        for row in column:
            if row == 1:
                pygame.draw.rect(screen, STATIONARY_TETROMINO_COLOR,
                                 pygame.Rect(TOP_LEFT_POSITION + current_row * TETROMINO_BLOCK_SIZE
                                             , TOP_RIGHT_POSITION + current_column * TETROMINO_BLOCK_SIZE
                                             , TETROMINO_BLOCK_SIZE
                                             , TETROMINO_BLOCK_SIZE))
            current_row += 1
        current_column += 1
    render_current_shape(screen, shape)


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
            if PlayField[exact_column][exact_row] != 0:
                return True
        current_column += 1
    return False


def merge_shape(shape):
    """ Merge given shape into the playing field """
    global PlayField
    current_shape = shape.getShape()
    x = shape.getX()
    y = shape.getY()
    current_column = 0
    for column in current_shape:
        current_row = 0
        for row in column:
            exact_row = x + current_row
            exact_column = y + current_column
            current_row += 1
            if row == 0 or exact_row < 0 or exact_column < 0 or exact_row >= ROWS or exact_column >= COLUMNS:
                continue
            PlayField[exact_column][exact_row] = row
        current_column += 1


def delete_full_rows():
    """ Remove filled rows from the playing field, and move the others accordingly """
    global currentScore
    global PlayField
    deleted_rows = 0
    current_column = -1
    rows_to_delete = queue.LifoQueue()
    for column in PlayField:
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
            PlayField = numpy.delete(PlayField, element - deleted_rows, axis=0)
            deleted_rows += 1
        except:
            break
    currentScore += deleted_rows
    if deleted_rows > 0:
        print("Current score: ", currentScore)
        extra_lines = [[0 for i in range(ROWS)] for j in range(deleted_rows)]
        PlayField = numpy.vstack((extra_lines, PlayField))


def handle_game_events(current_shape):
    """ Handle game events """
    global Done
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if not shape_stuck(current_shape.getShape(), current_shape.getX() + 1, current_shape.getY()):
                current_shape.moveRight()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if not shape_stuck(current_shape.getShape(), current_shape.getX() - 1, current_shape.getY()):
                current_shape.moveLeft()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            current_shape.moveDown()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if not shape_stuck(current_shape.getRotatedShape(), current_shape.getX(), current_shape.getY()):
                current_shape.rotate()


def main():
    """ Main game loop """
    global Done
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    render_background(screen)
    current_shape = ShapeGetter.Shape(ROWS)
    next_shape = ShapeGetter.Shape(ROWS)
    last_move_time = datetime.datetime.now()
    while not Done:
        now = datetime.datetime.now()
        delta = now - last_move_time
        if int(delta.total_seconds()) > 1:
            last_move_time = now
            current_shape.moveDown()
        if shape_stuck(current_shape.getShape(), current_shape.getX(), current_shape.getY()):
            Done = True
        render_background(screen)
        render_elements_on_field(screen, PlayField, current_shape)
        render_next_shape(screen, next_shape)
        handle_game_events(current_shape)
        if shape_stuck(current_shape.getShape(), current_shape.getX(), current_shape.getY() + 1):
            merge_shape(current_shape)
            current_shape = next_shape
            next_shape = ShapeGetter.Shape(ROWS)
        delete_full_rows()
        pygame.display.flip()


if __name__ == "__main__":
    main()
