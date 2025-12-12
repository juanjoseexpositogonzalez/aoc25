"""
Solución para el problema del Day 12: Christmas Tree Farm
Problema de packing 2D con rotaciones y reflejos de piezas
"""

from pathlib import Path
from typing import List, Tuple, Final, Optional

TEST_INPUT: Final[str] = "test.txt"
INPUT_FILE: Final[str] = "input.txt"

# Alias de tipos para mayor legibilidad
Shape = List[List[bool]]
Cells = List[Tuple[int, int]]
Size = Tuple[int, int]
# Cada variación se representa como (celdas, tamaño, número_de_celdas)
Variation = Tuple[Cells, Size, int]
# Piezas: lista de variaciones y el conteo restante de esa pieza
Piece = Tuple[List[Variation], int]


def trim_shape(shape: Shape) -> Shape:
    """
    Recorta filas y columnas vacías alrededor de la forma para reducir el
    espacio de búsqueda. Devuelve una nueva forma recortada.
    """
    if not shape:
        return []

    rows = len(shape)
    cols = len(shape[0])

    top = next((r for r in range(rows) if any(shape[r])), 0)
    bottom = next((r for r in range(rows - 1, -1, -1) if any(shape[r])), rows - 1)

    left = 0
    right = cols - 1
    for c in range(cols):
        if any(shape[r][c] for r in range(rows)):
            left = c
            break
    for c in range(cols - 1, -1, -1):
        if any(shape[r][c] for r in range(rows)):
            right = c
            break

    trimmed: Shape = []
    for r in range(top, bottom + 1):
        trimmed.append(shape[r][left : right + 1])
    return trimmed


def parse_shapes(input_lines: List[str]) -> List[Shape]:
    """
    Parsea las formas de los regalos del input.
    Retorna una lista de formas, donde cada forma es una matriz de booleanos.
    True representa '#' (parte de la forma) y False representa '.' (vacío).
    """
    shapes = []
    i = 0
    
    while i < len(input_lines):
        line = input_lines[i].strip()
        # Detectar si es una forma (formato: "número:") o una región (formato: "númeroxnúmero:")
        if line and ':' in line and 'x' not in line:
            # Es una forma (ej: "0:")
            shape = []
            i += 1
            # Leer las filas de la forma hasta encontrar una línea vacía o la siguiente forma/región
            while i < len(input_lines):
                next_line = input_lines[i].strip()
                # Si encontramos una línea vacía o una nueva forma/región, terminamos
                if not next_line or (':' in next_line and 'x' not in next_line) or ('x' in next_line and ':' in next_line):
                    break
                # Procesar la fila de la forma
                row = []
                for char in next_line:
                    if char == '#':
                        row.append(True)
                    elif char == '.':
                        row.append(False)
                if row:  # Solo agregar filas no vacías
                    shape.append(row)
                i += 1
            if shape:
                shapes.append(trim_shape(shape))
        else:
            i += 1
    
    return shapes


def rotate_shape(shape: Shape) -> Shape:
    """
    Rota una forma 90 grados en sentido horario.
    """
    if not shape:
        return []
    rows, cols = len(shape), len(shape[0])
    rotated = [[False] * rows for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            rotated[c][rows - 1 - r] = shape[r][c]
    return rotated


def flip_shape(shape: Shape) -> Shape:
    """
    Voltea una forma horizontalmente (reflejo sobre el eje vertical).
    """
    if not shape:
        return []
    return [row[::-1] for row in shape]


def normalize_shape(shape: Shape) -> Tuple[Tuple[bool, ...], ...]:
    """
    Normaliza una forma a una tupla de tuplas para poder compararla y evitar duplicados.
    """
    return tuple(tuple(row) for row in shape)


def get_all_variations(shape: Shape) -> List[Shape]:
    """
    Genera todas las variaciones únicas de una forma (rotaciones y reflejos).
    """
    variations = []
    seen = set()
    
    current = trim_shape(shape)
    for _ in range(4):  # 4 rotaciones
        trimmed = trim_shape(current)
        normalized = normalize_shape(trimmed)
        if normalized not in seen:
            seen.add(normalized)
            variations.append([row[:] for row in trimmed])
        
        # También probar el reflejo
        flipped = trim_shape(flip_shape(current))
        normalized_flipped = normalize_shape(flipped)
        if normalized_flipped not in seen:
            seen.add(normalized_flipped)
            variations.append([row[:] for row in flipped])
        
        # Rotar para la siguiente iteración
        current = rotate_shape(current)
    
    return variations


def get_shape_cells(shape: Shape) -> Cells:
    """
    Obtiene las coordenadas relativas de todas las celdas ocupadas (#) en una forma.
    """
    cells = []
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c]:
                cells.append((r, c))
    return cells


