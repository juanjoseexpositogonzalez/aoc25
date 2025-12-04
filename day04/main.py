from pathlib import Path
from typing import List, Final
from itertools import product

PAPER_ROLL: Final[str] = '@'
TEST_FILE: Final[str] = 'test.txt'
INPUT_FILE: Final[str] = 'input.txt'
DIRECTIONS: Final[List[tuple[int, int]]] = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1),
]
MAX_ADJACENT_ROLLS: Final[int] = 4

def read_input(file_path: Path) -> List[str]:
    """
    Read the input data from the file.

    Args:
        file_path: The path to the file to read.

    Returns:
        The input data as a list of strings.
    """
    with open(file_path, 'r') as file:
        return file.read().splitlines()


def is_paper_roll(input_data: List[str], i: int, j: int) -> bool:
    """
    Check if the cell is a paper roll.

    Args:
        input_data: The input data.
        i: The row index.
        j: The column index.

    Returns:
        True if the cell is a paper roll, False otherwise.
    """
    return input_data[i][j] == PAPER_ROLL

def count_adjacent_rolls(grid: List[str], i: int, j: int) -> int:
    """
    Count the number of adjacent rolls.

    Args:
        grid: The grid.
        i: The row index.
        j: The column index.

    Returns:
        The number of adjacent rolls.
    """
    rows, cols = len(grid), len(grid[0])
    return sum(
        is_paper_roll(grid, i + di, j + dj)
        for di, dj in DIRECTIONS
        if 0 <= i + di < rows and 0 <= j + dj < cols
    )

def count_accesible_rolls(grid: List[str]) -> int:
    """
    Count the number of accessible rolls.

    Args:
        grid: The grid.

    Returns:
        The number of accessible rolls.
    """
    accesible_rolls: int = 0
    rows, cols = len(grid), len(grid[0])
    for row, col in product(range(rows), range(cols)):
        if is_paper_roll(grid, row, col):
            neighbors: int = count_adjacent_rolls(grid, row, col)
            if neighbors < MAX_ADJACENT_ROLLS:
                accesible_rolls += 1
    return accesible_rolls


def main() -> None:
    """
    Main function to solve the problem.

    Args:
        None.

    Returns:
        None.
    """
    input_data = read_input(Path(INPUT_FILE))
    accessible_rolls = count_accesible_rolls(input_data)
    print(accessible_rolls)


if __name__ == '__main__':
    main()