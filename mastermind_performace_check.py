from z3 import And, Bool, Implies, Not, Or, Solver, sat
from itertools import combinations, permutations
import time, sys

def convert(w):
    a = sorted(
        [(int(p.split("_")[1]), int(p.split("_")[2])) for p in w], key=lambda x: x[0]
    )
    return "".join([str(l[1]) for l in a])


def mastermind2(B):
    guess_len = len(B[0])
    P = [[Bool(f"P_{i}_{n}") for n in range(10)] for i in range(1, guess_len + 1)]
    s = Solver()

    start_time = time.time()
    
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
            white_available_spots = [
                x for x in range(guess_len) if x not in black_combination
            ]

            for white_combination in combinations(white_available_spots, white_peg):
                not_present = []

                remaining_positions = [
                    x for x in white_available_spots if x not in white_combination
                ]

                for white_position in white_combination:
                    not_present.append(Not(P[white_position][guess[white_position]]))

                # NOTE: Here we can remove all the possible positions if the number doesn't
                # appear on black and white. Is this optimization worth it?
                # Yes :D //zemarques
                for remaining_position in remaining_positions:
                    not_present.append(
                        Not(P[remaining_position][guess[remaining_position]])
                    )

# para cada spot livre, as que fixamos como brancas podem estar lá, em qualquer posição.
# ['123456'] com 1 preta e 2 brancas.
# assumir que posição 1 está certa e que posição 2 e 3 têm numero certo, mas posição errada.
# temos as remaining positions negadas, para o numero que está lá
# e podemos ir por implicações. p_num_2 => And p_num_i for i = 4 through 6

                for new_pos in white_available_spots:
                    present = []
                    for white_pos in white_combination:
                        if new_pos != white_pos:
                            clause = [Not(P[new_pos][v]) for v in range(10) if v != guess[white_pos]]
                            present.append(Implies(P[new_pos][guess[white_pos]], And(clause)))
                    # present.append(Or(P[new_pos][guess[white_pos]]))
                    clauses_to_add.append(And(locked_present + present + not_present))


                # for white_permutation in permutations(white_available_spots, white_peg):
                #     present = []
                #     if any(
                #         white_permutation[i] == white_combination[i]
                #         for i in range(white_peg)
                #     ):
                #         continue

                #     for original_position, new_position in zip(
                #         white_combination, white_permutation
                #     ):
                #         present.append(P[new_position][guess[original_position]])
                #     clauses_to_add.append(And(locked_present + present + not_present))
        s.add(Or(clauses_to_add))

    # Each position needs to have a number
    for pos in P:
        s.add(Or(pos))

    # Each position can only have *one* number
    for i in range(guess_len):
        for j in range(10 - 1):
            for k in range(j + 1, 10):
                s.add(Implies(P[i][j], Not(P[i][k])))

    build_time = time.time() - start_time
    print(f"Board len = {guess_len}", file=sys.stderr)
    print(f"Guess num = {len(B) // 3}", file=sys.stderr)
    print(f"formula building time = {build_time:.4f}s", file=sys.stderr)

    start_solve_time = time.time()

    solutions = []
    print_once = 1
    while s.check() == sat:
        
        if print_once:
            print(print_once * f"first solving time = {time.time() - start_solve_time:.4f}s", file=sys.stderr)
            print_once = 0
        
        m = s.model()
        candidates = [p.name() for p in m.decls() if m[p]]

        solutions.append(convert(candidates))

        block = [p() != m[p] for p in m.decls()]
        s.add(Or(block))

    print(f"total solving time = {time.time() - start_solve_time:.4f}s", file=sys.stderr)
    return solutions


def unique_solution2(B):
    return len(mastermind2(B)) == 1


# Boards = [

# ]

# for b in Boards:
#     print(mastermind2(b))

# board_10 = [
#     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 10, 0,
#     [0, 1, 2, 3, 4, 5, 6, 7, 9, 8], 8, 2,
# ]

