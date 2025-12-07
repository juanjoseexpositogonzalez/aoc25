from pathlib import Path
from typing import Final, List, Tuple, Set

TEST_FILE: Final[str] = 'test.txt'
INPUT_FILE: Final[str] = 'input.txt'

START: Final[str] = 'S'
DEFLECTOR: Final[str] = '^'

def read_file(file_path: Path) -> List[str]:
    """
    Read the file and return a list of lines.

    Args:
        file_path: The path to the file to read.

    Returns:
        A list of lines from the file.
    """
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def parse_input(lines: List[str]) -> Tuple[Tuple[int, int], Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Parse the input and return the start position, splitter positions, and grid size.
    """
    start: Tuple[int, int] = (0, 0)    
    size: Tuple[int, int] = (len(lines), len(lines[0]))
    splitters: Set[Tuple[int, int]] = set()

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == START:
                start = (row, col)
            elif char == DEFLECTOR:
                splitters.add((row, col))
    
    return start, splitters, size

def simulate_beams(start: Tuple[int, int], splitters: Set[Tuple[int, int]], size: Tuple[int, int]) -> int:
    """
    Simulate the beams and return the number of splits.
    """
    active_beams = {start}
    total_splits = 0
    rows, cols = size
    
    while active_beams:
        new_beams: Set[Tuple[int, int]] = set()
        for row, col in active_beams:
            new_row = row + 1  # Solo hacia abajo
            
            # Sale del grid → desaparece
            if new_row >= rows:
                continue
            
            # Encuentra splitter → se divide
            if (new_row, col) in splitters:
                total_splits += 1
                if col - 1 >= 0:
                    new_beams.add((new_row, col - 1))
                if col + 1 < cols:
                    new_beams.add((new_row, col + 1))
            else:
                # Espacio vacío → continúa
                new_beams.add((new_row, col))
        
        active_beams = new_beams
    
    return total_splits


def first_part() -> None:
    """
    First part of the puzzle.

    Args:
        None.

    Returns:
        None.
    """

    file_path = Path(TEST_FILE)
    lines = read_file(file_path)
    start, splitters, size = parse_input(lines)
    total_splits = simulate_beams(start, splitters, size)
    print(f"Test file - First part: {total_splits}")

    file_path = Path(INPUT_FILE)
    lines = read_file(file_path)
    start, splitters, size = parse_input(lines)
    total_splits = simulate_beams(start, splitters, size)
    print(f"Input file - First part: {total_splits}")


def second_part() -> None:
    """
    Second part of the puzzle.

    Args:
        None.

    Returns:
        None.
    """
    ...

def main() -> None:
    """
    Main function.

    Args:
        None.

    Returns:
        None.
    """
    first_part()
    second_part()

if __name__ == '__main__':
    main()