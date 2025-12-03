import math


def part1(start: int, end: int) -> int:
    print("DEBUG: get_invalid_ids", start, end)
    result = set()
    # for 10^n+1
    start_order = math.floor(math.log10(start)) + 1 if start > 0 else 1
    end_order = math.floor(math.log10(end)) + 1 if end > 0 else 1

    for n in range(max(1, start_order // 2), (end_order // 2) + 1):
        # multiples of 10...01, which should start from 10..(n-1 zeros) to 99..(n nines)
        number = 10**n + 1
        start_multiple = max(10 ** (n - 1), (start + number - 1) // number)
        end_multiple = min(number - 2, end // number)
        for multiple in range(start_multiple, end_multiple + 1):
            print(f"DEBUG: adding {number} multiple:", multiple * number)
            result.add(multiple * number)
    return sum(result)


def part2(start: int, end: int) -> int:
    print("DEBUG: get_invalid_ids", start, end)
    result = set()
    start_order = math.floor(math.log10(start)) + 1 if start > 0 else 1
    end_order = math.floor(math.log10(end)) + 1 if end > 0 else 1

    # for (10^n-1) // (10^k-1), where k divides n and n is the order of the number
    # For example, n=6: 111111, 10101, 1001
    for n in range(max(2, start_order), end_order + 1):
        nominor = 10**n - 1
        for k in range(1, n // 2 + 1):
            if n % k != 0:
                continue
            number = nominor // (10**k - 1)
            # multiples of 10...01, which should start from 10..(n-1 zeros) to 99..(n nines)
            start_multiple = max(10 ** (k - 1), (start + number - 1) // number)
            end_multiple = min(10**k - 1, end // number)
            for multiple in range(start_multiple, end_multiple + 1):
                print(f"DEBUG: adding {number} multiple:", multiple * number)
                result.add(multiple * number)
    return sum(result)


def main():
    with open("inputs/day2.txt") as f:
        data = f.read().strip()

    result = 0

    for line in data.split(","):
        start, end = map(int, line.split("-"))
        result += part2(start, end)
    print(f"Sum of all invalid IDs: {result}")


if __name__ == "__main__":
    main()
