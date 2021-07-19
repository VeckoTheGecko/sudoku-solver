from typing import Tuple
import numpy as np

from views import CommandView


class Sudoku:
    def __init__(self, view, sudoku_path=None):
        """A function to initialise the sudoku given a view and a sudoku_path.

        view: A view object that is capable of rendering the scene.
        sudoku_path: A string leading to the sudoku text file. 0s represent blank spaces and numbers represent populated spaces."""

        self.view = view

        # List[List] Making a list of lists
        if sudoku_path is not None:
            self.grid = self.read_grid(sudoku_path)
            assert self.grid.shape == (
                9, 9), "The sudoku file is of improper dimensions"

        else:
            self.grid = np.zeros(shape=(9, 9), dtype=np.int8)

        self.record_preoccupied_cells()

    def read_grid(self, path):
        """Reads in the grid (given with 0s as blanks and numbers as populated values)."""
        with open(path, 'r', encoding="utf-8") as file:
            content = file.read().strip().splitlines()
        content = [[int(cell) for cell in row] for row in content]

        return np.array(content, dtype=np.int8)

    def record_preoccupied_cells(self) -> None:
        """Given the grid, generates a list of the cells that are preoccupied."""
        populated_set = set()
        for row_index in range(len(self.grid)):
            for col_index in range(len(self.grid[row_index])):
                if self.grid[row_index, col_index] != 0:
                    populated_set.add((row_index, col_index))

        self.prepopulated = populated_set
        return

    def is_valid(self, last_move) -> bool:
        """Examines the sudoku board around the last entry and determines whether
        the board is valid."""

        row_index, col_index = last_move

        row = self.grid[row_index, :]  # Constructing the row to be tested
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
    
    def before_iteration(self):
        """A function that is called before the solving algorithm begins."""
        self.view.render(self.grid)

    def between_iteration(self):
        """A function that is called between a new item is guessed in the sudoku grid."""
        # self.view.render(self.grid)
        return

    def when_done(self):
        """A function that is called the final result is determined."""
        self.view.render(self.grid)
        print("We're done now!!")
        return

    def solve(self, row=0, col=0):
        """An implementation of the backtracking algorithm using recursion."""
        # Implementing before_iteration call
        if row==0 and col==0:
            self.before_iteration()

        # Defining progression conditions
        if col > 8:  # Going to the next row
            return self.solve(row + 1, 0)

        if row > 8:  # Finished!
            self.between_iteration()
            self.when_done()
            return True

        if (row, col) in self.prepopulated:  # Just move on
            return self.solve(row, col + 1)

        # Guessing each number
        for guess in range(1, 10):
            self.grid[row, col] = guess
            self.between_iteration()
            if self.is_valid((row, col)):
                if self.solve(row, col + 1):
                    return True

        self.grid[row, col] = 0  # Resetting the value for the backtracking
        self.between_iteration()  # Temp
        return False


if __name__ == "__main__":
    view = CommandView()  # delay=0.0001)
    sudoku = Sudoku(view, sudoku_path="sudokus/2.txt")
    sudoku.solve()
