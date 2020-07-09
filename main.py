import pygame
import queue
import numpy
import datetime
from ShapeGetter import ShapeGetter

topLeft = 30
topRight = 30
tetrominoElementSize = 40
Done = False
Rows = 10
Columns = 16
PlayField = [[0 for i in range(Rows)] for j in range(Columns)]


def draw_field(screen):
    color = (255, 255, 255)
    field_rect = pygame.Rect(topLeft, topRight, 400, 640)
    pygame.draw.rect(screen, color, field_rect)
    pygame.draw.rect(screen, color, pygame.Rect(topLeft + 410, topRight, 100, 60))


def render_next_shape(screen, shape):
    color = (255, 0, 0)
    current_column = -1
    for column in shape.getShape():
        current_row = -1
        current_column += 1
        for row in column:
            current_row += 1
            if row == 1:
                pygame.draw.rect(screen, color,
                                 pygame.Rect(topLeft + 420 + current_row * int(tetrominoElementSize / 2)
                                             , topRight + 10 + current_column * int(tetrominoElementSize / 2)
                                             , int(tetrominoElementSize / 2)
                                             , int(tetrominoElementSize / 2)))


def render_current_shape(screen, shape):
    color = (0, 255, 0)
    tetromino = shape.getShape()
    x = shape.getX()
    y = shape.getY()
    current_column = -1
    for column in tetromino:
        current_row = -1
        current_column += 1
        for row in column:
            current_row += 1
            exact_row = x + current_row
            exact_column = y + current_column
            if row == 0 or exact_row < 0 or exact_column < 0 or exact_row >= Rows or exact_column >= Columns:
                continue
            pygame.draw.rect(screen, color,
                             pygame.Rect(topLeft + exact_row * tetrominoElementSize
                                         , topRight + exact_column * tetrominoElementSize
                                         , tetrominoElementSize
                                         , tetrominoElementSize))


def render_elements_on_field(screen, table, shape):
    color = (255, 0, 0)
    current_column = -1
    for column in table:
        current_row = -1
        current_column += 1
        for row in column:
            current_row += 1
            if row == 1:
                pygame.draw.rect(screen, color,
                                 pygame.Rect(topLeft + current_row * tetrominoElementSize
                                             , topRight + current_column * tetrominoElementSize
                                             , tetrominoElementSize
                                             , tetrominoElementSize))
    render_current_shape(screen, shape)


def shape_stuck(tetromino, x, y):
    current_column = -1
    for column in tetromino:
        current_row = -1
        current_column += 1
        for row in column:
            current_row += 1
            exact_row = x + current_row
            exact_column = y + current_column
            if row == 0 or exact_row < 0 or exact_column < 0:
                continue
            if exact_row >= Rows or exact_column >= Columns:
                return True
            if PlayField[exact_column][exact_row] != 0:
                return True
    return False


def merge_shape(shape):
    tetromino = shape.getShape()
    x = shape.getX()
    y = shape.getY()
    current_column = -1
    for column in tetromino:
        current_row = -1
        current_column += 1
        for row in column:
            current_row += 1
            exact_row = x + current_row
            exact_column = y + current_column
            if row == 0 or exact_row < 0 or exact_column < 0 or exact_row >= Rows or exact_column >= Columns:
                continue
            PlayField[exact_column][exact_row] = row


def delete_full_rows():
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
    if deleted_rows > 0:
        extra_lines = [[0 for i in range(Rows)] for j in range(deleted_rows)]
        PlayField = numpy.vstack((extra_lines, PlayField))
        print("added to playfiled?" + str(len(PlayField)))


def main():
    global Done
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    draw_field(screen)
    currentShape = ShapeGetter.Shape(Rows)
    nextShape = ShapeGetter.Shape(Rows)
    lastMoveTime = datetime.datetime.now()
    while not Done:
        now = datetime.datetime.now()
        delta = now - lastMoveTime
        if int(delta.total_seconds()) > 1:
            lastMoveTime = now
            currentShape.moveDown()
        if shape_stuck(currentShape.getShape(), currentShape.getX(), currentShape.getY()):
            Done = True
        draw_field(screen)
        render_elements_on_field(screen, PlayField, currentShape)
        render_next_shape(screen, nextShape)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if not shape_stuck(currentShape.getShape(), currentShape.getX() + 1, currentShape.getY()):
                    currentShape.moveRight()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if not shape_stuck(currentShape.getShape(), currentShape.getX() - 1, currentShape.getY()):
                    currentShape.moveLeft()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                currentShape.moveDown()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if not shape_stuck(currentShape.getRotatedShape(), currentShape.getX() - 1, currentShape.getY()):
                    currentShape.rotate()
        if shape_stuck(currentShape.getShape(), currentShape.getX(), currentShape.getY() + 1):
            merge_shape(currentShape)
            currentShape = nextShape
            nextShape = ShapeGetter.Shape(Rows)
        delete_full_rows()
        pygame.display.flip()


if __name__ == "__main__":
    main()
