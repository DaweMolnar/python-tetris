""" Renderer functions and variables connected to rendering """
import pygame

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
    for column in shape.get_tetromino():
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

