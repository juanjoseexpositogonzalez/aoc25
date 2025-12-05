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

def calculate_total_valid_ingredients_in_ranges(valid_ranges: List[Tuple[int, int]]) -> int:
    """Calculate the total valid ingredients in the ranges.
    
    Args:
        valid_ranges (List[Tuple[int, int]]): A list of valid ranges.
    """    
    # 1. Order the ranges by the start of the range
    valid_ranges.sort(key=lambda x: x[0])    
    # 2. Initialize first range
    start, end = valid_ranges[0]
    # 3. Iterate through the ranges, storing new ranges
    new_ranges: List[Tuple[int, int]] = []
    for valid_range in valid_ranges[1:]:        
        new_start, new_end = valid_range
        if new_start <= end:
            end = max(end, new_end)            
        else:
            new_ranges.append((start, end))
            start, end = new_start, new_end
    # 4. Don't forget to add the last range
    new_ranges.append((start, end))
    # 5. Calculate the total valid ingredients in the new ranges
  
    return sum(end - start + 1 for start, end in new_ranges)
        

def main() -> None:
    """Main function."""
    lines = read_input(Path(INPUT))
    valid_ranges = extract_valid_ranges(lines)
    ingredients_ids = extract_ingredients_ids(lines)
    valid_ranges_int = [convert_str_range_to_int_range(valid_range) for valid_range in valid_ranges]    
    ingredients_are_valid = determine_if_ingredients_are_valid(ingredients_ids, valid_ranges_int)
    # Part 1
    total_valid_ingredients = calculate_total_valid_ingredients(ingredients_are_valid)
    print(f"Part 1: {total_valid_ingredients}")
    # Part 2
    total_valid_ingredients_in_ranges = calculate_total_valid_ingredients_in_ranges(valid_ranges_int)
    print(f"Part 2: {total_valid_ingredients_in_ranges}")


if __name__ == "__main__":
    main()