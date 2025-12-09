import bisect
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Final, List, Self, Tuple, Set, Dict


TEST_FILE: Final[str] = 'test.txt'
INPUT_FILE: Final[str] = 'input.txt'


@dataclass
class Point:
    """
    Representa un punto en el espacio 2D.
    
    Usado para almacenar las coordenadas de los puntos rojos que forman el polígono.
    Los puntos se conectan en orden para formar el perímetro del polígono.

    Attributes:
        x: Coordenada x del punto.
        y: Coordenada y del punto.
    """
    x: int
    y: int

    def can_be_opposite_corner(self, other: Self) -> bool:
        """
        Verifica si este punto y otro pueden formar esquinas opuestas de un rectángulo.
        
        Para que dos puntos formen esquinas opuestas de un rectángulo válido,
        deben tener coordenadas x e y diferentes.
        
        Args:
            other: Otro punto a verificar.
            
        Returns:
            True si los puntos pueden formar esquinas opuestas, False en caso contrario.
        """
        return self.x != other.x and self.y != other.y


def read_file(file_path: Path) -> List[str]:
    """
    Lee el archivo y retorna una lista de líneas como strings.
    
    Optimización: Usa read().splitlines() que es más eficiente que readlines()
    para archivos grandes, ya que evita crear objetos de línea intermedios.

    Args:
        file_path: Ruta al archivo a leer.

    Returns:
        Lista de strings, una por cada línea del archivo (sin incluir el carácter de nueva línea).
    """
    with open(file_path, 'r') as file:
        return file.read().splitlines()


def parse_input(lines: List[str]) -> List[Point]:
    """
    Parsea una lista de strings de entrada en una lista de objetos Point.
    
    Formato esperado: cada línea contiene dos números separados por coma (ej: "4,5").
    Los puntos se interpretan como coordenadas (x, y) en el plano 2D.

    Args:
        lines: Lista de strings, cada uno con coordenadas separadas por coma (ej: "4,5").

    Returns:
        Lista de instancias Point correspondientes a las coordenadas en las líneas de entrada.
    """
    points: List[Point] = []
    for line in lines:
        x, y = line.split(',')
        points.append(Point(int(x), int(y)))
    return points


def rectangle_area(p1: Point, p2: Point) -> int:
    """
    Calcula el área del rectángulo formado por dos esquinas opuestas (inclusive).
    
    El área incluye tanto los bordes como el interior del rectángulo.
    Por ejemplo, un rectángulo de (0,0) a (2,2) tiene área 3x3 = 9.
    
    Args:
        p1: Primera esquina del rectángulo.
        p2: Esquina opuesta del rectángulo.

    Returns:
        El área del rectángulo (ancho × alto, ambos inclusive).
    """
    return (abs(p2.x - p1.x) + 1) * (abs(p2.y - p1.y) + 1)


def part_one(file: str) -> int:
    """
    Resuelve la parte 1: Encuentra el área máxima de un rectángulo formado por dos puntos opuestos.
    
    Algoritmo:
    1. Lee y parsea los puntos del archivo de entrada.
    2. Genera todas las combinaciones de pares de puntos.
    3. Para cada par que puede formar esquinas opuestas (diferentes x e y):
       - Calcula el área del rectángulo.
       - Actualiza el área máxima encontrada.
    
    Complejidad: O(n²) donde n es el número de puntos.
    
    Args:
        file: Ruta al archivo de entrada.

    Returns:
        El área máxima de un rectángulo formado por dos puntos opuestos.
    """
    lines = read_file(Path(file))
    points = parse_input(lines)
    
    max_area = 0
    for p1, p2 in combinations(points, 2):
        if p1.can_be_opposite_corner(p2):
            max_area = max(max_area, rectangle_area(p1, p2))
    
    return max_area


