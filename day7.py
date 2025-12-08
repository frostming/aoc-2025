def part1():
    total_splits = 0
    with open("inputs/day7.txt") as f:
        first_line = next(f).strip()
        state = [0] * len(first_line)
        state[first_line.find("S")] = 1  # Start position
        print("DEBUG: ", state)
        for line in f:
            for i, c in enumerate(line.strip()):
                if c == "." or state[i] == 0:
                    continue
                # c == '^', split the beam
                if i > 0:
                    state[i - 1] = 1
                if i < len(state) - 1:
                    state[i + 1] = 1
                total_splits += 1
                state[i] = 0  # Beam consumed
            print("DEBUG: ", state)
    return total_splits


def part2():
    with open("inputs/day7.txt") as f:
        first_line = next(f).strip()
        state = [0] * len(first_line)
        state[first_line.find("S")] = 1  # Start position
        print("DEBUG: ", state)
        for line in f:
            for i, c in enumerate(line.strip()):
                if c == "." or state[i] == 0:
                    continue
                # c == '^', split the beam
                if i > 0:
                    state[i - 1] += state[i]
                if i < len(state) - 1:
                    state[i + 1] += state[i]
                state[i] = 0  # Beam consumed
            print("DEBUG: ", state)
    return sum(state)


if __name__ == "__main__":
    result = part1()
    print(f"Total beam splits (part 1): {result}")

    result2 = part2()
    print(f"Total timeline splits (part 2): {result2}")
