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
Training against Tit For Tat opponents |################################| 100/100
fittest ruleset is CDDCCCCCCCC
average ruleset is DDDCDDCCCDC
Average score for A: 7.0
Average score for B: 1752.0
```

Although the fittest ruleset is more 'fit', since it cooperates almost every time, the average ruleset *dominates* the game, since it defects more often.

It should also be noted that the mutation rate is 100%, so further testing will be necessary. The current mutation algorithm is much too erratic.
