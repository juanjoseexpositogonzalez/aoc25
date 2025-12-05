from pathlib import Path
from typing import List, Final, Tuple


TEST_INPUT: Final[str] = "test.txt"
INPUT: Final[str] = "input.txt"

def read_input(path: Path) -> List[str]:
    """Read the input file and return a list of strings.
    
    Args:
        path (Path): The path to the input file.

    Returns:
        List[str]: A list of strings.
    """
    with open(path, "r") as f:
        return f.readlines()


def extract_valid_ranges(lines: List[str]) -> List[str]:
    """Extract the valid ranges from the input file.
    
    Args:
        lines (List[str]): A list of strings.

    Returns:
        List[str]: A list of strings.
    """
    valid_ranges: List[str] = []
    for line in lines:
        if line == '\n':
            break
        valid_ranges.append(line.strip())
    return valid_ranges

def extract_ingredients_ids(lines: List[str]) -> List[str]:
    """Extract the ingredients ids from the input file.
    
    Args:
        lines (List[str]): A list of strings.
    """
    ingredients_ids: List[str] = []
    start_extracting: bool = False
    for line in lines:
        if line == '\n':
            start_extracting = True
            continue
        if start_extracting:
            ingredients_ids.append(line.strip())
    return ingredients_ids

def convert_str_range_to_int_range(range: str) -> Tuple[int, int]:
    """Convert a string range to a tuple of integers.
    Example:
        "1-3" -> (1, 3)
    
    Args:
        range (str): The string range to convert.

    Returns:
        A tuple of integers.
    """
    start, end = range.split('-')
    return (int(start), int(end))

def determine_if_ingredient_is_valid(ingredient: str, valid_ranges: List[Tuple[int, int]]) -> bool:
    """Determine if the ingredient is valid.
    
    Args:
        ingredient (str): The ingredient to determine if is valid.
        valid_ranges (List[Tuple[int, int]]): A list of valid ranges.

    Returns:
        True if the ingredient is valid, False otherwise.
    """
    ingredient_int = int(ingredient)
    for valid_range in valid_ranges:
        if ingredient_int >= valid_range[0] and ingredient_int <= valid_range[1]:
            return True
    return False

def determine_if_ingredients_are_valid(ingredients: List[str], valid_ranges: List[Tuple[int, int]]) -> List[bool]:
    """Determine if the ingredients are valid.
    
    Args:
        ingredients (List[str]): A list of ingredients.
        valid_ranges (List[Tuple[int, int]]): A list of valid ranges.
    """
    return [determine_if_ingredient_is_valid(ingredient, valid_ranges) for ingredient in ingredients]

def calculate_total_valid_ingredients(ingredients_are_valid: List[bool]) -> int:
    """Calculate the total valid ingredients.
    
    Args:
        ingredients_are_valid (List[bool]): A list of booleans.
    """
    return sum(ingredients_are_valid)

def main() -> None:
    """Main function."""
    lines = read_input(Path(INPUT))
    valid_ranges = extract_valid_ranges(lines)
    ingredients_ids = extract_ingredients_ids(lines)
    print(valid_ranges)
    print(ingredients_ids)
    valid_ranges_int = [convert_str_range_to_int_range(valid_range) for valid_range in valid_ranges]
    ingredients_are_valid = determine_if_ingredients_are_valid(ingredients_ids, valid_ranges_int)
    print(ingredients_are_valid)
    total_valid_ingredients = calculate_total_valid_ingredients(ingredients_are_valid)
    print(total_valid_ingredients)


if __name__ == "__main__":
    main()