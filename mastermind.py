from z3 import And, Bool, Implies, Not, Or, Solver, sat
from itertools import combinations, permutations


def convert(w):
    a = sorted(
        [(int(p.split("_")[1]), int(p.split("_")[2])) for p in w], key=lambda x: x[0]
    )
    return "".join([str(l[1]) for l in a])


def mastermind2(B):
    guess_len = len(B[0])
    P = [[Bool(f"P_{i}_{n}") for n in range(10)] for i in range(1, guess_len + 1)]
    s = Solver()

    for guess_i, black_peg_i, white_peg_i in zip(
        range(0, len(B), 3), range(1, len(B), 3), range(2, len(B), 3)
    ):
        guess = B[guess_i]
        black_peg = B[black_peg_i]
        white_peg = B[white_peg_i]

        guess_with_indices = list(enumerate(guess))
        if black_peg == 0:
            for value_i, value in guess_with_indices:
                s.add(Not(P[value_i][value]))
        black_combinations_list = combinations(range(guess_len), black_peg)
        clauses_to_add = []
        for black_combination in black_combinations_list:
            locked_present = []
            for black_i in black_combination:
                locked_present.append(P[black_i][guess[black_i]])
            available_spots = [
                x for x in range(guess_len) if x not in black_combination
            ]
            for white_combination in combinations(available_spots, white_peg):
                not_present = []

                for white_position in white_combination:
                    not_present.append(Not(P[white_position][guess[white_position]]))

                for white_permutation in permutations(available_spots, white_peg):
                    present = []
                    if any(
                        white_permutation[i] == white_combination[i]
                        for i in range(white_peg)
                    ):
                        continue

                    for original_position, new_position in zip(
                        white_combination, white_permutation
                    ):
                        present.append(P[new_position][guess[original_position]])
                    clauses_to_add.append(And(locked_present + present + not_present))
        s.add(Or(clauses_to_add))

    # Each position needs to have a number
    for pos in P:
        s.add(Or(pos))

    # Each position can only have *one* number
    for i in range(guess_len):
        for j in range(10 - 1):
            for k in range(j + 1, 10):
                s.add(Implies(P[i][j], Not(P[i][k])))

    solutions = []
    while s.check() == sat:
        m = s.model()
        candidates = [p.name() for p in m.decls() if m[p]]

        solutions.append(convert(candidates))

        block = [p() != m[p] for p in m.decls()]
        s.add(Or(block))

    return solutions


def unique_solution2(B):
    return len(mastermind2(B)) == 1


B1 = [
    [1, 1, 2, 2],
    0,
    1,
    [3, 4, 4, 1],
    1,
    1,
    [5, 3, 5, 1],
    1,
    1,
    [6, 6, 3, 1],
    0,
    1,
    [2, 4, 5, 3],
    1,
    3,
]

B2 = [
    [1, 2, 3, 4, 5, 6],
    1,
    2,
]
print(mastermind2(B1))
# print(mastermind2(B2))
