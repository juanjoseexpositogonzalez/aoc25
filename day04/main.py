from pathlib import Path
from typing import List, Final, Set, Tuple
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
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    return sum(
        is_paper_roll(grid, i + di, j + dj)
        for di, dj in DIRECTIONS
        if 0 <= i + di < rows and 0 <= j + dj < cols
    )

def count_accessible_rolls(grid: List[str]) -> int:
    """
    Count the number of accessible rolls.

    Args:
        grid: The grid.

    Returns:
        The number of accessible rolls.
    """
    if not grid or not grid[0]:
        return 0
    accesible_rolls: int = 0
    rows, cols = len(grid), len(grid[0])
    for row, col in product(range(rows), range(cols)):
        if is_paper_roll(grid, row, col):
            neighbors: int = count_adjacent_rolls(grid, row, col)
            if neighbors < MAX_ADJACENT_ROLLS:
                accesible_rolls += 1
    return accesible_rolls


# FUNCIONES PART2
def get_roll_positions(grid: List[str]) -> Set[tuple[int, int]]:
    """
    Get the positions of all paper rolls.
    """
    return {
        (i, j)
        for i, row in enumerate(grid)
        for j, c in enumerate(row)
        if c == PAPER_ROLL
    }


def count_adjacent_rolls_set(rolls: Set[tuple[int, int]], i: int, j: int) -> int:
    """
    Count the number of adjacent rolls using the set approach.
    """
    return sum(
        (i + di, j + dj) in rolls
        for di, dj in DIRECTIONS
    )


def remove_all_accessible(rolls: Set[Tuple[int, int]]) -> int:
    """
    Remove all accessible rolls iteratively until none are left.
    
    Returns:
        Total number of rolls removed.
    """
    total = 0
    while True:
        accessible = {
            (i, j) for (i, j) in rolls
            if count_adjacent_rolls_set(rolls, i, j) < MAX_ADJACENT_ROLLS
        }
        if not accessible:
            break
        rolls -= accessible
        total += len(accessible)
    return total


def main() -> None:
    """
    Main function to solve the problem.

    Args:
        None.

    Returns:
        None.
    """
    input_data = read_input(Path(INPUT_FILE))
    
    # Part 1
    accessible_rolls = count_accessible_rolls(input_data)
    print(f"Part 1: {accessible_rolls}")
    
    # Part 2
    rolls = get_roll_positions(input_data)
    total_removed = remove_all_accessible(rolls)
    print(f"Part 2: {total_removed}")


if __name__ == '__main__':
    main()