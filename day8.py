import bisect
import functools
import operator


def get_distance(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> int:
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2


def part1(k: int = 10):
    # Each item is (distance, i, j)
    distance_list: list[tuple[int, int, int]] = []
    is_saturated: bool = False
    points: list[tuple[int, int, int]] = []
    with open("inputs/test.txt") as f:
        for line in f:
            line = line.strip()
            x, y, z = map(int, line.split(","))
            points.append((x, y, z))
    number_points = len(points)
    boxes = [0] * number_points
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            # the distance should be euclidean distance, but manhattan distance works as well
            dist = get_distance(points[i], points[j])
            if not is_saturated or dist < distance_list[-1][0]:
                bisect.insort(distance_list, (dist, i, j))
                if is_saturated:
                    distance_list.pop()
                if not is_saturated and len(distance_list) >= k:
                    is_saturated = True

    max_box_size = 1
    for _, i, j in distance_list:
        box_index = max(boxes[i], boxes[j])
        if box_index == 0:
            box_index = max_box_size
            max_box_size += 1
            boxes[i] = boxes[j] = box_index
        elif 0 in (boxes[i], boxes[j]):
            boxes[i] = boxes[j] = box_index
        else:
            lower_index = min(boxes[i], boxes[j])
            for m in range(number_points):
                if boxes[m] == lower_index:
                    boxes[m] = box_index
    for _, i, j in distance_list:
        print(f"DEBUG: {points[i]}[{boxes[i]}] <-> {points[j]}[{boxes[j]}]")
    box_sizes = [0] * max_box_size
    for box_index in boxes:
        if box_index != 0:
            box_sizes[box_index] += 1
    print("Box sizes:", box_sizes)
    box_sizes.sort(reverse=True)
    return functools.reduce(operator.mul, box_sizes[:3])


def part2():
    # Each item is (distance, i, j)
    distance_list: list[tuple[int, int, int]] = []
    points: list[tuple[int, int, int]] = []
    with open("inputs/day8.txt") as f:
        for line in f:
            line = line.strip()
            x, y, z = map(int, line.split(","))
            points.append((x, y, z))
    number_points = len(points)
    boxes = [0] * number_points
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            # the distance should be euclidean distance, but manhattan distance works as well
            dist = get_distance(points[i], points[j])
            bisect.insort(distance_list, (dist, i, j))

    max_box_size = 1
    for _, i, j in distance_list:
        print(f"DEBUG: {points[i]} <-> {points[j]}")
        box_index = max(boxes[i], boxes[j])
        if box_index == 0:
            box_index = max_box_size
            max_box_size += 1
            boxes[i] = boxes[j] = box_index
        elif boxes[i] != boxes[j]:
            lower_index = min(boxes[i], boxes[j])
            if lower_index == 0:
                boxes[i] = boxes[j] = box_index
            else:
                for m in range(number_points):
                    if boxes[m] == lower_index:
                        boxes[m] = box_index
        if len(set(boxes)) == 1:
            return points[i][0] * points[j][0]


if __name__ == "__main__":
    # result = part1()
    # print(f"Product of box sizes: {result}")

    result = part2()
    print(f"Result of part 2: {result}")
