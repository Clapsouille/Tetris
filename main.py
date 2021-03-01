from pygame.locals import *
import figures
import pygame
import random
import sys

types = [figures.Square, figures.Line]


class Game:

    def __init__(self, window=(500, 500), speed=5, block=20, fps=20):
        pygame.init()
        pygame.display.set_caption("Tetrissss")

        self.WINDOW_SIZE = window
        self.SPEED = speed
        self.BLOCK = block
        self.FPS = fps

        # Calcul des dimensions de la grille / de l'adresse de chaque case et mise en place
        self.nb_blocks = ((self.WINDOW_SIZE[0] - 1) // (self.BLOCK + 1), (self.WINDOW_SIZE[1] - 1) // (self.BLOCK + 1))
        self.padd = ((self.WINDOW_SIZE[0] - 1) % (self.BLOCK + 1), (self.WINDOW_SIZE[1] - 1) % (self.BLOCK + 1))
        self.grid_x = {i: (self.padd[0] // 2) + 2 + i * (self.BLOCK + 1) for i in range(self.nb_blocks[0])}
        self.grid_y = {i: (self.padd[1] // 2) + 2 + i * (self.BLOCK + 1) for i in range(self.nb_blocks[1])}

        self.clock = pygame.time.Clock()
        self.clock.tick(self.FPS)
        self.surface = pygame.display.set_mode(self.WINDOW_SIZE)

        # Instanciation figure(s) et variables de suivi du mur de blocs
        self.fig = random.choice(types)(self, self.BLOCK, 5, 0)
        self.fig.draw()
        self.limit = {i: self.nb_blocks[1] - 1 for i in range(self.nb_blocks[0])}
        self.wall = {y: {} for y in range(self.nb_blocks[1])}
        self.lines = {i: self.nb_blocks[0] for i in range(self.nb_blocks[1])}

        self.playing = True


    def draw_grid(self):
        """Mise en place de la grille"""
        self.surface.fill((0, 0, 0))
        curs = (self.padd[0] // 2) + 1
        for _ in range(self.nb_blocks[0] + 1):
            pygame.draw.line(self.surface, (20, 20, 20), (curs, self.padd[1] // 2),
                             (curs, self.WINDOW_SIZE[1] - (self.padd[1] // 2 + self.padd[1] % 2)))
            curs += self.BLOCK + 1
        curs = (self.padd[1] // 2) + 1
        for _ in range(self.nb_blocks[1] + 1):
            pygame.draw.line(self.surface, (20, 20, 20), (self.padd[0] // 2, curs),
                             (self.WINDOW_SIZE[0] - (self.padd[0] // 2 + self.padd[0] % 2), curs))
            curs += self.BLOCK + 1

    def block_to_wall(self):
        """Ajout d'un bloc ayant achevé sa chute au mur de blocs"""
        for block in self.fig.get_top():
            self.limit[block[0]] = block[1] - 1
            if block[1] <= 2:
                self.playing = False  # TODO : perdu
        full_lines = []
        for block in self.fig.get_blocks():
            self.wall[block[1]][block[0]] = self.fig.color
            self.lines[block[1]] -= 1
            if self.lines[block[1]] == 0:
                full_lines.append(block[1])
        if len(full_lines) > 0:
            full_lines.sort(reverse=True)
            for i in range(len(full_lines)):
                self.del_line(full_lines[i] + i)
            # TODO : bonus si plusieurs lignes complétées en même temps
        del self.fig

        # Instanciation aléatoire d'une figure
        self.fig = random.choice(types)(self, self.BLOCK, 5, 0)

    def del_line(self, y):
        """Suppression d'une ligne complète"""
        for x, val in self.limit.items():
            self.limit[x] += 1
        toDel = []
        iterate = True
        while iterate:
            self.lines[y] = self.lines[y - 1]
            for bl, col in self.wall[y].items():
                if bl in self.wall[y - 1].keys():
                    self.wall[y][bl] = self.wall[y - 1][bl]
                else:
                    toDel.append((y, bl))
            y -= 1
            if self.lines[y] == self.nb_blocks[0]:
                iterate = False
        for blY, blX in toDel:
            del self.wall[blY][blX]

    def game_loop(self):
        count = 0
        while self.playing:
            pygame.display.update()
            self.draw_grid()

            # Lorsque la figure atteint le sol, ses blocs sont intégrés au mur et la limite recalculée
            if not self.fig.falling:
                self.block_to_wall()

            # Affichage du bloc courant et du mur de blocs
            self.fig.draw()
            for y, bl in self.wall.items():
                for x, col in bl.items():
                    pygame.draw.rect(self.surface, col, (self.grid_x[x], self.grid_y[y], self.BLOCK, self.BLOCK))

            # Commandes utilisateur
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.fig.move(-1)
                    elif event.key == K_RIGHT:
                        self.fig.move(1)
                    elif event.key == K_DOWN:
                        self.fig.fall()
                    elif event.key == K_UP:
                        while self.fig.falling:
                            self.fig.fall()
                    elif event.key == K_SPACE:
                        self.fig.turn()

            # Chute du bloc courant
            if count < self.SPEED:
                count += 1
            elif count == self.SPEED:
                self.fig.fall()
                count = 0

            self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game(window=(230, 300))
    game.game_loop()
