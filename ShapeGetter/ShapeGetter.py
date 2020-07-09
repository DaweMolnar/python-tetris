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


def getRandomTetromino():
    return random.choice(ShapeVector)


class Shape:
    def __init__(self, maxColumn):
        self.bottomLeftX = int(maxColumn / 2)
        self.bottomLeftY = 0
        self.maxColumn = maxColumn
        self.currentShape = getRandomTetromino()

    def getX(self):
        return self.bottomLeftX

    def getY(self):
        return self.bottomLeftY

    def moveDown(self):
        self.bottomLeftY += 1

    def moveRight(self):
        if self.bottomLeftX + len(self.currentShape[0]) < self.maxColumn:
            self.bottomLeftX += 1

    def moveLeft(self):
        if self.bottomLeftX != 0:
            self.bottomLeftX -= 1

    def getShape(self):
        return self.currentShape

    def rotate(self):
        self.currentShape = list(list(x)[::-1] for x in zip(*self.currentShape))

    def getRotatedShape(self):
        return list(list(x)[::-1] for x in zip(*self.currentShape))
