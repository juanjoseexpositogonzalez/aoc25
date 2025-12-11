from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Final, List
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus  # type: ignore

TEST_INPUT: Final[str] = "test.txt"
REAL_INPUT: Final[str] = "input.txt"


@dataclass
class Machine:
    target: int = 0
    buttons: List[int] = field(default_factory=list)
    joltages: List[int] = field(default_factory=list)
    button_positions: List[List[int]] = field(default_factory=list)  # Nuevo: guardar posiciones originales

    def parse(self, tokens: List[str]) -> None:
        """Parse the tokens and update the machine state."""
        # Estado objetivo (parte 1)
        lights_str = tokens[0].strip('[]')
        self.target = self.lights_to_bitmask(lights_str)
        
        # Botones
        self.buttons = []
        self.button_positions = []
        for token in tokens[1:-1]:
            if token.startswith('('):
                positions_str = token.strip('()')
                positions = [int(p) for p in positions_str.split(',')]
                self.button_positions.append(positions)
                self.buttons.append(self.positions_to_bitmask(positions))
        
        # Joltages (parte 2)
        joltage_str = tokens[-1].strip('{}')
        self.joltages = [int(j) for j in joltage_str.split(',')]

    def find_minimum_presses_part2(self) -> int:
        """Find minimum button presses to reach joltage targets using ILP."""
        num_buttons = len(self.button_positions)
        num_counters = len(self.joltages)
        
        # Crear el problema
        prob = LpProblem("MinButtonPresses", LpMinimize)
        
        # Variables: x_i = pulsaciones del botón i (entero >= 0)
        x = [LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(num_buttons)]
        
        # Objetivo: minimizar total de pulsaciones
        prob += lpSum(x)
        
        # Restricciones: para cada contador, suma de pulsaciones = target
        for j in range(num_counters):
            # Sumar x_i para cada botón i que afecta al contador j
            prob += lpSum(x[i] for i in range(num_buttons) if j in self.button_positions[i]) == self.joltages[j]
        
        # Resolver
        prob.solve()  # type: ignore
        
        if LpStatus[prob.status] == 'Optimal':  # type: ignore
            return int(sum(var.varValue for var in x))  # type: ignore
        else:
            return -1  # Sin solución


    def positions_to_bitmask(self, positions: List[int]) -> int:
        """Convert a list of positions to a bitmask."""
        mask = 0
        for pos in positions:
            mask |= (1 << pos)
        return mask

    def lights_to_bitmask(self, lights: str) -> int:
        """Convert a string of lights to a bitmask."""
        mask = 0
        for i, c in enumerate(lights):
            if c == '#':
                mask |= (1 << i)
        return mask

    def __str__(self) -> str:
        return f"Target: 0b{self.target:0b}, Buttons: {[bin(b) for b in self.buttons]}"

    def find_minimum_presses(self) -> int:
        """Find the minimum number of button presses to reach target state."""
        # Caso especial: si target es 0, no necesitamos pulsar nada
        if self.target == 0:
            return 0
        
        n = len(self.buttons)
        
        # Probar subconjuntos de tamaño 1, 2, 3...
        for size in range(1, n + 1):
            for subset in combinations(self.buttons, size):
                # XOR de todos los botones en el subconjunto
                result = 0
                for button in subset:
                    result ^= button
                
                if result == self.target:
                    return size
        
        return -1  # No hay solución


def read_input(path: Path) -> List[str]:
    with open(path, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def parse_input(input_lines: List[str]) -> List[Machine]:
    """Parse all machines from input."""
    machines: List[Machine] = []
    for line in input_lines:
        tokens = line.split()
        machine = Machine()
        machine.parse(tokens)
        machines.append(machine)  # type: ignore
    return machines


def main() -> None:
    input_path = Path(REAL_INPUT)
    input_lines = read_input(input_path)
    machines = parse_input(input_lines)
    
    # Parte 1
    total_part1 = 0
    for i, machine in enumerate(machines):
        min_presses = machine.find_minimum_presses()
        total_part1 += min_presses
    print(f"Part 1: {total_part1}")
    
    # Parte 2
    total_part2 = 0
    for i, machine in enumerate(machines):
        min_presses = machine.find_minimum_presses_part2()
        print(f"Machine {i}: {min_presses} presses")
        total_part2 += min_presses
    print(f"Part 2: {total_part2}")


if __name__ == "__main__":
    main()
