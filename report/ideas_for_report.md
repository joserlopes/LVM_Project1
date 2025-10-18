# Report

## CDCL - exercise 1
![cdcl-1](../images/cdcl-1.jpg)
![cdcl-2](../images/cdcl-2.jpg)

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

If there are no black pegs, we negate the numbers at the current guess's position.

Let $a_i$ be the number at the position $i$ of a given guess, where $i = 1, ..., n$

$\bigwedge_{k=1}^{n} \neg p_{a_{i}k}$

Else, let $b$ be the number of black pegs for a given guess. We need to consider all possible groups of $b$ size, without repetition.
We get a total of $B = \frac{n!}{b!(n-b)!}$ sets of $b$ size. These sets have, at most, $n$ elements, if $b = n$
Each of these sets will contain the possible positions with the correct numbers.
let $P_{l}$ be such a set, with $l = 1, ..., b$ and $NP_{l}$ the complement of $P_{l}$. e.g. if $n = 4$, $b=3$ and $P_{1} = \{1, 2, 3\}$, 
then $NP_{1} = \{4\}$


$\bigvee_{l=1}^{B} \bigwedge_{\substack{  c \in P_{l}  \\ q \in NP_{l}} } p_{a_{c}c} \wedge \neg p_{a_{c}q}$

#### Full Mastermind - exercise 2.2

Let $w$ be the number of white pegs for a given guess. 
For each combination (i.e. the set $P_{l}$ with the positions we consider to have the correct number),
the number of sets that contain the possible white positions on the guess 

$W = \frac{(n-b)!}{w!((n-b)-w)!}$

This is because there's no need to consider positions that we are assuming to be correct for the current combination (stored in $P_{l}$)

Let $WP_{m}, m = 1, ..., W$ be sets of positions on the guess, where the size of each $WP_{m} = w$ (WP for wrong position).

And so, for each black combination, and for each white combination, we need to consider all permutations of positions
,which can be positions present in $WP_{m}$. for example, we can have a 2 in position 1 and a 3 in position 2 that are not in the code,
but if those positions are white (that is, in $WP_{m}$) 3 can be at position 1 and 2 at position 2.

Then, the number of possible permutations is $Perm = (n-b)! / ((n-b) - w)!$, and again, let $V_{z}, z = 1, ..., Perm$ be the sets that have 
all possible permutations of possible positions where the number indexed by $WP_{m}$ can be, to match the secret code

And finally we can right the encoding as such:

$\bigvee_{l=1}^{B} \bigvee_{m=1}^{W} \bigvee_{z=1}^{Perm} (\bigwedge_{\substack{  c \in P_{l}  \\ q \in NP_{l}} } p_{a_{c}c} \wedge \neg p_{a_{c}q} \bigwedge_{\substack{d \in WP_{m} \\ e \in V_{z}} } \neg p_{a_{d}d} \wedge p_{a_{d}e})$



### graphs

#### increasing guess number

We tested independentely two variables, number of guesses and size of a guess (which we call board len)

![len6](./guess_inc_len6.png)
![len7](./guess_inc_len7.png)
![len8](./guess_inc_len8.png)

Increasing the number of guesses increases the formula building time somewhat linearly. the spikes in time are, as expected, related to the bigger porpotion of white pegs in relation to black pegs

We see the same pattern for boards with len of 9, but for the same number of guesses, each building is much much bigger

![len9](./guess_inc_len9.png)


If we now increase the len of boards, but with the same guess number, we see a sharp rise in the time it takes to construct a formula

![guess20](./len_inc.png)

This is because we consider all permutations for possible places for the white pegs, for each combination of black pegs. This corresponds to the complexity of our encoding being factorial.

