#!/bin/bash

len=9

for f in `seq 12 2 20`
do
    outfile=boards/"boards_increasing_guesses_len_$len"
    echo "Create board of with len of $len and $f guesses"
    python3 chat_board_generator.py "$f" "$len" >> "$outfile"
    echo "generation done len = $len, guess num = $f"
done

