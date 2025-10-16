# Report

## CDCL - exercise 1
<!-- ![cdcl-1](../images/cdcl-1.jpg) -->
<!-- ![cdcl-2](../images/cdcl-2.jpg) -->

## Encoding - exercise 2

### variables
Let $n$ be the length of the secret code and the guesses on the board.

for $i \in \{0, 1,..., 9\}$ and $k \in \{1, 2,..., n\}$, we define the propositional symbols

$p_{ik}$ - entry at position $k$ has number $i$

### constraints

#### Each position must have at least 1 number

$\bigvee_{i = 0}^{9} \bigvee_{k=1}^{n} p_{ik}$ 

#### Each position must have at most 1 number

$\bigwedge_{k=1}^{n} \bigwedge_{i = 0}^{8} \bigwedge_{j = i+1}^{9} (\neg p_{ik} \vee \neg p_{jk})$ 

#### Almost Mastermind - exercise 2.1

if there were no black pegs, we negate the numbers at the current guess's position
let $a_i$ be the number at the position $i$ of a given guess, where $i = 1, ..., n$

$\bigwedge_{k=1}^{n} \neg p_{a_{i}k}$

Else, let $b$ be the number of black pegs. We need to consider all possible groups of $b$ size, without repetition.
We get a total of $N = \frac{n!}{b!(n-b)!}$ sets of $b$ size. These sets have, at most, $n$ elements, if $b = n$
Each of these sets will contain the possible positions with the correct numbers.
let $P_{l}$ be such a set, with $l = 1, ..., b$ and $NP_{l}$ the complement of $P_{l}$. e.g. if $n = 4$, $b=3$ and $P_{1} = \{1, 2, 3\}$, 
then $NP_{1} = \{4\}$


$\bigvee_{l=1}^{N} \bigwedge_{\substack{  p \in P_{l}  \\ q \in NP_{l}} } p_{a_{p}p} \wedge \neg p_{a_{q}q}$

Consider $A$ to be the number of positions that have the right number.