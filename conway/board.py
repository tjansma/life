from abc import ABCMeta, abstractmethod
import copy

_DEFAULT_BOARD_SIZE_X = 32
_DEFAULT_BOARD_SIZE_Y = 24

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
    def __init__(self, size_x: int = _DEFAULT_BOARD_SIZE_X, size_y: int = _DEFAULT_BOARD_SIZE_Y, grid: list[list[bool]] = None):
        """Create new board/grid for Conway's game of life of specified size.
        If an existing grid is supplied, size_x and size_y dimensions are
        ignored and the new board will be a copy with the same dimensions of
        the supplied grid.

        Args:
            size_x (int, optional): Horizontal board size. 
                                    Defaults to _DEFAULT_BOARD_SIZE_X.
            size_y (int, optional): Vertical board size. 
                                    Defaults to _DEFAULT_BOARD_SIZE_Y.
            grid (list[list[bool]], optional): an existing grid. 
                                               Defaults to None.
        """
        if grid is None:
            self.grid = [[False] * size_x for i in
                        range(size_y)]
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
