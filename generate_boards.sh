#!/bin/bash

f=20

for len in `seq 4 1 9`
do
    outfile=boards/"boards_increasing_len_guess_$f"
    echo "Create board of with len of $len and $f guesses"
    python3 chat_board_generator.py "$f" "$len" >> "$outfile"
    echo "generation done len = $len, guess num = $f"
done

