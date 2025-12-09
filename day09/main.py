import bisect
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Final, List, Self, Tuple, Set


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

    def can_be_opposite_corner(self, p1: Point) -> bool:
        """
        Check if the two points can be opposite corners.
        """
        return self.top_left.x != p1.x and self.top_left.y != p1.y

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

# =============================================================================
# PASO 1: Generar líneas verdes entre puntos rojos consecutivos
# =============================================================================

def line_between(p1: Point, p2: Point) -> Set[Tuple[int, int]]:
    """
    Genera todos los puntos en la línea entre p1 y p2 (INCLUYENDO extremos).
    
    Los puntos consecutivos siempre comparten X o Y (línea recta).
    
    Ejemplo: (2,3) a (7,3) genera {(2,3), (3,3), (4,3), (5,3), (6,3), (7,3)}
    """
    points: Set[Tuple[int, int]] = set()
    
    if p1.x == p2.x:  # Línea vertical
        min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)
        for y in range(min_y, max_y + 1):
            points.add((p1.x, y))
    else:  # Línea horizontal (p1.y == p2.y)
        min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
        for x in range(min_x, max_x + 1):
            points.add((x, p1.y))
    
    return points


def get_polygon_border(red_points: List[Point]) -> Set[Tuple[int, int]]:
    """
    Genera todo el borde del polígono (líneas verdes + puntos rojos).
    
    El polígono conecta: punto[0] → punto[1] → ... → punto[n-1] → punto[0]
    """
    border: Set[Tuple[int, int]] = set()
    n = len(red_points)
    
    for i in range(n):
        p1 = red_points[i]
        p2 = red_points[(i + 1) % n]  # Wrap around al primero
        border.update(line_between(p1, p2))
    
    return border


# =============================================================================
# PASO 2: Encontrar el interior del polígono (Flood Fill desde exterior)
# =============================================================================

def get_bounds(points: List[Point]) -> Tuple[int, int, int, int]:
    """Devuelve (min_x, max_x, min_y, max_y) con margen de 1."""
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    return min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1


def flood_fill_exterior(border: Set[Tuple[int, int]], 
                         bounds: Tuple[int, int, int, int]) -> Set[Tuple[int, int]]:
    """
    Flood fill desde las esquinas para encontrar todas las baldosas EXTERIORES.
    
    Estrategia:
    1. Empezamos desde una esquina (que sabemos está fuera)
    2. Expandimos a todos los vecinos que no sean borde
    3. Todo lo que NO alcanzamos está dentro del polígono
    """
    min_x, max_x, min_y, max_y = bounds
    
    # BFS desde la esquina superior izquierda
    exterior: Set[Tuple[int, int]] = set()
    queue = [(min_x, min_y)]
    
    while queue:
        x, y = queue.pop()
        
        # Fuera de límites
        if x < min_x or x > max_x or y < min_y or y > max_y:
            continue
        
        # Ya visitado o es borde
        if (x, y) in exterior or (x, y) in border:
            continue
        
        exterior.add((x, y))
        
        # Expandir a vecinos (4 direcciones)
        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))
    
    return exterior


def get_interior(border: Set[Tuple[int, int]], 
                 bounds: Tuple[int, int, int, int]) -> Set[Tuple[int, int]]:
    """
    Encuentra todas las baldosas INTERIORES del polígono.
    
    Interior = Todo lo que está dentro de bounds - borde - exterior
    """
    min_x, max_x, min_y, max_y = bounds
    exterior = flood_fill_exterior(border, bounds)
    
    interior: Set[Tuple[int, int]] = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in border and (x, y) not in exterior:
                interior.add((x, y))
    
    return interior


# =============================================================================
# PASO 3: Verificar si un rectángulo es válido
# =============================================================================

def is_valid_rectangle(p1: Point, p2: Point, valid_tiles: Set[Tuple[int, int]]) -> bool:
    """
    Verifica que TODAS las baldosas del rectángulo estén en valid_tiles.
    
    El rectángulo va de (min_x, min_y) a (max_x, max_y) inclusive.
    """
    min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
    min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)
    
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in valid_tiles:
                return False
    
    return True


def rectangle_area(p1: Point, p2: Point) -> int:
    """Calcula el área del rectángulo (inclusive)."""
    return (abs(p2.x - p1.x) + 1) * (abs(p2.y - p1.y) + 1)


# =============================================================================
# PASO Adicional: Verificar si un rectángulo es válido de forma más eficiente
# =============================================================================

def get_exterior_sorted(border: Set[Tuple[int, int]], 
                        bounds: Tuple[int, int, int, int]) -> List[Tuple[int, int]]:
    """
    Devuelve las baldosas exteriores ordenadas por X (para búsqueda binaria).
    """
    exterior = flood_fill_exterior(border, bounds)
    return sorted(exterior)


