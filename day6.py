from typing import IO


def _get_last_line(f: IO[str]) -> str:
    f.seek(0, 2)  # Move to the end of the file
    pos = f.tell() - 2  # skip the last newline
    while pos >= 0:
        f.seek(pos)
        if f.read(1) == "\n":
            break
        pos -= 1
    line = f.readline()
    f.seek(0)  # Reset file pointer to the beginning
    return line.strip()


def part1():
    with open("inputs/day6.txt") as f:
        last_line = _get_last_line(f)
        operators = [x == "*" for x in last_line.split()]
        results = [1 if op else 0 for op in operators]  # Initial values

        for line in f:
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            for i, c in enumerate(line.split()):
                if operators[i]:
                    results[i] *= int(c)
                else:
                    results[i] += int(c)
        return sum(results)


def _read_in_column(f: IO[str], col_index: int) -> str | None:
    f.seek(0)
    column_chars = []
    for line in f:
        line = line.rstrip()
        if len(line) > col_index:
            column_chars.append(line[col_index])
    f.seek(0)
    return "".join(column_chars).strip() if column_chars else None


def part2():
    with open("inputs/day6.txt") as f:
        result = 0
        new_problem = True
        col_index = 0
        temp = 0
        is_multiplication = False
        while True:
            column_data = _read_in_column(f, col_index)
            col_index += 1
            if column_data is None:
                result += temp
                break
            if column_data == "":
                new_problem = True
                result += temp
                continue
            if new_problem:
                temp = int(column_data[:-1])
                is_multiplication = column_data[-1] == "*"
                new_problem = False
            else:
                if is_multiplication:
                    temp *= int(column_data)
                else:
                    temp += int(column_data)
        return result


if __name__ == "__main__":
    result = part1()
    print(f"Final result (part 1): {result}")
    result = part2()
    print(f"Final result (part 2): {result}")
