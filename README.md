# Project 1

## Requirements

Submit a complete technical report on a project about the Iterated Prisoners’ Dilemma that will be presented during the class.

## Implementation Considerations

### Reward Table

| p1 \\ p2  | cooperate | defect |
| --------- | --------- | ------ |
| cooperate | 3, 3      | 0, 5   |
| defect    | 5, 0      | 1, 1   |

### Example strategy analysis

- Three strategies analyzed:
  - ALL-D: always defect, optimizes individual fitness
  - ALL-C: always cooperate, optimizes population fitness
  - RAND: randomly chooses between defect and cooperate
- Expected scores from this analysis:

| playing | ALL-C | RAND | ALL-D | Average |
| ------- | ----- | ---- | ----- | ------- |
| ALL-C   | 3.0   | 1.5  | 0.0   | 1.5     |
| RAND    | 4.0   | 2.25 | 0.5   | 2.25    |
| ALL-D   | 5.0   | 3.0  | 1.0   | 3.0     |

_\*\*We will initially perform an analysis similar to this one with some non-genetic simple agents_

### Genetic Algorithms

- Uses a darwinism model
- Each entity has a fitness function
- Each generation selects the most fit individuals to reproduce
- Each reproduction produces a new generation with some mutations, traits of predecessors MUST be passed on
- Over time, the population will evolve to be more fit

#### Genetic Algorithms and the Prisoner's Dilemma

- Population of 100 individuals
- Chromosome is a 64-bit string representing the strategy of the individual
- A bit is a choice depending on cooperate or defect played for a specific configuration of past moves

How do you encode a strategy with a string?

Suppose memory depth is only 1. Then, there are only four choices, based on previous moves:

| Memory | A   | B   |
| ------ | --- | --- |
| Case 0 | C   | C   |
| Case 1 | D   | C   |
| Case 2 | C   | D   |
| Case 3 | D   | D   |

Now, using 3 previous moves, suppose the memory is this:

| Memory | A   | B   | Code |
| ------ | --- | --- | ---- |
| Move 1 | C   | C   | R    |
| Move 2 | D   | C   | T    |
| Move 3 | C   | D   | R    |

(RTR = 010 = 5) (I don't get this part but we can just use opponent moves probably)

** Bit string must be `2 ** MEMLEN + MEMLEN` long; last MEMLEN bits are reserved for the first few moves.

### GA’s and PD

- Fitness: Each player competes against every
  other for 64 consecutive rounds, and a
  cumulative score is maintained
- Selection: Roulette Wheel selection
- Reproduction: Random point crossover with
  replacement
- Mutation rate 0.001
- **Generations: 1,000 generations**

## Simple Agent Types

- Tit for tat (TFT)
  - First move, cooperate
  - Always choose opponent's last move as next move
- Tit for Two Tat (TFT2)
  - First two moves, cooperate
  - If the opponent defects twice in a row, choose defection as the next move
- Suspicious Tit for Tat (STFT)
  - First move, defect
  - Always choose opponent's last move as next move
- Free Rider (ALL-D)
  - ALWAYS defect
- Always Cooperate (ALL-C)
  - Must I say any more

## Details Contents

You will form groups of 3 or 4.

## Final technical report (6-8 pages) due Feb 28<sup>th</sup>; make sure to include the following sections

- Abstract (150-200 words summarizing your work and highlight your findings)
- Introduction (general overview, motivation, your contribution)
- Relevant Literature Review
- Experimental setup and methodology, discussion of your findings
- Concluding remarks with a brief future work section
- References
- Appendix containing all extra materials used
