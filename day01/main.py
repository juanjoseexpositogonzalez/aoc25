from pathlib import Path
from typing import Final, List, Tuple
from itertools import pairwise


LEFT: Final[str] = '-'
RIGHT: Final[str] = '+'
MODULUS: Final[int] = 100
INITIAL_POSITION: Final[int] = 50

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
    
def get_direction_and_magnitude(input_data: List[str]) -> List[Tuple[str, int]]:
    """
    Get the direction and magnitude of the input data.

    Args:
        input_data: The input data to get the direction and magnitude of.

    Returns:
        The direction and magnitude of the input data.
    """
    return [(line[0], int(line[1:])) for line in input_data if line.strip()]

def normalize_direction(direction: int) -> Tuple[int,int]:
    """
    Normalize the direction to a positive direction.

    Args:
        direction: The direction to normalize.

    Returns:
        The normalized direction.
    """

    return  (direction // MODULUS), (direction % MODULUS)

def build_direction_and_magnitude(indications: List[Tuple[str,int]]) -> Tuple[int,List[int]]:
    """
    Build the direction and magnitude of the indications.

    Args:
        indications: The indications to build the direction and magnitude of.

    Returns:
        The total number of cycles and the changes in position.
    """
    normalized_directions: List[Tuple[int,int]] = [normalize_direction(indication[1]) for indication in indications]
    cycles, positions = zip(*normalized_directions)
    new_indications = [position  for position in positions]
    for i, (indication, _) in enumerate(indications):        
        if indication == 'L':
            new_indications[i] = -1 * new_indications[i]
    return sum(cycles), new_indications
    
def build_trajectory(start_position: int, changes_in_position: List[int]) -> Tuple[List[int], int, int]:
    """
    Build the trajectory of the changes in position.
    """
    old_position = start_position
    trajectory: List[int] = [start_position]
    extra_zero_crossings: int = 0
    zero_stops: int = 0
    for change in changes_in_position:
        new_position = old_position + change
        if new_position == 0 or new_position == MODULUS:
            zero_stops += 1
        if new_position * old_position < 0 or new_position > MODULUS and old_position < MODULUS:
            extra_zero_crossings += 1
        trajectory.append(new_position % MODULUS)
        old_position = new_position % MODULUS
    return trajectory, extra_zero_crossings, zero_stops

def print_trajectory(trajectory: List[int]) -> None:
    """
    Print the trajectory of the changes in position.
    """
    for i, (prev_pos, current_pos) in enumerate(pairwise(trajectory)):
        print(f"Paso {i +1:02d}: {prev_pos:02d} -> {current_pos:02d}")
        


def main() -> None:
    input_data = read_input(Path('input.txt'))    
    direction_and_magnitude = get_direction_and_magnitude(input_data)
    total_cycles, changes_in_position = build_direction_and_magnitude(direction_and_magnitude)
    trajectory, extra_zero_crossings, zero_stops = build_trajectory(INITIAL_POSITION, changes_in_position)
    password = total_cycles + extra_zero_crossings + zero_stops
    print_trajectory(trajectory)
    print(f"Extra zero crossings: {extra_zero_crossings}")
    print(f"Zero stops: {zero_stops}")
    print(f"Total cycles: {total_cycles}")
    print(f"Password: {password}")

if __name__ == '__main__':
    main()