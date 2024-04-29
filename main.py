"""Conway's game of life."""

import sys

import pygame

CELL_SIZE = 25
CELL_COUNT_HORIZONTAL = 32
CELL_COUNT_VERTICAL = 24
MAIN_WINDOWS_SIZE = (CELL_COUNT_HORIZONTAL * CELL_SIZE, 
                     CELL_COUNT_VERTICAL * CELL_SIZE)


class Board:        
    def __init__(self):
        self.grid = [[False] * CELL_COUNT_HORIZONTAL for i in
                     range(CELL_COUNT_VERTICAL)]

    def toggle(self, cell_x, cell_y):
        self.grid[cell_y][cell_x] = not self.grid[cell_y][cell_x]


def main():
    """Execute main function."""
    MAIN_WINDOWS_SIZE = (800, 600)

    screen = pygame.display.set_mode(MAIN_WINDOWS_SIZE)

    print(Board().grid)

    exit_game = False
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(100, 100, 75, 50))
        pygame.display.update()

    return 0


# --- Program entry ---
if __name__ == "__main__":
    sys.exit(main())
