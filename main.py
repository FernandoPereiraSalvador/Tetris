import pygame
import sys
import random

# Configuración inicial
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Tamaño de las casillas
cell_size = 40
grid_width = 800 // cell_size
grid_height = 600 // cell_size

# Piezas del Tetris
pieces = [
    [[1, 1, 1, 1]],

    [[1, 1, 1],
     [0, 1, 0]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[0, 1, 1],
     [1, 1]],
]


class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

    def clear_line(self, line):
        del self.grid[line]
        self.grid.insert(0, [0 for _ in range(grid_width)])


class Figure(pygame.sprite.Sprite):
    def __init__(self, board):
        super().__init__()
        self.shape = random.choice(pieces)
        self.surf = pygame.Surface((cell_size * len(self.shape[0]), cell_size * len(self.shape)))
        self.surf.fill((0, 0, 0))  # Rellenar con color de fondo
        self.rect = self.surf.get_rect(topleft=(400, 0))
        self.board = board

        # Dibujar los bloques de la figura (excluyendo espacios en blanco)
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.surf, (255, 255, 255),
                                     pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0 and not self.check_collision(-1, 0):
            self.rect.move_ip(-cell_size, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < 800 and not self.check_collision(1, 0):
            self.rect.move_ip(cell_size, 0)

        # Cambios en la lógica de movimiento hacia abajo
        if self.rect.bottom < 600 and not self.check_collision(0, 1):
            self.rect.move_ip(0, cell_size)
        else:
            self.update_board()
            return False

        return True

    def check_collision(self, dx, dy):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:  # Solo considerar las celdas ocupadas de la figura
                    new_x = (self.rect.left // cell_size) + x + dx
                    new_y = (self.rect.top // cell_size) + y + dy
                    if new_x < 0 or new_x >= grid_width or new_y >= grid_height or (
                            new_y >= 0 and self.board.grid[new_y][new_x]):
                        return True
        return False

    def update_board(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = (self.rect.left // cell_size) + x
                    grid_y = (self.rect.top // cell_size) + y
                    if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
                        self.board.grid[grid_y][grid_x] = 1

        self.board.clear_line(0)


def draw_grid(board):
    for y, row in enumerate(board.grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (255, 255, 255),
                                 pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size), 1)


# Bucle del juego
board = Board()
figures = [Figure(board)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    # Dibujar la cuadrícula
    draw_grid(board)

    # Mover y dibujar la figura actual
    if not figures[-1].move():
        figures.append(Figure(board))

    # Dibujar la figura actual en cada iteración
    screen.blit(figures[-1].surf, figures[-1].rect.topleft)

    pygame.display.flip()
    clock.tick(5)
