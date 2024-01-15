import random
import pygame

from constants import *


class Figure(pygame.sprite.Sprite):
    def __init__(self, board):
        super().__init__()
        self.shape = random.choice(PIECES)
        self.color = COLORS[PIECES.index(self.shape)]  # Assign color according to the figure
        self.surf = pygame.Surface((CELL_SIZE * len(self.shape[0]), CELL_SIZE * len(self.shape)), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(400, 0))
        self.board = board

        # Draw the blocks of the figure (excluding blanks).
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.surf, self.color + (128,),  # Agregar canal alfa para transparencia
                                     pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0 and not self.check_collision(-1, 0):
            self.rect.move_ip(-CELL_SIZE, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < 800 and not self.check_collision(1, 0):
            self.rect.move_ip(CELL_SIZE, 0)

        if self.rect.bottom < 600 and not self.check_collision(0, 1):
            self.rect.move_ip(0, CELL_SIZE)
        else:
            self.update_board()
            self.board.check_and_clear_lines()
            return False

        return True

    def check_collision(self, dx, dy, shape=None):
        shape_to_check = shape or self.shape
        for y, row in enumerate(shape_to_check):
            for x, cell in enumerate(row):
                if cell:
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
                        self.board.grid[grid_y][grid_x] = self.color

        self.board.clear_line(0)

    def rotate(self):
        rotated_shape = list(zip(*reversed(self.shape)))
        if not self.check_collision(0, 0, rotated_shape):
            self.shape = rotated_shape
            self.update_surface()

    def update_surface(self):
        self.surf = pygame.Surface((CELL_SIZE * len(self.shape[0]), CELL_SIZE * len(self.shape)), pygame.SRCALPHA)
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.surf, self.color + (128,),
                                     pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))