from pathlib import Path
from typing import Dict, List, Final, Tuple

START_OF_RANGE: Final[str] = '-'
SEPARATOR: Final[str] = ','
def read_input(file_path: Path) -> List[str]:
    """
    Read the input data from the file.

    Args:
        file_path: The path to the file to read.

    Returns:
        The input data as a list of strings.
    """
    with open(file_path, 'r') as file:
        return file.read().split(SEPARATOR)

def get_ranges(input_data: List[str]) -> List[Tuple[int, int]]:
    """
    Get the range of the input data.   

    Args:
        input_data: The input data to get the ranges of.

    Returns:
        The ranges of the input data.
    """
    return [(int(start), int(end)) for start, end in [data.split(START_OF_RANGE) for data in input_data]]

def is_id_invalid(id: int) -> bool:
    """
    Check if the id is invalid.

    Args:
        id: The id to check if it is invalid.

    Returns:
        True if the id is invalid, False otherwise.
    """
    # 1. Convert the id to a string
    id_str = str(id)
    # 2. Calculate the length of the id
    length = len(id_str)
    if id_str[:length // 2] == id_str[length // 2:]:
        return True
    return False

def process_ids(input: List[Tuple[int, int]]) -> Dict[str, List[int]]:
    """
    Process the id.

    Args:
        input: The input to process.

    Returns:
        A dictionary with the key as the range and the value as the invalid ids.
    """
    results: Dict[str, List[int]] = {}
    
    for start, end in input:
        for candidate in range(start, end + 1):
            key = f"{start}-{end}"
            if is_id_invalid(candidate):
                if key not in results:
                    results[key] = []
                results[key].append(candidate)        
    return results

def add_invalid_ids(results: Dict[str, List[int]]) -> int:
    """
    Add the invalid ids to the results.

    Args:
        results: The results to add the invalid ids to.

    Returns:
        The total number of invalid ids.
    """
    return sum(sum(invalid_ids) for invalid_ids in results.values())

def main() -> None:
    input_data = read_input(Path('input.txt'))
    ranges = get_ranges(input_data)   
    results = process_ids(ranges)    
    total_invalid_ids = add_invalid_ids(results)
    print(total_invalid_ids)

if __name__ == '__main__':
    main()