def part1():
    total_zeros = 0
    cursor = 50
    max_distance = 100
    for line in open("inputs/day1.txt"):
        line = line.strip()
        if not line:
            continue
        direction, steps = line[0], int(line[1:])
        if direction == "R":
            cursor = (cursor + steps) % max_distance
        else:
            cursor = (cursor - steps) % max_distance
        if cursor == 0:
            total_zeros += 1
    return total_zeros


def part2():
    total_zeros = 0
    cursor = 50
    max_distance = 100
    for line in open("inputs/day1.txt"):
        line = line.strip()
        if not line:
            continue
        direction, steps = line[0], int(line[1:])
        circles, remainder = divmod(steps, max_distance)
        new_position = cursor + remainder if direction == "R" else cursor - remainder
        total_zeros += circles + int(
            cursor > 0 and new_position <= 0 or new_position >= max_distance
        )
        cursor = new_position % max_distance
        print(
            f"Current cursor position after {line}: {cursor} (total zeros: {total_zeros})"
        )
    return total_zeros


if __name__ == "__main__":
    result = part1()
    print(f"Total times cursor returned to zero: {result}")
    result = part2()
    print(f"Total times cursor passed through zero: {result}")
