# Generating one satisfiable Mastermind board
import random
import sys

n = int(sys.argv[1])
size = int(sys.argv[2])
def mastermind_feedback(secret, guess):
    correct_position = sum(s == g for s, g in zip(secret, guess))
    secret_counts = {}
    guess_counts = {}
    for s, g in zip(secret, guess):
        if s != g:
            secret_counts[s] = secret_counts.get(s, 0) + 1
            guess_counts[g] = guess_counts.get(g, 0) + 1
    correct_digit = sum(min(secret_counts.get(k, 0), guess_counts.get(k, 0)) for k in guess_counts)
    return correct_position, correct_digit

rng = random.Random()
secret = [rng.randint(0,9) for _ in range(size)]

board = []
for _ in range(n):
    guess = [rng.randint(0,9) for _ in range(size)]
    fb = mastermind_feedback(secret, guess)
    board.append([guess, fb[0], fb[1]])

# Print in the user's compact style: secret + flat list entries for the board
print("# secret code =", secret)
print(f"[")
for entry in board:
    guess, a, b = entry
    print("    {}, {}, {},".format(guess, a, b))
print("],")
