import time
import numpy as np

BORDER = "+---+---+---+"

def read_grid(path):
        """Reads in the grid (given with 0s as blanks and numbers as populated values)."""
        with open(path, 'r') as file:
            content = file.read().strip().splitlines()
        content = [[int(cell) for cell in row] for row in content]
        
        # Equivalent to:
        # content = []
        # for row in content:
        #     row_data = []
        #     for cell in row:
        #         row_data.append(int(cell))
        #     content.append(row_data)

        return np.array(content, dtype=np.int8)

def is_valid(grid, last_move) -> bool:
    """Examines the sudoku board around the last entry and determines whether
    the board is valid."""

    row_index, col_index = last_move

    row = grid[row_index, :]  # Constructing the row to be tested
    col = grid[:, col_index]  # Constructing the column to be tested

    # Constructing the cell block to be tested
    top_left = (row_index - row_index % 3, col_index - col_index % 3)
    cell_block = grid[
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


def three_chunk(lst: list, delimiter: str):
    """Takes in a list of strings, and groups the elements of the list evenly into chunks of 3 separated by a delimiter."""
    return [delimiter.join(lst[i:i + 3]) for i in range(0, len(lst), 3)]


def render(grid, print_delay=None):
    """A function that prints the grid to the terminal."""
    out_lst = []

    for row in grid:
        row = [str(element) for element in row]
        row = three_chunk(row, "")  # Forming the row into chunks of 3

        out_lst.append("|" + "|".join(row) + "|")

    out_lst = three_chunk(out_lst, "\n")

    to_print = "\n".join([BORDER, out_lst[0], BORDER,
                out_lst[1], BORDER, out_lst[2], BORDER])
    to_print = to_print.replace("0", " ")

    print(to_print, flush=True)
    if print_delay is not None:
        time.sleep(print_delay)

    return


def record_preoccupied_cells(grid):
    """Given the grid, generates a list of the cells that are preoccupied."""
    prepopulated_lst = []
    for row_index in range(len(grid)):
        for col_index in range(len(grid[row_index])):
            if grid[row_index, col_index] != 0:
                prepopulated_lst.append((row_index, col_index))
    return prepopulated_lst


def solve_sudoku(row=0, col=0):
    """An implementation of the backtracking algorithm using recursion."""

    global grid, prepopulated
    # Defining progression conditions
    if col > 8:  # Going to the next row
        return solve_sudoku(row + 1, 0)

    if row > 8:  # Finished!
        return True

    if (row, col) in prepopulated:  # Just move on
        return solve_sudoku(row, col + 1)

    # Guessing each number
    for guess in range(1, 10):
        grid[row, col] = guess
        if is_valid(grid, (row, col)):
            if solve_sudoku(row, col + 1):
                return True

    grid[row, col] = 0  # Resetting the value for the backtracking
    return False


if __name__ == "__main__":
    grid = read_grid("sudokus/1.txt")
    prepopulated = record_preoccupied_cells(grid)
    render(grid)
    solve_sudoku()
    render(grid)
