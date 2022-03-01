# Findings from Testing

## Simple Agents

|       -        | Random//Random | Random//Tit For Tat | Random//Pavlov | Tit For Tat//Tit For Tat | Tit For Tat//Pavlov | Pavlov//Pavlov |
| -------------- | -------------- | ------------------- | -------------- | ------------------------ | ------------------- | -------------- |
| winner         | Random         | Random              | Pavlov         | TIE                      | TIE                 | TIE            |
| avg A score    | 22.7           | 23.9                | 18.7           | 30.0                     | 30.0                | 30.0           |
| avg B score    | 23.7           | 21.9                | 26.2           | 30.0                     | 30.0                | 30.0           |
| A/B avg        | 0.957806       | 1.091324            | 0.71374        | 1.0                      | 1.0                 | 1.0            |
| all identical? | False          | False               | False          | True                     | True                | True           |

## Genetic Agents

### Initial testing results on GAs

After training a population of GAs against TFT agents, two agents were created from this training data:

1. An agent with the ruleset from the highest fitness GA
2. An agent with a ruleset constructed as the average ruleset for the last population of GAs

Then, these two agents were tested against each other, with the following results:

```txt
(3 memory, 100 generations, 10 games @ 50 turns, 100 population)
Training against Tit For Tat opponents |################################| 100/100
fittest ruleset is CDDCCCCCCCC
average ruleset is DDDCDDCCCDC
Average score for A: 7.0
Average score for B: 1752.0
```

Although the fittest ruleset is more 'fit', since it cooperates almost every time, the average ruleset *dominates* the game, since it defects more often.

It should also be noted that the mutation rate is 100%, so further testing will be necessary. The current mutation algorithm is much too erratic.

### GA vs GA

Initial findings were that a small training size saw the average genome dominate the fittest one. 

```txt
(3 memory, 100 generations, 10 games @ 30 turns, 100 population)
Training against Genetic opponents |################################| 100/100
fittest ruleset is DDDCDCDCCDC
average ruleset is DDDDCCCDCDD
Average score for fittest: 352.0
Average score for average: 1232.0
```

#### More extensive testing

First test with a high number of generations

```txt
(3 memory, 500 generations, 10 games @ 64 turns, 100 population)
Training against Genetic opponents |################################| 500/500
fittest ruleset is DCDDDCCDCDD
average ruleset is DCDCCDCDDCD
Average score for fittest: 1053.6
Average score for average: 472.1
```

Test with a (much) larger memory, over 1000 generations, and 5x population size

```txt
(6 memory, 1000 generations, 10 games @ 64 turns, 500 population)
fittest ruleset is DDCDDCCDCCDDCDDDDCCDDCCCDCDCCDCDDCCDCDDDDCCCCDCDDDCDDDDCDCCCDDDDCDDDDC
average ruleset is DDCCCCCDDDCDCDCCCCDDDDCCDCCDDDDCCDCCDCDDCDDDCDDDCCDDDDCDCDDDCDDCDCDCDC
Average score for fittest: 1666.0
Average score for average: 66.0
```
