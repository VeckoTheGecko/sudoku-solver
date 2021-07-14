from typing import Tuple

import numpy as np

from exceptions import LastMoveException


class Sudoku:
    def __init__(self, view=None, sudoku_path=None):
        """A function to initialise the sudoku given a view and a sudoku_path.

        :param view: A view object that is capable of rendering the scene.
        :param sudoku_path: A string leading to the sudoku text file. 0s represent blank spaces and numbers represent populated spaces."""

        self.view = view

        # List[List] Making a list of lists
        if sudoku_path is not None:
            self.load_grid(np.fromfile(sudoku_path, dtype=np.int8))
            assert self.grid.shape == (
                9, 9), "The sudoku file is of improper dimensions"

        self.load_grid(np.zeros(shape=(9, 9), dtype=np.int8))

        self.last_move = None

    def load_grid(self, grid: np.ndarray) -> None:
        """Loads the grid (given with 0s as blanks and numbers as populated values). The function defines self.grid and self.prepopulated."""
        self.grid = grid

        populated_set = set()
        for row_index, row in enumerate(grid):
            for col_index, col in enumerate(row):
                if grid[row_index, col_index] != 0:
                    populated_set.add((row_index, col_index))

        self.prepopulated = populated_set
        return

    def set_last_move(self, last_move: Tuple[int, int]) -> None:
        """Records the position of the cell that was changed last."""
        self.last_move = last_move
        return

    def is_valid(self) -> bool:
        """Examines the sudoku board around the last entry and determines whether
        the board is valid."""

        if self.last_move is None:
            raise LastMoveException("Last move has not been properly recorded")
        else:
            row_index, col_index = self.last_move

        row = self.grid[row_index, :]  # Contructing the row to be tested
        col = self.grid[:, col_index]  # Constructing the column to be tested

        # Constructing the cell block to be tested
        top_left = (row_index - row_index % 3, col_index - col_index % 3)
        cell_block = self.grid[
            top_left[0]: top_left[0] + 3, top_left[1]: top_left[1] + 3
        ]
        cell_block = cell_block.flatten()

        # Testing each to make sure no duplicate values
        for test_set in [row, col, cell_block]:
            unique, counts = np.unique(test_set, return_counts=True)
            # Occurrences of each number in test_set
            occurrences = dict(zip(unique, counts))

            # Going through unique values checking for no duplicates
            for number in occurrences:
                if occurrences[number] > 1 and number != 0:
                    return False

        # All checks passed
        return True

    def between_iteration(self):
        """A function that is called between a new item is guessed in the sudoku grid."""
        return

    def solve(self):
        """An implementation of the backtracking algorithm using recursion."""


if __name__ == "__main__":
    sudoku = Sudoku()
    sudoku.grid[6:, 6:] = np.array([[0, 0, 4], [4, 5, 6], [7, 8, 9]])
    sudoku.set_last_move((7, 7))
    print(sudoku.is_valid())
