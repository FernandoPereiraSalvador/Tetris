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

        # Aumentar el ancho de la pantalla para incluir el área de la próxima figura
        self.next_figure_width = 200
        self.screen = pygame.display.set_mode(
            (self.game_width + 2 * self.border_size + self.next_figure_width, self.game_height + 2 * self.border_size)
        )

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
        # Dibujar la próxima figura a la derecha del área del juego
        next_figure_text = self.font.render("Next:", True, (255, 255, 255))
        next_figure_rect = next_figure_text.get_rect(
            center=(self.game_width + self.border_size + self.next_figure_width // 2, self.border_size + 30))
        self.screen.blit(next_figure_text, next_figure_rect)

        # Ajustar la posición de la próxima figura
        next_figure_surf = self.next_figure.surf
        next_figure_rect = next_figure_surf.get_rect(
            center=(self.game_width + self.border_size + self.next_figure_width // 2, self.border_size + 100))
        self.screen.blit(next_figure_surf, next_figure_rect)

    def draw_score(self):
        # Dibujar la puntuación debajo de la próxima figura
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(
            center=(self.game_width + self.border_size + self.next_figure_width // 2, self.border_size + 200))
        self.screen.blit(score_text, score_rect)

    def draw_border(self):
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (0, 0, self.game_width + 2 * self.border_size + self.next_figure_width, self.border_size))  # Borde superior
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (0, 0, self.border_size, self.game_height + 2 * self.border_size))  # Borde izquierdo
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.game_width + self.border_size, 0, self.border_size,
                          self.game_height + 2 * self.border_size))  # Borde derecho
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (0, self.game_height + self.border_size,
                          self.game_width + 2 * self.border_size + self.next_figure_width, self.border_size))  # Borde inferior

    def draw_start_screen(self):
        self.screen.fill((0, 0, 0))
        start_text = self.font.render("Press any key to start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(start_text, start_rect)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

    def draw_final_screen(self):
        self.screen.fill((0, 0, 0))
        final_text = self.font.render("Game Over", True, (255, 255, 255))
        final_text_rect = final_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 30))
        self.screen.blit(final_text, final_text_rect)

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 30))
        self.screen.blit(score_text, score_text_rect)

        pygame.display.flip()
        pygame.time.delay(2000)  # Delay para que el jugador pueda ver la pantalla final

    def run_game(self):
        self.draw_start_screen()
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

            # Dibujar la cuadrícula
            self.draw_grid()

            # Dibujar la siguiente figura
            self.draw_next_figure()

            # Mover y dibujar la figura actual
            if not self.figures[-1].move():
                # Comprobar condición de game over
                if any(self.board.grid[1]):
                    pygame.time.delay(500)
                    self.game_over = True
                    print("Game Over")
                    break
                self.figures.append(self.next_figure)
                self.next_figure = Figure(self.board)
                self.score += 10

            # Dibujar la figura actual
            self.draw_figure(self.figures[-1])

            # Dibujar la puntuación
            self.draw_score()

            pygame.display.flip()
            self.clock.tick(5)

        self.draw_final_screen()


if __name__ == "__main__":
    tetris_game = TetrisGame()
    tetris_game.run_game()
