# Subset Sum Implementation

`Infector.limited_infection` is implemented using a solver for the subset sum optimization problem.  A vital choice is the implementation that is chosen to solve the subset sum problem.  This document explores the available implementation choices and provides a rational for the selected algorithm

## Basic Context
The subset sum problem is given a set of integers and a value find a subset of the original set that sums to the target value.

For the `Feature Infection` project, we are interested in a slightly different version of the problem called the subset sum optimization problem (SSO).  Given the set and a target, find a subset with a maximal sum not exceeding the target value.  The initial set is restricted to contain natural numbers instead of all integers.

SSO belongs to the `NP-Complete` algorithm class, so there doesn't exist an exact solution that runs in polynomial time.  

## Solution Space

Algorithm options
Exact
Psudo-polynomial Time
Fully-Polynomial Time Approximation Solutions
Heuristic

## Timing Data


## Conclusions

Greedy is good enough.  And the fastest.