from typing import IO


def parse_light(light: str) -> int:
    """parse ligt string like .#..#..## into integer bitmask
    The leftmost character is the lowest bit, and the rightmost character is the highest bit.
    """
    result = 0
    for ch in reversed(light[1:-1]):
        result = (result << 1) | (1 if ch == "#" else 0)
    return result


def parse_button(button: str) -> int:
    result = 0
    for ch in button[1:-1].split(","):
        result += 2 ** int(ch)
    return result


def part1(f: IO[str]) -> int:
    def min_presses(light: int, buttons: list[int], left: int = 0) -> int:
        if light == 0:
            return 0
        elif left >= len(buttons):
            return -2  # Impossible, use -2 so that it's still negative after +1
        presses_with = min_presses(light ^ buttons[left], buttons, left + 1) + 1
        presses_without = min_presses(light, buttons, left + 1)
        return min((p for p in (presses_with, presses_without) if p >= 0), default=-2)

    ans = 0
    for line in f:
        light_str, *button_strs, _ = line.strip().split()
        light = parse_light(light_str)
        buttons = [parse_button(bs) for bs in button_strs]
        presses = min_presses(light, buttons)
        assert presses >= 0, "Should be possible"
        print(f"DEBUG: {light = :b}, {presses = }")
        ans += presses

    return ans


def _pretty_print_matrix(mat):
    for row in mat:
        print(
            " ".join(
                f"{v.numerator}{f'/{v.denominator}' if v.denominator != 1 else ''}"
                for v in row
            )
        )
    print()


