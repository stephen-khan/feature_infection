# Subset Sum Implementation

`Infector.limited_infection` is implemented using a solver for the subset sum optimization problem.  A vital choice is the implementation that is chosen to solve the subset sum problem.  This document explores the available implementation choices and provides a rational for the selected algorithm.

## Basic Context
The subset sum problem is to find a subset of given a set of integers with the maximum sum not exceeding a given target value.

For the `Feature Infection` project, we are interested in a slightly different version of the problem called the subset sum optimization problem (SSO).  Given the set and a target, find a subset with a maximal sum not exceeding the target value.  The initial set is restricted to contain natural numbers instead of all integers.

SSO belongs to the `NP-Complete` algorithm class, so there does not exist an exact solution that runs in polynomial time.  

## Solution Space
### Exact Algorithm

The basic algorithm operates in `O(2**n)` space because we need to consider set membership
for each element of the set.  This is implemented in the subset_sum module as `exact`.

The `exact` implementation from the subset_sum module was excluded from the data below because there is not enough memory available to handle collecting the available subset.  The timing example program has its own implementation
of `exact` that does not find the subset, but only the subset sum value, but it is not directly comparable.

### Psudo-polynomial Time

Dynamic programming admits a psudo-polynomial solution that depends on the size of the target weight.  This algorithm operates in `O(n * W)` where `W` is the target weight.  This is implemented in the subset_sum module as `psuedopolynomial`.

### Fully-Polynomial Time Approximation Solutions

This class of algorithms provides a polynomial time algorith with a bounded error.  There are a number of schemes.  The state of the art here seems to be Keller et al (2003) that `O(min{n/error,n+1/error**2 * log(1/error)})`.
The subset_sum library implements the algorithm described at [http://www.cs.ust.hk/mjg_lib/Classes/COMP572_Fall07/Notes/SS_FPTAS.pdf](http://www.cs.ust.hk/mjg_lib/Classes/COMP572_Fall07/Notes/SS_FPTAS.pdf) as `approximation`.  This algorithm has a running time of `O(n**2 * ln(W) / error )`

### Heuristic

This class of algorithm produces a search over the solution space by estimating the value of each choice.  There are branch and bound methods, but by far the most common is a greedy algorithm taking items from largest to smallest.  This is implemented as `greedy`.  This runs in `O(n*log(n))`.

The greedy algorithm can have an error up to 1/2, so one fix is to rerun the algorithm on a decreasing subset of the input elements to force the algorithm to exclude the largest elements.  This runs in a worst case of `O(n*n)` and is implemented in the subset_sum libary as `iterated_greedy`

## Timing

Two sample timings are included in the examples folder.  The timings for each algorithm increase until a threshold duration is reached.

[Sample 1](https://github.com/stephen-khan/feature_infection/examples/timing.csv)
[Sample 2](https://github.com/stephen-khan/feature_infection/examples/timing_large.csv)

The first sample uses sample elements of uniform size up to 10.  The second sample uses sample elements of uniform size up to 1000.  The target is set at 20% of the sum of all sample in both cases

Except for the greedy algorithms, all of the algorithms perfomed significantly worse when there was a larger range of elements.  The worst decrease in performance came from the dynamic programming solution as expected.


## Conclusions

Running on input ranging from 200 to 52,428,800 (excluding algorithms when they exceeded 10 seconds) using uniform random input, all of the algorithms found the optimal average of the target.  

This implies that we are using an easy distribution for testing.  One improvement would be to test on the distribution of connected component sizes that we are operating on.  It gives us confidence, however, that all the algorithms will perform accurately enough for the feature infection package.

Looking at the timing data, included in the example package shows that the greedy algorithms are by far the fastest as expected.  According to [this interview with Sal](http://live.fastcompany.com/Event/A_QA_With_Salman_Khan) back in 2013, there were 10 million unique users a month.  The only algorithms in our package that can keep up with
that load are the greedy algorithms.

Thus our base implementation for the feature infection library is the greedy algorithm.
