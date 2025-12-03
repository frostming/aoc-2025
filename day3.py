def part1(line: str) -> int:
    best = 0
    max_right = -1
    for i in range(len(line) - 1, -1, -1):
        d = int(line[i])
        if max_right != -1:
            best = max(best, d * 10 + max_right)
        max_right = max(max_right, d)
    print("Best for line", line, "is", best)
    return best


def part2(line: str, k: int = 12) -> int:
    stack = []
    to_remove = len(line) - k
    for c in line:
        while to_remove > 0 and stack and stack[-1] < c:
            stack.pop()
            to_remove -= 1
        stack.append(c)
    number = int("".join(stack[:k]))
    return number


def main():
    result = 0
    with open("inputs/day3.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            result += part2(line)
    print(f"Sum of best values: {result}")


if __name__ == "__main__":
    main()
