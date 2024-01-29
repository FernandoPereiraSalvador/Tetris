import pygame
import sys
from classes.board import Board
from classes.figure import Figure
from constants import *

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.border_size = 10  # Ancho del borde blanco
        self.game_width = GRID_WIDTH * CELL_SIZE
        self.game_height = GRID_HEIGHT * CELL_SIZE

        # Creamos la pantalla solo para el área del juego más el borde
        self.screen = pygame.display.set_mode(
            (self.game_width + 2 * self.border_size + 200, self.game_height + 2 * self.border_size))
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.figures = [Figure(self.board)]
        self.next_figure = Figure(self.board)  # Nueva instancia para la próxima figura
        self.game_over = False
        self.score = 0

        # Fuente y tamaño del texto
        self.font = pygame.font.Font(None, 36)

    def draw_grid(self):
        for y, row in enumerate(self.board.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, cell,
                                     pygame.Rect(x * CELL_SIZE + self.border_size, y * CELL_SIZE + self.border_size,
                                                 CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     pygame.Rect(x * CELL_SIZE + self.border_size, y * CELL_SIZE + self.border_size,
                                                 CELL_SIZE, CELL_SIZE), 1)

    def draw_figure(self, figure):
        self.screen.blit(figure.surf, (figure.rect.x + self.border_size, figure.rect.y + self.border_size))

    def draw_next_figure(self):
        # Dibujar la próxima figura centrada
        next_figure_text = self.font.render("Next:", True, (255, 255, 255))
        next_figure_rect = next_figure_text.get_rect()
        next_figure_rect.midtop = (self.game_width + 2 * self.border_size + 100, self.border_size + 10 + 100)
        self.screen.blit(next_figure_text, next_figure_rect)

        next_figure_surf = self.next_figure.surf
        next_figure_rect = next_figure_surf.get_rect()
        next_figure_rect.midtop = (self.game_width + 2 * self.border_size + 100, self.border_size + 50 + 10 + 100)
        self.screen.blit(next_figure_surf, next_figure_rect)

    def draw_score(self):
        # Dibujar la puntuación abajo de la próxima figura pero más arriba
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.midtop = (self.game_width + 2 * self.border_size + 100, self.border_size + 50)
        self.screen.blit(score_text, score_rect)

    def draw_border(self):
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (0, 0, self.game_width + 2 * self.border_size + 200, self.border_size))  # Borde superior
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (0, 0, self.border_size, self.game_height + 2 * self.border_size))  # Borde izquierdo
        pygame.draw.rect(self.screen, (255, 255, 255), (self.game_width + self.border_size, 0, self.border_size,
                                                        self.game_height + 2 * self.border_size))  # Borde derecho
        pygame.draw.rect(self.screen, (255, 255, 255), (
        0, self.game_height + self.border_size, self.game_width + 2 * self.border_size + 200,
        self.border_size))  # Borde inferior

    def run_game(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.figures[-1].rotate()

            self.screen.fill((0, 0, 0))

            # Dibujar el borde
            self.draw_border()

            # Draw the grid
            self.draw_grid()

            # Draw the next figure
            self.draw_next_figure()

            # Move and draw the current figure
            if not self.figures[-1].move():
                # Check for game over condition
                if any(self.board.grid[1]):
                    pygame.time.delay(500)
                    self.game_over = True
                    print("Game Over")
                    break
                self.figures.append(self.next_figure)
                self.next_figure = Figure(self.board)
                self.score += 10

            # Draw the current figure on each iteration with its color
            self.draw_figure(self.figures[-1])

            # Draw the score
            self.draw_score()

            pygame.display.flip()
            self.clock.tick(5)


if __name__ == "__main__":
    tetris_game = TetrisGame()
    tetris_game.run_game()
