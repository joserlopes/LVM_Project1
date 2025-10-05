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

    # Since we only have black pegs, consider the number of combinations of size `peg_value`
    # because we know for sure one of those combinations is right
    for guess_i, black_peg_i, white_peg_i in zip(
        range(0, len(B), 3), range(1, len(B), 3), range(2, len(B), 3)
    ):
        guess = B[guess_i]
        black_peg = B[black_peg_i]
        white_peg = B[white_peg_i]

        guess_with_indices = list(enumerate(guess))
        if black_peg == 0 and white_peg == 0:
            for value_i, value in guess_with_indices:
                s.add(Not(P[value_i][value]))
        else:
            black_combinations_list = combinations(guess_with_indices, black_peg)
            # Essentially what this is doing is it adds a clause for each combination that says
            # that the numbers in combination can be part of the right solution and the others
            # not so...
            clauses_to_add = []
            for black_combination in black_combinations_list:
                available_spots = [
                    x[0] for x in guess_with_indices if x not in black_combination
                ]
                for white_combination in combinations(available_spots, white_peg):
                    for white_position in white_combination:
                        clauses_to_add.append(
                            Not(P[white_position][guess[white_position]])
                        )
                    for white_permutation in permutations(available_spots, white_peg):
                        if any(
                            white_permutation[i] == white_combination[i]
                            for i in range(white_peg)
                        ):
                            continue

                        present = []
                        not_present = []
                        white_available_spots = [
                            x for x in available_spots if x not in white_permutation
                        ]
                        print("White available spots:", white_available_spots)
                        for original_position, new_position in zip(
                            white_combination, white_permutation
                        ):
                            print("Original position:", original_position)
                            print("New position:", new_position)
                            present.append(P[new_position][guess[original_position]])
                            for white_available_spot in white_available_spots:
                                not_present.append(
                                    Not(P[white_available_spot][guess[new_position]])
                                )
                        clauses_to_add.append(And(present + not_present))
                    s.add(Or(clauses_to_add))
                    print(s)

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
# print(mastermind2(B1))
print(mastermind2(B2))