def get_shape_size(shape: Shape) -> Size:
    """
    Obtiene el tamaño (alto, ancho) de una forma.
    """
    return (len(shape), len(shape[0]) if shape else 0)


def can_place_shape(grid: List[List[bool]], shape_cells: Cells, 
                    row: int, col: int, width: int, height: int) -> bool:
    """
    Verifica si una forma puede ser colocada en la posición (row, col) del grid.
    Optimizado: recibe las celdas precomputadas en lugar de la forma completa.
    """
    for dr, dc in shape_cells:
        r, c = row + dr, col + dc
        if r < 0 or r >= height or c < 0 or c >= width:
            return False
        if grid[r][c]:  # Ya está ocupado
            return False
    return True


def place_shape(grid: List[List[bool]], shape_cells: Cells, 
                row: int, col: int) -> None:
    """
    Coloca una forma en el grid en la posición (row, col).
    Optimizado: recibe las celdas precomputadas.
    """
    for dr, dc in shape_cells:
        grid[row + dr][col + dc] = True


def remove_shape(grid: List[List[bool]], shape_cells: Cells, 
                 row: int, col: int) -> None:
    """
    Remueve una forma del grid en la posición (row, col).
    Optimizado: recibe las celdas precomputadas.
    """
    for dr, dc in shape_cells:
        grid[row + dr][col + dc] = False


def find_next_empty(grid: List[List[bool]]) -> Optional[Tuple[int, int]]:
    """
    Encuentra la siguiente celda vacía en orden fila-major.
    """
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if not val:
                return r, c
    return None


def backtrack(grid: List[List[bool]], pieces: List[Piece], width: int, height: int) -> bool:
    """
    Backtracking que intenta colocar cualquier pieza restante en cualquier posición válida.
    No fuerza cubrir todas las celdas (se permiten huecos), solo evitar solapamientos
    y mantener las piezas dentro de la región.
    """
    # Buscar próxima pieza con stock pendiente
    next_idx: Optional[int] = None
    for idx, (_, count) in enumerate(pieces):
        if count > 0:
            next_idx = idx
            break

    if next_idx is None:
        return True  # No quedan piezas por colocar

    variations_data, count = pieces[next_idx]

    for shape_cells, (shape_height, shape_width), _cell_count in variations_data:
        # Iterar todas las posiciones donde la caja de la pieza cabe
        for row in range(height - shape_height + 1):
            for col in range(width - shape_width + 1):
                if can_place_shape(grid, shape_cells, row, col, width, height):
                    place_shape(grid, shape_cells, row, col)
                    pieces[next_idx] = (variations_data, count - 1)

                    if backtrack(grid, pieces, width, height):
                        return True

                    remove_shape(grid, shape_cells, row, col)
                    pieces[next_idx] = (variations_data, count)

    return False


