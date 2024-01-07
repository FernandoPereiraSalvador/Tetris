import pygame
import sys
from classes.board import Board
from classes.figure import Figure
from constants import *

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.figures = [Figure(self.board)]

    def draw_grid(self):
        for y, row in enumerate(self.board.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, cell,
                                     pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw_figure(self, figure):
        self.screen.blit(figure.surf, figure.rect.topleft)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))

            # Draw the grid
            self.draw_grid()

            # Move and draw the current figure
            if not self.figures[-1].move():
                self.figures.append(Figure(self.board))

            # Draw the current figure on each iteration with its color
            self.draw_figure(self.figures[-1])

            pygame.display.flip()
            self.clock.tick(5)

if __name__ == "__main__":
    tetris_game = TetrisGame()
    tetris_game.run_game()