def compute_interior_ranges(red_points: List[Point]) -> Tuple[Dict[int, List[Tuple[int, int]]], List[int]]:
    """
    Calcula los rangos interiores del polígono y las coordenadas Y críticas ordenadas.
    
    Esta función utiliza un algoritmo de barrido vertical para determinar qué rangos
    horizontales de x están dentro del polígono para cada coordenada y crítica.
    
    Las Y críticas son aquellas donde:
    - Comienza o termina un segmento vertical
    - Existe un segmento horizontal
    
    Algoritmo:
    1. Identifica segmentos verticales y horizontales del polígono.
    2. Encuentra todas las Y críticas (donde cambian los rangos válidos).
    3. Para cada Y crítica, calcula los rangos de x que están dentro del polígono
       usando el principio de paridad (cada segmento vertical que cruza indica
       entrada/salida del polígono).
    4. Fusiona rangos solapados para cada fila.
    
    Args:
        red_points: Lista de puntos que forman los vértices del polígono en orden.

    Returns:
        Tupla con:
        - Diccionario {y: [(x_start, x_end), ...]} con rangos válidos por fila.
        - Lista ordenada de coordenadas Y críticas.
    """
    n = len(red_points)
    
    vertical_segments: List[Tuple[int, int, int]] = []
    horizontal_segments: List[Tuple[int, int, int]] = []
    
    for i in range(n):
        p1 = red_points[i]
        p2 = red_points[(i + 1) % n]
        
        if p1.x == p2.x:
            y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)
            vertical_segments.append((p1.x, y_min, y_max))
        else:
            x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
            horizontal_segments.append((p1.y, x_min, x_max))
    
    # Y críticas: donde cambian los rangos
    critical_ys: Set[int] = set()
    for _, y_min, y_max in vertical_segments:
        critical_ys.add(y_min)
        critical_ys.add(y_max)
    for y, _, _ in horizontal_segments:
        critical_ys.add(y)
    
    critical_ys_sorted = sorted(critical_ys)
    
    interior_ranges: Dict[int, List[Tuple[int, int]]] = {}
    
    for y in critical_ys_sorted:
        ranges: List[Tuple[int, int]] = []
        
        crossing_xs = sorted([x for x, y_min, y_max in vertical_segments if y_min <= y < y_max])
        for i in range(0, len(crossing_xs) - 1, 2):
            ranges.append((crossing_xs[i], crossing_xs[i + 1]))
        
        for seg_y, x_min, x_max in horizontal_segments:
            if seg_y == y:
                ranges.append((x_min, x_max))
        
        if ranges:
            ranges.sort()
            merged = [ranges[0]]
            for r_min, r_max in ranges[1:]:
                if r_min <= merged[-1][1] + 1:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], r_max))
                else:
                    merged.append((r_min, r_max))
            interior_ranges[y] = merged
    
    return interior_ranges, critical_ys_sorted


def is_range_covered(x_min: int, x_max: int, ranges: List[Tuple[int, int]]) -> bool:
    """
    Verifica si el rango [x_min, x_max] está completamente cubierto por algún rango en la lista.
    
    Un rango está cubierto si existe al menos un rango en la lista que lo contenga completamente.
    
    Args:
        x_min: Coordenada x mínima del rango a verificar.
        x_max: Coordenada x máxima del rango a verificar.
        ranges: Lista de tuplas (x_start, x_end) representando rangos válidos.

    Returns:
        True si [x_min, x_max] está completamente contenido en algún rango de la lista,
        False en caso contrario.
    """
    for r_min, r_max in ranges:
        if r_min <= x_min and x_max <= r_max:
            return True
    return False


