from typing import IO, NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def read_all_points(fp: IO[str]) -> list[Point]:
    points: list[Point] = []
    for line in fp:
        points.append(Point(*map(int, line.strip().split(","))))
    return points


def part1(fp: IO[str]) -> int:
    points = read_all_points(fp)

    ans = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dx = abs(points[i].x - points[j].x) + 1
            dy = abs(points[i].y - points[j].y) + 1
            ans = max(ans, dx * dy)

    return ans


def part2(fp: IO[str]) -> int:
    # Parse coordinates
    red_tiles = read_all_points(fp)

    n = len(red_tiles)

    # Build edge segments (both horizontal and vertical)
    h_edges = []  # (y, x_min, x_max) for horizontal edges
    v_edges = []  # (x, y_min, y_max) for vertical edges

    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]
        if y1 == y2:  # Horizontal edge
            h_edges.append((y1, min(x1, x2), max(x1, x2)))
        else:  # Vertical edge
            v_edges.append((x1, min(y1, y2), max(y1, y2)))

    def point_inside_or_on_boundary(px: int, py: int) -> bool:
        """Check if point is inside polygon or on boundary using ray casting"""
        # Check if on boundary first
        for y, x_min, x_max in h_edges:
            if py == y and x_min <= px <= x_max:
                return True
        for x, y_min, y_max in v_edges:
            if px == x and y_min <= py <= y_max:
                return True

        # Ray casting: count crossings going right
        crossings = 0
        for x, y_min, y_max in v_edges:
            if x > px and y_min < py < y_max:
                crossings += 1

        return crossings % 2 == 1

    def rectangle_valid(rx_min: int, rx_max: int, ry_min: int, ry_max: int) -> bool:
        """Check if rectangle is entirely inside polygon"""
        # Check all 4 geometric corners are inside or on boundary
        corners = [
            (rx_min, ry_min),
            (rx_min, ry_max),
            (rx_max, ry_min),
            (rx_max, ry_max),
        ]
        for cx, cy in corners:
            if not point_inside_or_on_boundary(cx, cy):
                return False

        # Check that no red tile is strictly inside the rectangle
        for rx, ry in red_tiles:
            if rx_min < rx < rx_max and ry_min < ry < ry_max:
                return False

        # Check if any boundary edge completely crosses through the rectangle
        # (i.e., the edge spans the full width/height and cuts the rectangle in two)

        # Horizontal edges that cross full width
        for y, x_min, x_max in h_edges:
            if ry_min < y < ry_max:  # Edge is in interior y-range
                if x_min <= rx_min and x_max >= rx_max:
                    # Edge spans full width - rectangle is cut in two
                    return False

        # Vertical edges that cross full height
        for x, y_min, y_max in v_edges:
            if rx_min < x < rx_max:  # Edge is in interior x-range
                if y_min <= ry_min and y_max >= ry_max:
                    # Edge spans full height - rectangle is cut in two
                    return False

        # Also check for edges that have endpoints strictly inside the rectangle
        # (meaning the boundary turns inside the rectangle)
        for y, x_min, x_max in h_edges:
            if ry_min < y < ry_max:  # Edge in interior y-range
                # Check if endpoints are strictly inside x-range
                if rx_min < x_min < rx_max or rx_min < x_max < rx_max:
                    return False

        for x, y_min, y_max in v_edges:
            if rx_min < x < rx_max:  # Edge in interior x-range
                if ry_min < y_min < ry_max or ry_min < y_max < ry_max:
                    return False

        return True

    # Find largest rectangle where both corners are red tiles and rectangle is valid
    max_area = 0
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]

            rx_min, rx_max = min(x1, x2), max(x1, x2)
            ry_min, ry_max = min(y1, y2), max(y1, y2)

            area = (rx_max - rx_min + 1) * (ry_max - ry_min + 1)
            if area <= max_area:
                continue  # Skip if can't beat current best

            if rectangle_valid(rx_min, rx_max, ry_min, ry_max):
                print(f"DEBUG: ({x1},{y1}) to ({x2},{y2}) area={area}")
                max_area = area

    return max_area


if __name__ == "__main__":
    with open("inputs/day9.txt") as f:
        print(f"Part 1: {part1(f)}")
        f.seek(0)
        print(f"Part 2: {part2(f)}")
