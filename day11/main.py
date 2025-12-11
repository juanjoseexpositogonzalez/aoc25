from pathlib import Path
from typing import Final, Dict, List
from functools import lru_cache

TEST_INPUT: Final[str] = "test.txt"
REAL_INPUT: Final[str] = "input.txt"
TEST_INPUT_PART2: Final[str] = "test_part2.txt"


def read_input(path: Path) -> List[str]:
    with open(path, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def parse_graph(lines: List[str]) -> Dict[str, List[str]]:
    """Parse input into adjacency list."""
    graph: Dict[str, List[str]] = {}
    for line in lines:
        node, outputs = line.split(": ")
        graph[node] = outputs.split()
    return graph


def count_paths(graph: Dict[str, List[str]], start: str, end: str) -> int:
    """Count all paths from start to end using memoization."""
    
    @lru_cache(maxsize=None)
    def dfs(node: str) -> int:
        if node == end:
            return 1
        if node not in graph:
            return 0
        return sum(dfs(child) for child in graph[node])
    
    return dfs(start)


def count_paths_through_both(graph: Dict[str, List[str]], 
                              start: str, end: str, 
                              checkpoint1: str, checkpoint2: str) -> int:
    """
    Count paths from start to end that pass through BOTH checkpoints.
    """
    # Caso 1: start → checkpoint1 → checkpoint2 → end
    case1 = (count_paths(graph, start, checkpoint1) * 
             count_paths(graph, checkpoint1, checkpoint2) * 
             count_paths(graph, checkpoint2, end))
    
    # Caso 2: start → checkpoint2 → checkpoint1 → end
    case2 = (count_paths(graph, start, checkpoint2) * 
             count_paths(graph, checkpoint2, checkpoint1) * 
             count_paths(graph, checkpoint1, end))
    
    return case1 + case2


def main() -> None:
    # Part 1
    input_path = Path(REAL_INPUT)
    lines = read_input(input_path)
    graph = parse_graph(lines)
    
    result1 = count_paths(graph, "you", "out")
    print(f"Part 1: {result1}")
    
    # Part 2
    result2 = count_paths_through_both(graph, "svr", "out", "dac", "fft")
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()