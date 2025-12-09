from dataclasses import dataclass
from itertools import combinations
import math
from pathlib import Path
from typing import Final, List, Self

TEST_FILE: Final[str] = 'test.txt'
INPUT_FILE: Final[str] = 'input.txt'
MAX_NUM_JUNCTIONS: Final[int] = 1000

@dataclass
class Point:
    x: int
    y: int
    z: int


    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def euclidean_distance(self, other: Self) -> float:
        """
        Calculate the Euclidean distance between two points.

        Args:
            other: The other point.

        Returns:
            The Euclidean distance between the two points.
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def manhattan_distance(self, other: Self) -> int:
        """
        Calculate the Manhattan distance between two points.

        Args:
            other: The other point.

        Returns:
            The Manhattan distance between the two points.
        """
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x: int) -> int:
        """Encuentra la raíz del grupo de x."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """Une x e y. Devuelve True si estaban en grupos distintos."""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True
    
    def get_sizes(self) -> List[int]:
        """Devuelve los tamaños de todos los grupos."""
        return [self.size[i] for i in range(len(self.parent)) if self.parent[i] == i]


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
    Parse the input and return a list of points.

    Args:
    """
    points: List[Point] = []
    for line in lines:
        x, y, z = line.split(',')
        points.append(Point(int(x), int(y), int(z)))
    return points


def generate_pairs_by_distance(points: List[Point]) -> List[tuple[float, int, int]]:
    """
    Genera todos los pares de puntos ordenados por distancia.
    
    Returns:
        Lista de (distancia, índice_i, índice_j)
    """
    pairs: List[tuple[float, int, int]] = []
    for i, j in combinations(range(len(points)), 2):
        dist = points[i].euclidean_distance(points[j])
        pairs.append((dist, i, j))
    pairs.sort(key=lambda x: x[0])
    return pairs

def part_two(file: str) -> None:
    """
    Part two of the puzzle.

    Args:
        None.

    Returns:
        None.
    """
    file_path = Path(file)
    lines = read_file(file_path)
    points = parse_input(lines)
    pairs = generate_pairs_by_distance(points)
    
    uf = UnionFind(len(points))
    num_groups = len(points)  # Empezamos con n grupos
    
    for _, i, j in pairs:
        if uf.union(i, j):
            num_groups -= 1
            if num_groups == 1:
                # ¡Esta fue la última conexión!
                result = points[i].x * points[j].x
                print(f"Última conexión: {points[i]} y {points[j]}")
                print(f"Resultado: {result}")
                break

def main() -> None:
    """
    Main function to solve the problem.
    """
    file_path = Path(TEST_FILE)
    lines = read_file(file_path)
    points = parse_input(lines)
    pairs = generate_pairs_by_distance(points)
    
    uf = UnionFind(len(points))
    for dist, i, j in pairs[:MAX_NUM_JUNCTIONS]:
        uf.union(i, j)
        print(f"Union de {i} y {j} con distancia {dist}")    
    sizes = sorted(uf.get_sizes(), reverse=True)    
    result = math.prod(sizes[:3])
    print(f"Test file - First part: {result}")

    print(f"Input file - Second part: {part_two(TEST_FILE)}")


if __name__ == "__main__":
    main()