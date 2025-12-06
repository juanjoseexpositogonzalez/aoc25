import math
from pathlib import Path
from typing import List, Final

ADD: Final[str] = '+'
MULTIPLY: Final[str] = '*'
TEST_FILE: Final[str] = 'test.txt'
INPUT_FILE: Final[str] = 'input.txt'

def read_file(file_path: Path, remove_empty_strings: bool = True, strip_lines: bool = True) -> List[str]:
    """
    Read the file and return a list of lines.

    Args:
        file_path: Path to the file to read.
        remove_empty_strings: Whether to remove empty strings from the list of lines.
        strip_lines: Whether to strip the lines.
    Returns:
        List of lines from the file.
    """
    with open(file_path, 'r') as file:
        if strip_lines and remove_empty_strings:
            lines = [line.strip().split(' ') for line in file.readlines()]
            lines = remove_empty_columns(lines)
        else:
            lines = file.read().splitlines()
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

def transpose_strings(strings: List[str]) -> List[List[str]]:
    """
    Transpose the list of strings by columns.

    Args:
        strings: List of strings to transpose.
    Returns:
        Transposed list of strings.
    """
    return [list(col) for col in zip(*strings)]

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

def is_separator(column: List[str]) -> bool:
    """
    Check if the column is a separator.

    Args:
        column: List of strings to check if it is a separator.
    Returns:
        True if the column is a separator, False otherwise.
    """
    return all(c == ' ' for c in column)

def group_problems(columns: List[List[str]]) -> List[List[List[str]]]:
    """
    Group the columns into problems.

    Args:
        columns: List of columns to group into problems.
    Returns:
        List of problems, where each problem is a list of columns.
    """
    problems = []
    current_problem = []
    for column in columns:
        if is_separator(column):
            problems.append(current_problem)
            current_problem = []
        else:
            current_problem.append(column)
    if current_problem:
        problems.append(current_problem)
    return problems

def extract_numbers_and_operator(problem: List[List[str]]) -> Tuple[List[int], str]:
    """
    Extract numbers and operator from a problem.
    
    Each column forms a number (digits top to bottom).
    The operator is in the last row.
    """
    numbers = []
    operator = None
    for column in problem:
        # Join all digits in the column to form a number
        digits = ''.join(c for c in column if c.isdigit())
        if digits:
            numbers.append(int(digits))
        
        # Check if operator is in this column (last row)
        if column[-1] in [ADD, MULTIPLY]:
            operator = column[-1]
    
    return numbers, operator  

def calculate_problem(problem: Tuple[List[int], str]) -> int:
    """
    Calculate the result of a problem.

    Args:
        problem: Tuple of numbers and operator to calculate the result of.
    Returns:
        Result of the problem.
    """
    numbers, operator = problem    
    if operator == ADD:
        return int(math.fsum(numbers))
    elif operator == MULTIPLY:
        return int(math.prod(numbers))


def main():
    # First part of the puzzle
    file_path = Path(INPUT_FILE)
    lines = read_file(file_path, remove_empty_strings=True, strip_lines=True)
    transposed_lines = transpose_lines(lines)
    print(f"First part of the puzzle: {calculate_result(transposed_lines)}")

    # Second part of the puzzle
    lines = read_file(file_path, remove_empty_strings=False, strip_lines=False)    
    transposed_lines = transpose_strings(lines)    
    problems = group_problems(transposed_lines)    
    numbers_and_operators = [extract_numbers_and_operator(problem) for problem in problems]
    results = int(math.fsum([calculate_problem(problem) for problem in numbers_and_operators]))
    print(f"Second part of the puzzle: {results}")

if __name__ == '__main__':
    main()

    