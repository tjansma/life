"""Conway's game of life."""

from abc import ABCMeta, abstractmethod
import copy
import sys
import time

import pygame

CELL_SIZE = 25
CELL_COUNT_HORIZONTAL = 32
CELL_COUNT_VERTICAL = 24
MAIN_WINDOWS_SIZE = (CELL_COUNT_HORIZONTAL * CELL_SIZE, 
                     CELL_COUNT_VERTICAL * CELL_SIZE)
NEXT_STEP_INTERVAL = 0.25

class IBoard(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, "toggle") and callable(subclass.toggle) and
                hasattr(subclass, "next_step") and callable(subclass.next_step)
        )     

    @abstractmethod
    def toggle(self, x: int, y: int) -> None:
        """Toggle live/dead status of cell at specified coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        raise NotImplementedError
    
    @abstractmethod
    def next_step(self):
        """Generate next step according to Conway's game of life rules:
        1. Any live cell with fewer than two live neighbors dies, as if by
           underpopulation.
        2. Any live cell with two or three live neighbors lives on to the next
           generation.
        3. Any live cell with more than three live neighbors dies, as if by
           overpopulation.
        4. Any dead cell with exactly three live neighbors becomes a live
           cell, as if by reproduction.

        Returns:
            IBoard: board object with new generations.
        """
        raise NotImplementedError

class Board(IBoard):        
    def __init__(self, grid: list[list[bool]] = None):
        if grid is None:
            self.grid = [[False] * CELL_COUNT_HORIZONTAL for i in
                        range(CELL_COUNT_VERTICAL)]
        else:
            self.grid = copy.deepcopy(grid)

    def toggle(self, x: int, y: int) -> None:
        """Toggle live/dead status of cell at specified coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        self.grid[y][x] = not self.grid[y][x]

    def _get_neighbour_count(self, x: int, y: int) -> int:
        """Count number of neighbours of cell at specified coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            int: number of neighbours of cell at position (x, y)
        """
        neighbour_count = 0
        for neighbour_y in range(max(0, y-1), min(y+2, len(self.grid))):
            for neighbour_x in range(max(0, x-1), min(x+2, len(self.grid[neighbour_y]))):
                if not (neighbour_x == x and neighbour_y == y):
                    neighbour_count += 1 if self.grid[neighbour_y][neighbour_x] else 0

        return neighbour_count

    def next_step(self) -> IBoard:
        """Generate next step according to Conway's game of life rules:
        1. Any live cell with fewer than two live neighbors dies, as if by
           underpopulation.
        2. Any live cell with two or three live neighbors lives on to the next
           generation.
        3. Any live cell with more than three live neighbors dies, as if by
           overpopulation.
        4. Any dead cell with exactly three live neighbors becomes a live
           cell, as if by reproduction.

        Returns:
            IBoard: board object with new generations.
        """
        next_board = Board()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                neighbour_count = self._get_neighbour_count(x, y)
                if self.grid[y][x]:
                    if neighbour_count < 2:
                        next_board.grid[y][x] = False
                    elif neighbour_count > 3:
                        next_board.grid[y][x] = False
                    else:
                        next_board.grid[y][x] = True
                else:
                    if neighbour_count == 3:
                        next_board.grid[y][x] = True

        return next_board


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

    board = Board()
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
