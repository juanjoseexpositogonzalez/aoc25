from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Final, List, Self


TEST_FILE: Final[str] = 'test.txt'
INPUT_FILE: Final[str] = 'input.txt'

@dataclass
class Point:
    x: int
    y: int

    def can_be_opposite_corners(self, p1: Self) -> bool:
        """
        Check if the two points can be opposite corners.
        
        Args:
            p1: The first point.
            p2: The second point.

        Returns:
            True if the two points can be opposite corners, False otherwise.
        """
        return self.x != p1.x and self.y != p1.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

@dataclass
class Rectangle:
    top_left: Point
    bottom_right: Point

    def __str__(self) -> str:
        return f"Rectangle(top_left={self.top_left}, bottom_right={self.bottom_right})"

    def __repr__(self) -> str:
        return f"Rectangle(top_left={self.top_left}, bottom_right={self.bottom_right})"

    def contains(self, point: Point) -> bool:
        """
        Check if the point is inside the rectangle.
        
        Args:
            point: The point to check.

        Returns:
            True if the point is inside the rectangle, False otherwise.
        """
        return self.top_left.x <= point.x <= self.bottom_right.x and self.top_left.y <= point.y <= self.bottom_right.y  

    @property
    def area(self) -> int:
        """
        Calculate the area of the rectangle.

        Returns:
            The area of the rectangle.
        """
        return abs(self.bottom_right.x - self.top_left.x) * abs (self.bottom_right.y - self.top_left.y)

    @staticmethod
    def from_corners(p1: Point, p2: Point) -> Rectangle:
        """
        Create a rectangle from two points.             
        

        Args:
            p1: The first point.
            p2: The second point.

        Returns:
            A rectangle.
        """
        return Rectangle(p1, p2)

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


def parse_input(lines: List[str]) -> List[Point]:
    """
    Parse the input and return a list of tuples.

    Args:
        lines: A list of lines from the file.

    Returns:
        A list of tuples.
    """
    points: List[Point] = []
    for line in lines:
        x, y = line.split(',')
        points.append(Point(int(x), int(y)))
    return points

def part_one(file: str) -> int:
    file_path = Path(file)
    lines = read_file(file_path)
    points = parse_input(lines)
    
    max_area = 0
    for p1, p2 in combinations(points, 2):
        if p1.can_be_opposite_corners(p2):
            area = (abs(p2.x - p1.x) + 1) * (abs(p2.y - p1.y) + 1 )
            max_area = max(max_area, area)   
    
    return max_area


def main() -> None:
    max_area = part_one(INPUT_FILE)
    print(f"Test file - First part: {max_area}")
    # part_one(INPUT_FILE)

if __name__ == "__main__":
    main()