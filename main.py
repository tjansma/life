"""Conway's game of life."""

import sys
import time

import pygame

from conway import Board

CELL_SIZE = 25
CELL_COUNT_HORIZONTAL = 32
CELL_COUNT_VERTICAL = 24
MAIN_WINDOWS_SIZE = (CELL_COUNT_HORIZONTAL * CELL_SIZE, 
                     CELL_COUNT_VERTICAL * CELL_SIZE)
NEXT_STEP_INTERVAL = 0.25

def draw_board(surface: pygame.Surface, board: Board) -> None:
    """Draw Conway board on given pygame Surface.

    Args:
        surface (pygame.Surface): surface to draw on.
        board (Board): Conway's game of life board.
    """
    CELL_COLOR = (255, 255, 255) # White
    BG_COLOR = (0, 0, 0) # Black

    window = pygame.Rect(0, 0, MAIN_WINDOWS_SIZE[0], MAIN_WINDOWS_SIZE[1])
    pygame.draw.rect(surface, BG_COLOR, window)

    for y in range(len(board.grid)):
        for x in range(len(board.grid[y])):
            if board.grid[y][x]:
                cell_square = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, CELL_COLOR, cell_square, width=10)

def main():
    """Execute main function."""
    # MAIN_WINDOWS_SIZE = (800, 600)

    screen = pygame.display.set_mode(MAIN_WINDOWS_SIZE)

    board = Board(size_x=CELL_COUNT_HORIZONTAL, size_y=CELL_COUNT_VERTICAL)
    board.toggle(0, 1)
    board.toggle(1, 2)
    board.toggle(2, 0)
    board.toggle(2, 1)
    board.toggle(2, 2)
    

    exit_game = False
    generation = 0
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
        
        draw_board(screen, board)
        pygame.display.update()

        time.sleep(NEXT_STEP_INTERVAL)

        generation += 1
        generation_start_time = time.time_ns()
        board = board.next_step()
        generation_calculation_time = time.time_ns() - generation_start_time
        print(f"Generation #{generation} calculated in: {generation_calculation_time / 1000000} ms")

    return 0


# --- Program entry ---
if __name__ == "__main__":
    sys.exit(main())
