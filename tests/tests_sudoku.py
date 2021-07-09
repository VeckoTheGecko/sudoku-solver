from unittest import TestCase
import numpy as np
from sudoku import Sudoku


class TestSudoku(TestCase):
    def setUp(self) -> None:
        # Initialising 6 boards
        self.sudoku = Sudoku()

    def test_row(self):
        # Correct first row
        self.sudoku.grid[0, :] = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.sudoku.set_last_move((0, 0))
        self.assertTrue(self.sudoku.is_valid())

        # Incorrect 4th row
        self.setUp()
        self.sudoku.grid[3, :] = np.array([1, 2, 3, 3, 5, 6, 7, 8, 9])
        self.sudoku.set_last_move((3, 0))
        self.assertFalse(self.sudoku.is_valid())

    def test_column(self):
        # Correct first column
        self.sudoku.grid[:, 0] = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.sudoku.set_last_move((0, 0))
        self.assertTrue(self.sudoku.is_valid())

        # Incorrect last column
        self.setUp()
        self.sudoku.grid[:, -1] = np.array([2, 2, 3, 3, 5, 6, 7, 7, 9])
        self.sudoku.set_last_move((0, 8))
        self.assertFalse(self.sudoku.is_valid())

    def test_cell_block(self):
        # Correct first block
        self.sudoku.grid[:3, :3] = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.sudoku.set_last_move((0, 0))
        self.assertTrue(self.sudoku.is_valid())

        # Correct other block
        self.setUp()
        self.sudoku.grid[3:6, 6:] = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.sudoku.set_last_move((4, 7))
        self.assertTrue(self.sudoku.is_valid())

        # Incorrect block
        self.setUp()
        self.sudoku.grid[6:, 6:] = np.array([[0, 0, 4], [4, 5, 6], [7, 8, 9]])
        self.sudoku.set_last_move((7, 7))
        self.assertFalse(self.sudoku.is_valid())
