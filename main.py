"""Conway's game of life."""

import sys

import pygame

import conway

CELL_SIZE = 25
CELL_COUNT_HORIZONTAL = 32
CELL_COUNT_VERTICAL = 24
MAIN_WINDOW_SIZE = (CELL_COUNT_HORIZONTAL * CELL_SIZE, 
                    CELL_COUNT_VERTICAL * CELL_SIZE)
NEXT_STEP_INTERVAL_IN_MS = 250

class PygameBoard:
    def __init__(self, board: conway.IBoard, surface: pygame.Surface):
        self.board = board
        self.surface = surface
        self._updated = False

    def draw_board(self) -> None:
        """Draw Conway board on given pygame Surface.

        Args:
            surface (pygame.Surface): surface to draw on.
            board (Board): Conway's game of life board.
        """
        if self._updated:
            CELL_COLOR = (255, 255, 255) # White
            BG_COLOR = (0, 0, 0) # Black

            window = pygame.Rect(0, 0, MAIN_WINDOW_SIZE[0], MAIN_WINDOW_SIZE[1])
            pygame.draw.rect(self.surface, BG_COLOR, window)

            for y in range(len(self.board.grid)):
                for x in range(len(self.board.grid[y])):
                    if self.board.grid[y][x]:
                        cell_square = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.surface, CELL_COLOR, cell_square, width=10)

        self._updated = False

    def next_step(self) -> None:
        """Calculate next generation of board.
        """
        self.board = self.board.next_step()
        self._updated = True

def main():
    """Execute main function."""
    screen = pygame.display.set_mode(MAIN_WINDOW_SIZE)

    board = conway.Board(size_x=CELL_COUNT_HORIZONTAL, size_y=CELL_COUNT_VERTICAL)
    board.toggle(0, 1)
    board.toggle(1, 2)
    board.toggle(2, 0)
    board.toggle(2, 1)
    board.toggle(2, 2)
    pg_board = PygameBoard(board, screen)

    pygame.time.set_timer(pygame.USEREVENT, NEXT_STEP_INTERVAL_IN_MS)

    exit_game = False
    generation = 0
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.USEREVENT:
                generation += 1
                pg_board.next_step()
                pg_board.draw_board()

        pygame.display.update()

    return 0


# --- Program entry ---
if __name__ == "__main__":
    sys.exit(main())
