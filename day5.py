from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int
    next: "Range | None" = None

    def insert(self, start: int, end: int) -> None:
        cur = self
        while cur.end < start - 1 and cur.next is not None:
            cur = cur.next
        if cur.end < start - 1:  # insert at end
            assert cur.next is None
            cur.next = Range(start, end)
            return
        if end < cur.start - 1:  # insert before current
            new_cur = Range(cur.start, cur.end, cur.next)
            cur.start, cur.end, cur.next = start, end, new_cur
            return
        cur.start = min(cur.start, start)
        cur.end = max(cur.end, end)
        # merge with next ranges if needed
        while cur.next is not None and cur.end >= cur.next.start - 1:
            cur.end = max(cur.end, cur.next.end)
            cur.next = cur.next.next

    def is_fresh(self, number: int) -> bool:
        cur = self
        while cur is not None:
            if cur.start <= number <= cur.end:
                return True
            cur = cur.next
        return False

    def __repr__(self) -> str:
        return self.pprint()

    def pprint(self) -> str:
        cur = self
        repr_str = []
        while cur is not None:
            if cur.start != 0 or cur.end != 0:
                repr_str.append(f"[{cur.start:_}, {cur.end:_}] -> ")
            cur = cur.next
        repr_str.append("END")
        return "".join(repr_str)


def part1():
    finish_ranges = False
    fresh_count = 0
    ranges = []
    with open("inputs/day5.txt") as f:
        for line in f:
            if not line.strip():
                finish_ranges = True
                continue
            if not finish_ranges:
                start, end = map(int, line.strip().split("-"))
                ranges.append((start, end))
            else:
                number = int(line.strip())
                for start, end in ranges:
                    if start <= number <= end:
                        fresh_count += 1
                        break
    return fresh_count


def part2():
    head = Range(0, 0)
    with open("inputs/day5.txt") as f:
        for line in f:
            if not line.strip():
                print(head)
                break
            start, end = map(int, line.strip().split("-"))
            head.insert(start, end)
    fresh_count = 0
    cur = head
    while cur is not None:
        if cur.start != 0 or cur.end != 0:
            fresh_count += cur.end - cur.start + 1
        cur = cur.next
    return fresh_count


if __name__ == "__main__":
    # result = part1()
    # print(f"Total fresh ingredients: {result}")
    result = part2()
    print(f"Total fresh ingredients (part 2): {result}")
