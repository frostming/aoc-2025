from collections import defaultdict
from functools import cache
from typing import IO


def read_graph(f: IO[str]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for line in f:
        src, outputs = line.strip().split(": ")
        for dst in outputs.split():
            graph[src].add(dst)
    return graph


def part1(graph: dict[str, set[str]]) -> int:
    def get_path_count(node: str, visited: set[str]) -> int:
        if node == "out":
            return 1
        count = 0
        for neighbor in graph[node]:
            if neighbor not in visited:
                new_visited = visited | {neighbor}
                count += get_path_count(neighbor, new_visited)
        return count

    return get_path_count("you", {"you"})


def part2(graph: dict[str, set[str]]) -> int:
    @cache
    def count_paths(
        node: str, visited_dac: bool = False, visited_fft: bool = False
    ) -> int:
        if node == "dac":
            visited_dac = True
        if node == "fft":
            visited_fft = True

        if node == "out":
            return 1 if (visited_dac and visited_fft) else 0
        if node not in graph:
            return 0

        return sum(count_paths(dest, visited_dac, visited_fft) for dest in graph[node])

    return count_paths("svr")


if __name__ == "__main__":
    with open("inputs/day11.txt") as f:
        graph = read_graph(f)
    print(f"Part 1: {part1(graph)}")
    print(f"Part 2: {part2(graph)}")
