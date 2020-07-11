""" Collection of tetrominos, and tetromino handler class """
import random

SmashBoy = [[1, 1],
            [1, 1]]

Hero = [[1, 1, 1, 1]]

TeeWee = [[0, 1, 0],
          [1, 1, 1]]

RhodeIslandZ = [[0, 1, 1],
                [1, 1, 0]]

ClevelandZ = [[1, 1, 0],
              [0, 1, 1]]

BlueRicky = [[1, 0, 0],
             [1, 1, 1]]

OrangeRicky = [[0, 0, 1],
               [1, 1, 1]]

ShapeVector = [SmashBoy, Hero, TeeWee, RhodeIslandZ, ClevelandZ, BlueRicky, OrangeRicky]


def get_random_tetromino():
    """ Generate random tetromino from ShapeVector """
    return random.choice(ShapeVector)


class Shape:
    """ Tetromino handler class """
    def __init__(self, max_column):
        self.bottomLeftX = int(max_column / 2)
        self.bottomLeftY = 0
        self.maxColumn = max_column
        self.current_tetromino = get_random_tetromino()

    def get_x(self):
        """ Get the top X position of the shape """
        return self.bottomLeftX

    def get_y(self):
        """ Get the top Y position of the shape """
        return self.bottomLeftY

    def move_down(self):
        """ Move the shape down """
        self.bottomLeftY += 1

    def move_right(self):
        """ Move the shape right """
        if self.bottomLeftX + len(self.current_tetromino[0]) < self.maxColumn:
            self.bottomLeftX += 1

    def move_left(self):
        """ Move the shape left """
        if self.bottomLeftX != 0:
            self.bottomLeftX -= 1

    def get_tetromino(self):
        """ Return current tetromino """
        return self.current_tetromino

    def rotate(self):
        """ Rotate the current tetromino """
        self.current_tetromino = list(list(x)[::-1] for x in zip(*self.current_tetromino))

    def get_rotated_shape(self):
        """ Return the current tetromino rotated """
        return list(list(x)[::-1] for x in zip(*self.current_tetromino))
