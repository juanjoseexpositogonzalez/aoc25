from pathlib import Path
from typing import Final, List, Dict, Set, Tuple

TEST_INPUT: Final[str] = "test.txt"
REAL_INPUT: Final[str] = "input.txt"


def read_input(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def parse_shape(lines: List[str]) -> Set[Tuple[int, int]]:
    shape = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                shape.add((row, col))
    return shape


def normalize_shape(shape: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    if not shape:
        return shape
    min_row = min(r for r, c in shape)
    min_col = min(c for r, c in shape)
    return {(r - min_row, c - min_col) for r, c in shape}


def rotate_90(shape: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    return normalize_shape({(c, -r) for r, c in shape})


def flip_horizontal(shape: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    return normalize_shape({(r, -c) for r, c in shape})


def get_all_orientations(shape: Set[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    orientations = set()
    current = shape
    
    for _ in range(4):
        normalized = normalize_shape(current)
        orientations.add(frozenset(normalized))
        
        flipped = flip_horizontal(current)
        orientations.add(frozenset(normalize_shape(flipped)))
        
        current = rotate_90(current)
    
    return [set(o) for o in orientations]


def parse_input(content: str) -> Tuple[Dict[int, Set[Tuple[int, int]]], List[Tuple[int, int, List[int]]]]:
    parts = content.strip().split('\n\n')
    
    region_start = 0
    for i, part in enumerate(parts):
        first_line = part.strip().split('\n')[0]
        if 'x' in first_line:
            region_start = i
            break
    
    shapes = {}
    for part in parts[:region_start]:
        lines = part.strip().split('\n')
        idx = int(lines[0].rstrip(':'))
        shape_lines = lines[1:]
        shapes[idx] = parse_shape(shape_lines)
    
    regions = []
    for part in parts[region_start:]:
        for line in part.strip().split('\n'):
            size_part, counts_part = line.split(': ')
            width, height = map(int, size_part.split('x'))
            counts = list(map(int, counts_part.split()))
            regions.append((width, height, counts))
    
    return shapes, regions


def can_place(grid: Set[Tuple[int, int]], shape: Set[Tuple[int, int]], 
              row: int, col: int, width: int, height: int) -> bool:
    for r, c in shape:
        nr, nc = row + r, col + c
        if nr < 0 or nr >= height or nc < 0 or nc >= width:
            return False
        if (nr, nc) in grid:
            return False
    return True


def place(grid: Set[Tuple[int, int]], shape: Set[Tuple[int, int]], 
          row: int, col: int) -> Set[Tuple[int, int]]:
    new_grid = grid.copy()
    for r, c in shape:
        new_grid.add((row + r, col + c))
    return new_grid


def solve(grid: Set[Tuple[int, int]], pieces: List[int], 
          width: int, height: int, 
          all_orientations: Dict[int, List[Set[Tuple[int, int]]]]) -> bool:
    """Backtracking: intenta colocar cada pieza en cualquier posición válida."""
    if not pieces:
        return True
    
    shape_idx = pieces[0]
    remaining = pieces[1:]
    
    # Probar cada orientación de la pieza
    for orientation in all_orientations[shape_idx]:
        # Probar cada posición
        for row in range(height):
            for col in range(width):
                if can_place(grid, orientation, row, col, width, height):
                    new_grid = place(grid, orientation, row, col)
                    if solve(new_grid, remaining, width, height, all_orientations):
                        return True
    
    return False


def can_fit_all(shapes: Dict[int, Set[Tuple[int, int]]], 
                width: int, height: int, counts: List[int]) -> bool:
    # Crear lista de piezas a colocar
    pieces = []
    for shape_idx, count in enumerate(counts):
        for _ in range(count):
            pieces.append(shape_idx)
    
    if not pieces:
        return True
    
    # Verificación rápida: espacio suficiente?
    total_cells = sum(len(shapes[i]) * counts[i] for i in range(len(counts)))
    if total_cells > width * height:
        return False
    
    # Precalcular orientaciones
    all_orientations = {i: get_all_orientations(shapes[i]) for i in range(len(counts))}
    
    return solve(set(), pieces, width, height, all_orientations)


def main() -> None:
    content = read_input(Path(TEST_INPUT))
    shapes, regions = parse_input(content)
    
    count = 0
    for i, (width, height, counts) in enumerate(regions):
        if can_fit_all(shapes, width, height, counts):
            count += 1
            print(f"Region {i}: {width}x{height} ✓")
        else:
            print(f"Region {i}: {width}x{height} ✗")
    
    print(f"\nTotal: {count}")


if __name__ == "__main__":
    main()