import random
import pygame

from constants import *


class Figure(pygame.sprite.Sprite):
    def __init__(self, board):
        super().__init__()
        self.shape = random.choice(PIECES)
        self.surf = pygame.Surface((CELL_SIZE * len(self.shape[0]), CELL_SIZE * len(self.shape)))
        self.surf.fill((0, 0, 0))  # Rellenar con color de fondo
        self.rect = self.surf.get_rect(topleft=(400, 0))
        self.board = board

        # Dibujar los bloques de la figura (excluyendo espacios en blanco)
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.surf, (255, 255, 255),
                                     pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0 and not self.check_collision(-1, 0):
            self.rect.move_ip(-CELL_SIZE, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < 800 and not self.check_collision(1, 0):
            self.rect.move_ip(CELL_SIZE, 0)

        # Cambios en la lógica de movimiento hacia abajo
        if self.rect.bottom < 600 and not self.check_collision(0, 1):
            self.rect.move_ip(0, CELL_SIZE)
        else:
            self.update_board()
            return False

        return True

    def check_collision(self, dx, dy):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:  # Solo considerar las celdas ocupadas de la figura
                    new_x = (self.rect.left // CELL_SIZE) + x + dx
                    new_y = (self.rect.top // CELL_SIZE) + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (
                            new_y >= 0 and self.board.grid[new_y][new_x]):
                        return True
        return False

    def update_board(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = (self.rect.left // CELL_SIZE) + x
                    grid_y = (self.rect.top // CELL_SIZE) + y
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        self.board.grid[grid_y][grid_x] = 1

        self.board.clear_line(0)