import math
from pathlib import Path
from typing import List, Final

ADD: Final[str] = '+'
MULTIPLY: Final[str] = '*'
TEST_FILE: Final[str] = 'test.txt'
INPUT_FILE: Final[str] = 'input.txt'

def read_file(file_path: Path) -> List[str]:
    """
    Read the file and return a list of lines.

    Args:
        file_path: Path to the file to read.

    Returns:
        List of lines from the file.
    """
    with open(file_path, 'r') as file:
        lines = [line.strip().split(' ') for line in file.readlines()]
        lines = remove_empty_columns(lines)
        return lines

def remove_empty_columns(lines: List[List[str]]) -> List[List[str]]:
    """
    Remove empty columns from the list of lines.

    Args:
        lines: List of lines to remove empty columns from.

    Returns:
        List of lines with empty columns removed.
    """
    return [[item for item in line if item] for line in lines]

def convert_to_numbers(lines: List[str]) -> List[int]:
    """
    Convert the list of lines to a list of numbers.

    Args:
        lines: List of strings to convert to numbers.

    Returns:
        List of numbers converted.
    """
    return [int(item) if item.isdigit() else item for item in lines]

def transpose_lines(lines: List[List[int]]) -> List[List[int]]:
    """
    Transpose the list of lines.

    Args:
        lines: List of lines to transpose.

    Returns:
        Transposed list of lines.
    """
    return [[line[i] for line in lines] for i in range(len(lines[0]))] if lines else []

def calculate_column(column: List[ int | str]) -> int:
    """
    Calculate the result of the column.

    Args:
        column: List of numbers and operators to calculate.        
    Returns:
        Result of the column.
    """
    numbers = convert_to_numbers(column[:-1])    
    operator = column[-1]
    if operator == ADD:
        return int(math.fsum(numbers))
    elif operator == MULTIPLY:
        return int(math.prod(numbers))

def calculate_result(lines: List[List[int | str]]) -> int:
    """
    Calculate the result of the lines.

    Args:
        lines: List of lines to calculate the result of.
    Returns:
        Result of the lines.
    """
    result = 0
    for column in lines:
        result += calculate_column(column)
    return result    

def main():
    file_path = Path(TEST_FILE)
    lines = read_file(file_path)
    transposed_lines = transpose_lines(lines)
    print(lines)


    # First part of the puzzle
    print(f"First part of the puzzle: {calculate_result(transposed_lines)}")

    # Second part of the puzzle
    # print(f"Second part of the puzzle: {calculate_result(lines, operator)}")

if __name__ == '__main__':
    main()

    