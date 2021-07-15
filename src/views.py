import numpy as np
import time


def three_chunk(lst: list, delimiter: str):
    """Takes in a list of strings, and groups the elements of the list evenly into chunks of 3 separated by a delimiter."""
    return [delimiter.join(lst[i:i + 3]) for i in range(0, len(lst), 3)]


class CommandView:
    """A very rudimentary view used to develop the backtracking algorithm."""
    BORDERS = {
        "top": "+---+---+---+",  # "┌───┬───┬───┐",
        "middle": "+---+---+---+",  # "├───┼───┼───┤",
        "bottom": "+---+---+---+",  # "└───┴───┴───┘"}
    }

    def __init__(self, delay: float = None):
        """A view used to render in the terminal.
        :param delay: number of seconds between grid re-render refreshes."""

        self.delay = delay

    def render(self, grid: np.ndarray, print_bool: bool = True) -> None:
        """Formats the grid and prints it out to terminal."""
        out_lst = []

        for row in grid:
            row = [str(element) for element in row]
            row = three_chunk(row, "")  # Forming the row into chunks of 3

            out_lst.append("|" + "|".join(row) + "|")

        out_lst = three_chunk(out_lst, "\n")

        to_print = "\n".join([self.BORDERS["top"], out_lst[0], self.BORDERS["middle"],
                             out_lst[1], self.BORDERS["middle"], out_lst[2], self.BORDERS["bottom"]]).replace("0", " ")

        if print_bool:
            print(to_print, flush=True)
            if self.delay is not None:
                time.sleep(self.delay)

        return to_print
