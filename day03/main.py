from pathlib import Path
from typing import List, Final

NUM_DIGITS: Final[int] = 12


def read_input(file_path: Path) -> List[str]:
    """
    Read the input data from the file.

    Args:
        file_path: The path to the file to read.

    Returns:
        The input data as a list of strings.
    """
    with open(file_path, 'r') as file:
        return file.readlines()

def get_digits(input: str) -> List[int]:
    """
    Get the digits from the input.

    Args:
        input: The input to get the digits from.

    Returns:
        The digits from the input.
    """    
    return [int(digit) for digit in input.split('\n')[0]]

def determine_max_number(input: List[int], num_digits: int = 2) -> int:
    """
    Determine the max number of num_digits from the input.

    Args:
        input: The input to determine the max number from.
        num_digits: The number of digits to determine the max number from.

    Returns:
        The max number with num_digits digits from the input.
    """
    # idx = max(range(len(input)-1), key=lambda i: input[i])
    # first_digit = input[idx]
    # idx = max(range(idx+1, len(input)), key=lambda i: input[i])
    # second_digit = input[idx]
    # return first_digit * 10 + second_digit
    idx = -1
    digits: List[int] = []
    n = len(input)
    for i in range(1, num_digits + 1):
        idx = max(range(idx + 1, n - num_digits + i), key=lambda j: input[j])
        digits.append(input[idx])        
    return int(''.join(map(str, digits)))

def get_max_voltage(input: List[str], num_digits: int = 2) -> int:
    """
    Get the max voltage from the input.

    Args:
        input: The input to get the max voltage from.
        num_digits: The number of digits to determine the max voltage from.
    Returns:
        The max voltage from the input.
    """
    total_voltage = 0
    for line in input:
        digits = get_digits(line)
        max_number = determine_max_number(digits, num_digits)
        total_voltage += max_number
    return total_voltage    


def main() -> None:
    input_data = read_input(Path('input.txt'))
    max_voltage = get_max_voltage(input_data, NUM_DIGITS)
    print(max_voltage)


if __name__ == '__main__':
    main()