import pygame
import random


class Figure:

    def __init__(self, game, size, start_x, start_y):
        self.falling = True
        self.game = game
        self.block_size = size
        self._blocks = tuple([start_x, start_y] for _ in range(4))
        self.color = None

    def draw(self):
        for b in self._blocks:
            pygame.draw.rect(self.game.surface, self.color,
                             (self.game.grid_x[b[0]], self.game.grid_y[b[1]], self.block_size, self.block_size))

    def fall(self):
        for block in self._blocks:
            block[1] += 1

    def move(self, direction: int):
        if self.falling:
            if abs(direction) != 1:
                raise ValueError("La direction doit être égale à -1 ou 1")
            for block in self._blocks:
                block[0] += direction

    def get_blocks(self):
        if self.falling:
            raise PermissionError("Impossible d'accéder à _blocks tant que la figure est en chute")
        return self._blocks


class Square(Figure):

    def __init__(self, surface, start_x=-1, start_y=-1, size=10):
        super().__init__(surface, start_x, start_y, size)
        self._blocks[1][0] += 1
        self._blocks[2][1] += 1
        self._blocks[3][0] += 1
        self._blocks[3][1] += 1
        self.color = (255, 255, 0)

    def fall(self):
        if self._blocks[2][1] == self.game.limit[self._blocks[2][0]] \
                or self._blocks[3][1] == self.game.limit[self._blocks[3][0]]:
            self.falling = False
        else:
            super().fall()

    def move(self, direction: int):
        collision = False
        for block in self._blocks:
            if block[0] + direction in self.game.wall[block[1]]:
                collision = True
        if not collision and ((direction == -1 and self._blocks[0][0] > 0)
                              or (direction == 1 and self._blocks[1][0] < self.game.nb_blocks[0] - 1)):
            super().move(direction)

    def turn(self):
        pass

    def get_top(self):
        return self._blocks[0], self._blocks[1]


class Line(Figure):

    def __init__(self, surface, start_x=-1, start_y=-1, size=10):
        super().__init__(surface, start_x, start_y, size)
        self._blocks[1][1] += 1
        self._blocks[2][1] += 2
        self._blocks[3][1] += 3
        self.color = (0, 255, 255)
        self.vertical = True

    def fall(self):
        if self._blocks[3][1] == self.game.limit[self._blocks[2][0]]:
            self.falling = False
        else:
            super().fall()

    def move(self, direction: int):
        collision = False
        for block in self._blocks:
            if block[0] + direction in self.game.wall[block[1]]:
                collision = True
        if not collision and ((direction == -1 and self._blocks[0][0] > 0)
                              or (direction == 1 and self._blocks[3][0] < self.game.nb_blocks[0] - 1)):
            super().move(direction)

    def turn(self):
        x = self._blocks[0][0]
        y = self._blocks[0][1]
        num = 0
        for block in self._blocks:
            if self.vertical:
                block[0] = x + num
                block[1] = y
            else:
                block[0] = x
                block[1] = y + num
            num += 1
        self.vertical = not self.vertical

    def get_top(self):
        if self.vertical:
            return [self._blocks[0]]
        else:
            return self._blocks

# TODO : faire les autres figures

