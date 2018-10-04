# Multi Armed Bandit Algorithms

Python implementation of various Multi-armed bandit algorithms like Upper-confidence bound algorithm, Epsilon-greedy algorithm and Exp3 algorithm

## Implementation Details

- Implemented all algorithms for 2-armed bandit.
- Each algorithm has time horizon T as 10000.
- Each experiment is repeated for 100 times to get mean results.
- Ploted the cummulative regret at time t against the rounds t = 1,...,T.
- Ploted the percentage of times optimal arm played against the rounds t = 1,...,T.
- Final plots are given in `Figures/` folder.

## Run and Input

- All algorithms file is given in `Code/` folder.
- Input of each algorithm is mean of first arm and mean of second arm.
- Here please note that for simplicity, I assumed that mean of first arm is greater than mean of second arm.
- To check effect of epsilon on Epsilon-greedy algorithm, I have run the epsilon-greedy algorithm for epsilon = 0.01, 0.1. 
- Figures of following problem is given in `Figures/` folder.


| Problem | Arm 1 | Arm 2 |
--- | --- | --- 
P1 | 0.9 | 0.6 
P2 | 0.9 | 0.8 
P3 | 0.55 | 0.45

