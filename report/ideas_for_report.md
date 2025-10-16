## Encoding

### variables
for $i \in {0, 1,..., 9}$ and $k \in {1, 2,..., n}$, where $n$ is the length of the secret code and guesses, 
we define the propositional symbols

$p_{ik}$ - entry at position $k$ has value $i$

### constraints

#### Each position must have at least 1 number

$\bigvee_{i = 0}^{9} \bigvee_{k=1}^{n} p_{ik}$ 

#### Each position must have at most 1 number

$\bigwedge_{k=1}^{n} \bigwedge_{i = 0}^{8} \bigwedge_{j = i+1}^{9} p_{ik}$ 



Consider $A$ to be the number of positions that have the right number.