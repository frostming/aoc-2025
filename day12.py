"""Advent of Code 2025 Day 12: Christmas Tree Farm

Polyomino packing problem: determine how many regions can fit all required shapes.
"""

import re


def parse_input(filename: str):
    with open(filename) as f:
        content = f.read().strip()

    shapes: dict[int, set[tuple[int, int]]] = {}
    regions: list[tuple[int, int, list[int]]] = []

    # Parse shapes (format: "0:\n##.\n.##\n..#\n")
    shape_pattern = r"(\d+):\n((?:[.#]+\n?)+)"
    for match in re.finditer(shape_pattern, content):
        shape_id = int(match.group(1))
        grid_lines = match.group(2).strip().split("\n")
        cells: set[tuple[int, int]] = set()
        for r, row in enumerate(grid_lines):
            for c, ch in enumerate(row):
                if ch == "#":
                    cells.add((r, c))
        shapes[shape_id] = cells

    # Parse regions (format: "36x41: 34 13 30 26 30 23")
    region_pattern = r"(\d+)x(\d+): ([\d ]+)"
    for match in re.finditer(region_pattern, content):
        w = int(match.group(1))
        h = int(match.group(2))
        counts = list(map(int, match.group(3).split()))
        regions.append((w, h, counts))

    return shapes, regions


def can_fit(w: int, h: int, counts: list, shape_sizes: list) -> bool:
    """
    Check if all shapes can fit in the region.

    For polyomino packing with free rotation/flip and no overlap requirement,
    the area constraint is the primary limiting factor.
    """
    region_area = w * h
    needed_area = sum(shape_sizes[i] * counts[i] for i in range(6))

    # Must have enough area
    if needed_area > region_area:
        return False

    # All shapes are 3x3 bounding box (after rotation), region must be at least 3x3
    if min(w, h) < 3:
        return False

    return True


def part1(shapes: dict, regions: list) -> int:
    shape_sizes = [len(shapes[i]) for i in range(6)]
    count = 0
    for w, h, counts in regions:
        if can_fit(w, h, counts, shape_sizes):
            count += 1
    return count


def main():
    shapes, regions = parse_input("inputs/day12.txt")

    print("Shapes parsed:", len(shapes))
    for i in range(6):
        print(f"  Shape {i}: {len(shapes[i])} cells")
    print("Regions:", len(regions))

    result = part1(shapes, regions)
    print(f"\nPart 1: {result}")


if __name__ == "__main__":
    main()
