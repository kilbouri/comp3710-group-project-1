# Compare the different agents in Agents.py, running Batches of Games in game.py

from itertools import combinations_with_replacement as cwr
from game import Batch, mean
from Agents import Agent
import pandas as pd

def allsame(lst):
    # Returns True if all elements in a list are the same
    return all(x == lst[0] for x in lst)

class Comparison:
    # ONLY works with simple agents for now
    # agents passed to constructor is a list of Agent types to test between
    def __init__(self, agents: list, gameLength: int = 50, numGames: int = 10, memorySize: int = 3):
        self.agents: list[Agent] = agents
        self.gameLength: int = gameLength
        self.numGames: int = numGames
        self.memorySize: int = memorySize
        self.results: dict = {}

    def run(self):
        # run one batch per combination (with replacement) of agents
        for agentA, agentB in cwr(self.agents, 2):
            batch = Batch(agentA, agentB, self.gameLength,
                          self.numGames, self.memorySize)
            resultA, resultB = batch.run()
            self.results[(agentA(self.memorySize).name, agentB(
                self.memorySize).name)] = [resultA, resultB]

        return self.results

    def __calcmeans(self):
        # return a dict where result values are means instead of lists
        return {
            key: [mean(value[0]), mean(value[1])]
            for key, value in self.results.items()
        }

    def df(self):
        # print(self.__calcmeans())
        # return results in a (formatted) dataframe
        return pd.DataFrame(
            {
                '//'.join(c):
                [
                    c[0] if m[0] > m[1] else c[1] if m[1] > m[0] else 'TIE',
                    m[0],
                    m[1],
                    'inf' if m[1] == 0 else round(m[0]/m[1], 2),
                    allsame(self.results[c][0]) and allsame(self.results[c][1])
                ]
                for c, m in self.__calcmeans().items()
            },
            index=['winner', 'avg A score', 'avg B score', 'A/B avg', 'all identical?']
        )

    def __str__(self):
        # print results in a nice table using a dataframe
        return str(self.df())