# print(mastermind2(board_10))


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

# NOTE: This two examples are the same as almost_mastermind. Just seeing if this works
# with no white pegs
B2 = [
    [9, 0, 3, 4, 2],
    2,
    0,
    [7, 0, 7, 9, 4],
    0,
    0,
    [3, 9, 4, 5, 8],
    2,
    0,
    [3, 4, 1, 0, 9],
    1,
    0,
    [5, 1, 5, 4, 5],
    2,
    0,
    [1, 2, 5, 3, 1],
    1,
    0,
]

B3 = [
    [5, 6, 1, 6, 1, 8, 5, 6, 5, 0, 5, 1, 8, 2, 9, 3],
    2,
    0,
    [3, 8, 4, 7, 4, 3, 9, 6, 4, 7, 2, 9, 3, 0, 4, 7],
    1,
    0,
    [5, 8, 5, 5, 4, 6, 2, 9, 4, 0, 8, 1, 0, 5, 8, 7],
    3,
    0,
    [9, 7, 4, 2, 8, 5, 5, 5, 0, 7, 0, 6, 8, 3, 5, 3],
    3,
    0,
    [4, 2, 9, 6, 8, 4, 9, 6, 4, 3, 6, 0, 7, 5, 4, 3],
    3,
    0,
    [3, 1, 7, 4, 2, 4, 8, 4, 3, 9, 4, 6, 5, 8, 5, 8],
    1,
    0,
    [4, 5, 1, 3, 5, 5, 9, 0, 9, 4, 1, 4, 6, 1, 1, 7],
    2,
    0,
    [7, 8, 9, 0, 9, 7, 1, 5, 4, 8, 9, 0, 8, 0, 6, 7],
    3,
    0,
    [8, 1, 5, 7, 3, 5, 6, 3, 4, 4, 1, 1, 8, 4, 8, 3],
    1,
    0,
    [2, 6, 1, 5, 2, 5, 0, 7, 4, 4, 3, 8, 6, 8, 9, 9],
    2,
    0,
    [8, 6, 9, 0, 0, 9, 5, 8, 5, 1, 5, 2, 6, 2, 5, 4],
    3,
    0,
    [6, 3, 7, 5, 7, 1, 1, 9, 1, 5, 0, 7, 7, 0, 5, 0],
    1,
    0,
    [6, 9, 1, 3, 8, 5, 9, 1, 7, 3, 1, 2, 1, 3, 6, 0],
    1,
    0,
    [6, 4, 4, 2, 8, 8, 9, 0, 5, 5, 0, 4, 2, 7, 6, 8],
    2,
    0,
    [2, 3, 2, 1, 3, 8, 6, 1, 0, 4, 3, 0, 3, 8, 4, 5],
    0,
    0,
    [2, 3, 2, 6, 5, 0, 9, 4, 7, 1, 2, 7, 1, 4, 4, 8],
    2,
    0,
    [5, 2, 5, 1, 5, 8, 3, 3, 7, 9, 6, 4, 4, 3, 2, 2],
    2,
    0,
    [1, 7, 4, 8, 2, 7, 0, 4, 7, 6, 7, 5, 8, 2, 7, 6],
    3,
    0,
    [4, 8, 9, 5, 7, 2, 2, 6, 5, 2, 1, 9, 0, 3, 0, 6],
    1,
    0,
    [3, 0, 4, 1, 6, 3, 1, 1, 1, 7, 2, 2, 4, 6, 3, 5],
    3,
    0,
    [1, 8, 4, 1, 2, 3, 6, 4, 5, 4, 3, 2, 4, 5, 8, 9],
    3,
    0,
    [2, 6, 5, 9, 8, 6, 2, 6, 3, 7, 3, 1, 6, 8, 6, 7],
    2,
    0,
]


print(mastermind2(B1))
print(mastermind2(B2))
# print(mastermind2(B3))
# print(mastermind2([[1,2,3], 1, 1]))