def min_joltage_presses(buttons: list[int], joltage: tuple[int, ...]) -> int | float:
    """Find minimum button presses to achieve target joltage values.

    Uses Gaussian elimination to find the solution space, then searches
    for minimum L1-norm solution.
    """
    from fractions import Fraction

    n_buttons = len(buttons)
    n_counters = len(joltage)

    # Build matrix A where A[i][j] = 1 if button j affects counter i
    A = [[Fraction(0)] * n_buttons for _ in range(n_counters)]
    for j, button_mask in enumerate(buttons):
        for i in range(n_counters):
            if button_mask & (1 << i):
                A[i][j] = Fraction(1)

    b = [Fraction(v) for v in joltage[:n_counters]]

    # Augmented matrix [A | b]
    mat = [row[:] + [b[i]] for i, row in enumerate(A)]
    n, m = n_counters, n_buttons

    # Gaussian elimination to row echelon form
    pivot_row = 0
    pivot_cols = []
    for col in range(m):
        # Find pivot in this column
        found = -1
        for row in range(pivot_row, n):
            if mat[row][col] != 0:
                found = row
                break
        if found == -1:
            continue

        # Swap rows
        mat[pivot_row], mat[found] = mat[found], mat[pivot_row]

        # Normalize pivot row
        piv = mat[pivot_row][col]
        for c in range(col, m + 1):
            mat[pivot_row][c] /= piv

        # Eliminate in other rows
        for row in range(n):
            if row != pivot_row and mat[row][col] != 0:
                factor = mat[row][col]
                for c in range(col, m + 1):
                    mat[row][c] -= factor * mat[pivot_row][c]

        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row >= n:
            break

    # Check consistency
    for row in range(pivot_row, n):
        if mat[row][m] != 0:
            return float("inf")  # Inconsistent

    # Identify free variables
    free_vars = [j for j in range(m) if j not in pivot_cols]
    n_free = len(free_vars)

    # If no free variables, unique solution
    if n_free == 0:
        x = [Fraction(0)] * m
        for i, col in enumerate(pivot_cols):
            x[col] = mat[i][m]
        # Check non-negative integer
        total = 0
        for val in x:
            if val < 0 or val.denominator != 1:
                return float("inf")
            total += int(val)
        return total

    # With free variables, solve the optimization problem
    # x[pivot_col] = mat[row][m] - sum(mat[row][fv] * x[fv]) for free vars fv
    # Objective: min sum(x) = sum(x[fv]) + sum(x[pivot_col])
    #          = sum(x[fv]) + sum(mat[row][m] - sum(mat[row][fv] * x[fv]))
    #          = sum(mat[row][m]) + sum(x[fv] * (1 - sum_over_rows(mat[row][fv])))

    pivot_to_row = {col: i for i, col in enumerate(pivot_cols)}

    # Compute objective coefficients for free variables
    # coef[j] = 1 - sum over pivot rows of mat[row][fv_j]
    obj_coef = []
    for fv in free_vars:
        col_sum = sum(mat[pivot_to_row[pc]][fv] for pc in pivot_cols)
        obj_coef.append(1 - col_sum)

    # Constraints: for each pivot col, x[pc] = mat[row][m] - sum(mat[row][fv] * x[fv]) >= 0
    # i.e., sum(mat[row][fv] * x[fv]) <= mat[row][m]

    # For small n_free, enumerate intelligently
    # For each free var, find valid range considering all constraints
    best = [float("inf")]

    def eval_solution(free_vals: list[int]) -> int | None:
        x = [Fraction(0)] * m
        for i, fv in enumerate(free_vars):
            x[fv] = Fraction(free_vals[i])

        total = Fraction(0)
        for i, fv in enumerate(free_vars):
            total += free_vals[i]

        for col in pivot_cols:
            row = pivot_to_row[col]
            val = mat[row][m]
            for fv in free_vars:
                val -= mat[row][fv] * x[fv]
            if val < 0 or val.denominator != 1:
                return None
            total += int(val)

        return int(total) if total.denominator == 1 else None

    # Use linear programming insight:
    # If obj_coef[j] > 0, prefer x[fv_j] = 0
    # If obj_coef[j] < 0, prefer x[fv_j] as large as possible
    # If obj_coef[j] = 0, x[fv_j] doesn't affect objective

    # Start with heuristic solution
    heuristic_vals: list[int] = []
    for i, fv in enumerate(free_vars):
        if obj_coef[i] >= 0:
            heuristic_vals.append(0)
        else:
            # Find max valid value for this free var given current vals
            max_v = 0
            for col in pivot_cols:
                row = pivot_to_row[col]
                if mat[row][fv] > 0:
                    # constraint: mat[row][m] - mat[row][fv] * x[fv] - other_terms >= 0
                    other = sum(
                        mat[row][free_vars[j]] * heuristic_vals[j]
                        for j in range(i)
                        if mat[row][free_vars[j]] != 0
                    )
                    avail = mat[row][m] - other
                    if avail >= 0:
                        max_here = int(avail / mat[row][fv])
                        if max_v == 0:
                            max_v = max_here
                        else:
                            max_v = min(max_v, max_here)
            heuristic_vals.append(max_v)

    result = eval_solution(heuristic_vals)
    if result is not None:
        best[0] = result

    # For small n_free, do exhaustive search
    # Use max joltage as a safe bound for each free variable
    if n_free <= 5:
        max_fv = max(joltage) + 1

        from itertools import product

        for vals in product(range(max_fv), repeat=n_free):
            result = eval_solution(list(vals))
            if result is not None and result < best[0]:
                best[0] = result

    return best[0]


def part2(f: IO[str]) -> int:
    ans = 0
    for line in f:
        _, *button_strs, joltage_str = line.strip().split()
        buttons = [parse_button(bs) for bs in button_strs]
        joltage = tuple(tuple(int(c) for c in joltage_str[1:-1].split(",")))

        presses = int(min_joltage_presses(buttons, joltage))
        print(f"DEBUG: {joltage = }, {presses = }")
        ans += presses
    return ans


if __name__ == "__main__":
    with open("inputs/day10.txt") as f:
        result = part1(f)
        print(f"Part 1: {result}")
        f.seek(0)
        result = part2(f)
        print(f"Part 2: {result}")
