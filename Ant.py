import threading
from numpy import random
from conf import width_image, height_image


# That class define an Ant
class Ant:
    def __init__(self, x, y, color):

        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.color = color  # color of the ant
        self.lock = threading.Lock()  # a lock to manage thread concurrency

    # function that move an ants in a random direction
    def deplacer(self):
        # calculate a random direction for the next move
        direction = random.randint(0, 8, 1, 'int')

        if direction == 0:
            self.x += 0
            self.y += -1
        elif direction == 1:
            self.x += 0
            self.y += 1
        elif direction == 2:
            self.x += -1
            self.y += 0
        elif direction == 3:
            self.x += 1
            self.y += 0
        elif direction == 4:
            self.x += -1
            self.y += 1
        elif direction == 5:
            self.x += 1
            self.y += 1
        elif direction == 6:
            self.x += -1
            self.y += -1
        elif direction == 7:
            self.x += 1
            self.y += -1

        # calculate the new position of the ant
        self.x = self.x % width_image
        self.y = self.y % height_image