def part_two(file: str) -> int:
    """
    Resuelve la parte 2: Encuentra el área máxima de un rectángulo completamente dentro del polígono.
    
    Algoritmo optimizado:
    1. Calcula los rangos interiores del polígono usando barrido vertical.
    2. Identifica las coordenadas Y críticas donde cambian los rangos válidos.
    3. Genera pares de puntos candidatos y los ordena por área descendente.
    4. Para cada rectángulo (de mayor a menor área):
       - Verifica solo las Y críticas dentro del rango del rectángulo.
       - Hace early exit si el área es menor al máximo actual.
       - Valida que todas las filas críticas estén completamente cubiertas.
    
    Optimizaciones clave:
    - Uso de barrido vertical para calcular rangos interiores eficientemente.
    - Verificación solo en Y críticas en lugar de todas las filas.
    - Ordenamiento descendente para early exit cuando el área es menor al máximo.
    - Búsqueda binaria para encontrar Y críticas relevantes.
    
    Complejidad: O(n² * k) donde n es número de puntos y k es número de Y críticas por rectángulo.
    
    Args:
        file: Ruta al archivo de entrada.

    Returns:
        El área máxima de un rectángulo completamente contenido en el polígono.
    """
    lines = read_file(Path(file))
    red_points = parse_input(lines)
    
    print(f"Puntos rojos: {len(red_points)}")
    
    interior_ranges, critical_ys = compute_interior_ranges(red_points)
    print(f"Y críticas: {len(critical_ys)}")
    
    def is_rect_valid(p1: Point, p2: Point) -> bool:
        """
        Verifica si un rectángulo formado por p1 y p2 está completamente dentro del polígono.
        
        Un rectángulo es válido si todas sus filas críticas están completamente cubiertas
        por rangos interiores. Solo verifica las Y críticas dentro del rango del rectángulo
        para optimizar el proceso.
        
        Args:
            p1: Primera esquina del rectángulo.
            p2: Esquina opuesta del rectángulo.
            
        Returns:
            True si el rectángulo está completamente dentro del polígono, False en caso contrario.
        """
        min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
        min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)
        
        # Solo verificar Y críticas dentro del rango usando búsqueda binaria
        left = bisect.bisect_left(critical_ys, min_y)
        right = bisect.bisect_right(critical_ys, max_y)
        
        # Verificar extremos
        if min_y not in interior_ranges:
            # Buscar la Y crítica justo antes de min_y
            if left > 0:
                prev_y = critical_ys[left - 1]
                if prev_y not in interior_ranges or not is_range_covered(min_x, max_x, interior_ranges[prev_y]):
                    return False
            else:
                return False
        elif not is_range_covered(min_x, max_x, interior_ranges[min_y]):
            return False
        
        # Verificar Y críticas en el rango
        for i in range(left, right):
            y = critical_ys[i]
            if y not in interior_ranges:
                return False
            if not is_range_covered(min_x, max_x, interior_ranges[y]):
                return False
        
        return True
    
    pairs = [
        (p1, p2) for p1, p2 in combinations(red_points, 2)
        if p1.can_be_opposite_corner(p2)
    ]
    pairs.sort(key=lambda p: rectangle_area(p[0], p[1]), reverse=True)
    print(f"Pares a verificar: {len(pairs)}")
    
    max_area = 0
    checked = 0
    for p1, p2 in pairs:
        area = rectangle_area(p1, p2)
        if area <= max_area:
            break  # Early exit: áreas siguientes serán menores
        
        checked += 1
        if checked % 10000 == 0:
            print(f"Verificados: {checked}...")
        
        if is_rect_valid(p1, p2):
            max_area = area
            print(f"Encontrado: {max_area} entre {p1} y {p2}")
    
    print(f"Pares verificados: {checked}")
    return max_area


def main() -> None:
    """
    Función principal que ejecuta ambas partes del desafío del día 9.
    
    Ejecuta primero la parte 1 y luego la parte 2, mostrando los resultados
    de cada una. Por defecto usa el archivo de prueba (TEST_FILE).
    
    Para ejecutar con el archivo de entrada real, cambiar TEST_FILE por INPUT_FILE
    en las llamadas a part_one y part_two.
    """
    print("=== Part One ===")
    result1 = part_one(TEST_FILE)
    print(f"Resultado: {result1}")
    
    print("\n=== Part Two ===")
    result2 = part_two(TEST_FILE)
    print(f"Resultado: {result2}")


if __name__ == "__main__":
    main()