def solve_region(width: int, height: int, requirements: List[int], all_shape_variations: List[List[Shape]]) -> bool:
    """
    Intenta resolver si todas las piezas requeridas caben en una región.
    Optimizado con precomputación de celdas y mejor ordenamiento.
    
    Args:
        width: Ancho de la región
        height: Alto de la región
        requirements: Lista con la cantidad de cada forma requerida
        all_shape_variations: Lista de todas las variaciones de cada forma
    
    Returns:
        True si todas las piezas caben, False en caso contrario
    """
    # Verificación temprana: calcular espacio total necesario
    total_cells_needed = 0
    for shape_idx, count in enumerate(requirements):
        if count > 0 and all_shape_variations[shape_idx]:
            cells_per_piece = len(get_shape_cells(all_shape_variations[shape_idx][0]))
            total_cells_needed += cells_per_piece * count
    
    total_space = width * height
    if total_cells_needed > total_space:
        return False
    
    # Crear grid vacío
    grid = [[False] * width for _ in range(height)]
    
    # Preparar lista de piezas a colocar con celdas precomputadas
    pieces: List[Piece] = []
    for shape_idx, count in enumerate(requirements):
        if count > 0:
            # Precomputar celdas y tamaños para cada variación
            variations_data: List[Variation] = []
            for variation in all_shape_variations[shape_idx]:
                shape_cells = get_shape_cells(variation)
                shape_size = get_shape_size(variation)
                variations_data.append((shape_cells, shape_size, len(shape_cells)))
            pieces.append((variations_data, count))
    
    # Ordenar por tamaño de pieza (más grandes primero) y luego por cantidad
    pieces.sort(key=lambda item: (item[0][0][2], item[1]), reverse=True)

    # Intentar resolver con backtracking
    return backtrack(grid, pieces, width, height)


def parse_regions(input_lines: List[str]) -> List[Tuple[int, int, List[int]]]:
    """
    Parsea las regiones del input.
    Retorna una lista de tuplas (width, height, requirements).
    """
    regions = []
    for line in input_lines:
        line = line.strip()
        if 'x' in line and ':' in line:
            # Formato: "widthxheight: req1 req2 ..."
            parts = line.split(':')
            size_part = parts[0].strip()
            reqs_part = parts[1].strip()
            
            width, height = map(int, size_part.split('x'))
            requirements = list(map(int, reqs_part.split()))
            regions.append((width, height, requirements))
    
    return regions


def read_input(path: Path) -> List[str]:
    """
    Lee el archivo de entrada y retorna una lista de líneas.
    
    Args:
        path: Ruta al archivo de entrada
    
    Returns:
        Lista de líneas del archivo
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()


def main():
    """
    Función principal que resuelve el problema.
    """
    # Leer el archivo de entrada (cambiar a INPUT_FILE para el problema real)
    input_file = Path(INPUT_FILE)  # Cambiar a INPUT_FILE para el problema completo
    lines = read_input(input_file)
    
    # Separar las formas de las regiones
    shape_end_idx = len(lines)
    for i, line in enumerate(lines):
        # Detectar primera región: formato "númeroxnúmero:"
        if 'x' in line and ':' in line:
            # Verificar que es una región y no una forma
            parts = line.split(':')
            if len(parts) == 2 and 'x' in parts[0]:
                shape_end_idx = i
                break
    
    shape_lines = lines[:shape_end_idx]
    region_lines = lines[shape_end_idx:]
    
    # Parsear formas
    shapes = parse_shapes(shape_lines)
    print(f"Formas parseadas: {len(shapes)}")
    
    # Generar todas las variaciones de cada forma
    all_shape_variations = []
    for shape in shapes:
        variations = get_all_variations(shape)
        all_shape_variations.append(variations)
        print(f"Forma {len(all_shape_variations) - 1}: {len(variations)} variaciones únicas")
    
    # Parsear regiones
    regions = parse_regions(region_lines)
    print(f"\nRegiones a procesar: {len(regions)}")
    
    # Resolver cada región
    solvable_count = 0
    for idx, (width, height, requirements) in enumerate(regions):
        print(f"Procesando región {idx + 1}/{len(regions)}: {width}x{height}", end=' ... ')
        
        if solve_region(width, height, requirements, all_shape_variations):
            solvable_count += 1
            print("✓ SOLUCIONABLE")
        else:
            print("✗ NO SOLUCIONABLE")
    
    print(f"\n{'='*60}")
    print(f"RESULTADO FINAL: {solvable_count} regiones pueden acomodar todos sus regalos")
    print(f"{'='*60}")
    
    return solvable_count


if __name__ == '__main__':
    main()

