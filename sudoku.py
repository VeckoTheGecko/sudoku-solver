from typing import List, Tuple
import numpy as np
from numpy.lib.arraysetops import unique


from exceptions import LastMoveException


class Sudoku:
    def __init__(self):
        # List[List] Making a list of lists
        self.grid = np.zeros(shape=(9, 9), dtype=np.int8)
        self.last_move = None

        # Would be a list of tuples containing (row,col) information of the entries that are predefined
        self.prepopulated = None

    def set_last_move(self, last_move: Tuple[int, int]) -> None:
        self.last_move = last_move
        return

    def is_valid(self):
        if self.last_move is None:
            raise LastMoveException("Last move has not been properly recorded")
        else:
            row_index, col_index = self.last_move

        row = self.grid[row_index, :]  # Contructing the row to be tested
        col = self.grid[:, col_index]  # Constructing the column to be tested

        # Constructing the cell block to be tested
        top_left = (row_index - row_index % 3, col_index - col_index % 3)
        cell_block = self.grid[
            top_left[0] : top_left[0] + 3, top_left[1] : top_left[1] + 3
        ]
        cell_block = cell_block.flatten()

        # Testing each to make sure no duplicate values
        for test_set in [row, col, cell_block]:
            unique, counts = np.unique(test_set, return_counts=True)
            # Occurences of each number in test_set
            occurences = dict(zip(unique, counts))

            # Going through unique values checking for no duplicates
            for number in occurences:
                if occurences[number] > 1 and number != 0:
                    return False

        return True


if __name__ == "__main__":
    sudoku = Sudoku()
    sudoku.grid[6:, 6:] = np.array([[0, 0, 4], [4, 5, 6], [7, 8, 9]])
    sudoku.set_last_move((7, 7))
    print(sudoku.is_valid())
