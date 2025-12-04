import pprint


def part1():
    with open("inputs/day4.txt") as f:
        lines = f.readlines()

    array = [[0] * len(lines[0].strip()) for _ in range(len(lines))]
    for i, line in enumerate(lines):
        line = line.strip()
        for j, c in enumerate(line):
            if c == "@":
                # add one to its adjacent cells
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < len(lines) and 0 <= nj < len(line):
                            array[ni][nj] += 1

    pprint.pprint(array)
    total = 0
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] < 4 and lines[i][j] == "@":
                total += 1
    return total


def part2():
    with open("inputs/day4.txt") as f:
        lines = f.readlines()

    array = [[0 if c == "@" else -1 for c in line.strip()] for line in lines]
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] != -1:
                # add one to its adjacent cells
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < len(array) and 0 <= nj < len(array[i]):
                            if array[ni][nj] != -1:
                                array[ni][nj] += 1

    pprint.pprint(array)
    total = 0
    while True:
        changed = 0
        for i in range(len(array)):
            for j in range(len(array[0])):
                if 0 <= array[i][j] < 4:
                    changed += 1
                    array[i][j] = -1
                    # reduce adjacent cells by one
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < len(array) and 0 <= nj < len(array[i]):
                                if array[ni][nj] != -1:
                                    array[ni][nj] -= 1
        if changed == 0:
            break
        total += changed
    return total


if __name__ == "__main__":
    result = part2()
    print(f"Total safe '@' cells: {result}")