def is_valid_rectangle_fast(p1: Point, p2: Point, 
                            exterior_sorted: List[Tuple[int, int]]) -> bool:
    """
    Verifica que NO haya baldosas exteriores dentro del rectángulo.
    Usa búsqueda binaria para eficiencia.
    """
    min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
    min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)
    
    # Encontrar primer elemento con x >= min_x
    left = bisect.bisect_left(exterior_sorted, (min_x, -1))
    
    # Verificar solo baldosas en el rango X
    for i in range(left, len(exterior_sorted)):
        x, y = exterior_sorted[i]
        if x > max_x:
            break  # Ya pasamos el rango X
        if min_y <= y <= max_y:
            return False  # ¡Baldosa inválida dentro!
    
    return True


def precompute_interior_ranges(border: Set[Tuple[int, int]], 
                                bounds: Tuple[int, int, int, int]) -> dict[int, List[Tuple[int, int]]]:
    """
    Para cada Y, calcula los rangos [x_start, x_end] que están dentro del polígono.
    """
    min_x, max_x, min_y, max_y = bounds
    
    border_by_y = defaultdict(list)
    for x, y in border:
        border_by_y[y].append(x)
    
    interior_ranges = {}
    
    for y in range(min_y, max_y + 1):
        if y not in border_by_y:
            continue
        
        xs = sorted(border_by_y[y])
        ranges = []
        
        # Los puntos del borde vienen en pares: entrada/salida
        # Entre cada par está el interior
        for i in range(0, len(xs) - 1, 2):
            if i + 1 < len(xs):
                ranges.append((xs[i], xs[i + 1]))
        
        interior_ranges[y] = ranges
    
    return interior_ranges


def is_range_inside(x_min: int, x_max: int, y: int, 
                    interior_ranges: dict[int, List[Tuple[int, int]]]) -> bool:
    """
    Verifica si el rango [x_min, x_max] está completamente dentro para una Y dada.
    """
    if y not in interior_ranges:
        return False
    
    for r_min, r_max in interior_ranges[y]:
        if r_min <= x_min and x_max <= r_max:
            return True
    
    return False


def part_two_fast(file: str) -> None:
    file_path = Path(file)
    lines = read_file(file_path)
    red_points = parse_input(lines)
    
    border = get_polygon_border(red_points)
    bounds = get_bounds(red_points)
    
    # Precalcular rangos interiores
    interior_ranges = precompute_interior_ranges(border, bounds)
    
    def is_rect_valid(p1: Point, p2: Point) -> bool:
        min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
        min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)
        
        # Verificar que CADA fila del rectángulo esté dentro
        for y in range(min_y, max_y + 1):
            if not is_range_inside(min_x, max_x, y, interior_ranges):
                return False
        return True
    
    # Ordenar pares por área potencial (mayor primero) para early exit
    pairs = [
        (p1, p2) for p1, p2 in combinations(red_points, 2)
        if p1.can_be_opposite_corners(p2)
    ]
    pairs.sort(key=lambda p: rectangle_area(p[0], p[1]), reverse=True)
    
    max_area = 0
    for p1, p2 in pairs:
        area = rectangle_area(p1, p2)
        
        # Early exit: si el área potencial es menor que el máximo actual, paramos
        if area <= max_area:
            break
        
        if is_rect_valid(p1, p2):
            max_area = area
            break  # Ya tenemos el máximo posible
    
    print(f"Área máxima: {max_area}")

# =============================================================================
# SOLUCIÓN PRINCIPAL
# =============================================================================

def part_two(file: str) -> None:
    file_path = Path(file)
    lines = read_file(file_path)
    red_points = parse_input(lines)
    
    border = get_polygon_border(red_points)
    
    # Índices para búsqueda rápida
    border_by_x: defaultdict[int, List[int]] = defaultdict(list)  # x -> sorted list of y
    border_by_y: defaultdict[int, List[int]] = defaultdict(list)  # y -> sorted list of x
    
    for x, y in border:
        border_by_x[x].append(y)
        border_by_y[y].append(x)
    
    for x in border_by_x:
        border_by_x[x].sort()
    for y in border_by_y:
        border_by_y[y].sort()
    
    def is_inside(x: int, y: int) -> bool:
        """Ray casting: cuenta cruces hacia la izquierda."""
        if (x, y) in border:
            return True
        if y not in border_by_y:
            return False
        crossings = bisect.bisect_left(border_by_y[y], x)
        return crossings % 2 == 1
    
    def is_rect_valid(p1: Point, p2: Point) -> bool:
        """Verifica solo los 4 bordes del rectángulo."""
        min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
        min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)
        
        # Verificar bordes horizontales
        for x in range(min_x, max_x + 1):
            if not is_inside(x, min_y) or not is_inside(x, max_y):
                return False
        
        # Verificar bordes verticales (sin esquinas, ya verificadas)
        for y in range(min_y + 1, max_y):
            if not is_inside(min_x, y) or not is_inside(max_x, y):
                return False
        
        return True
    
    max_area = 0
    for p1, p2 in combinations(red_points, 2):
        if p1.can_be_opposite_corners(p2) and is_rect_valid(p1, p2):
            area = rectangle_area(p1, p2)
            max_area = max(max_area, area)
    
    print(f"Área máxima: {max_area}")

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


    part_two_fast(INPUT_FILE)

if __name__ == "__main__":
    main()