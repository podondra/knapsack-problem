# Knapsack Problem

## 0-1 Knapsack Problem

Given whole number $n$ (number of things), whole number *M* (knapsack capacity),
finite set *W = {w_1, w_2, ... , w_n}* (things' weights),
finite set *C = {c_1, c_2, ... , c_n}* (things' price).
Construct set *X = {x_1, x_2, ... , x_n}* where all *x_i in {0, 1}*,
so that *w_1 x_1 + w_2 x_2 + ... + w_n x_n <= M*
(knapsack is not overloaded)
and expression *c_1 x_1 + c_2 x_2 + ... + c_n x_n* is maximal for all such sets
(price of things in knapsack is maximal).

## Report Build

1. download the notebook as TeX
2. use `pdflatex` to produce PDF
3. use `git archive -o <HW-NAME>.zip --prefix=<HW-NAME>/ HEAD`
