from pathlib import Path
from typing import Final, Dict, List
from functools import lru_cache

TEST_INPUT: Final[str] = "test.txt"
REAL_INPUT: Final[str] = "input.txt"


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


def main() -> None:
    input_path = Path(REAL_INPUT)
    lines = read_input(input_path)
    graph = parse_graph(lines)
    
    result = count_paths(graph, "you", "out")
    print(f"Part 1: {result}")


if __name__ == "__main__":
    main()