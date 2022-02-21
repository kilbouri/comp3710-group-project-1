# Compare the different agents in Agents.py, running Batches of Games in game.py

from itertools import combinations_with_replacement as cwr
from game import Batch, mean
from Agents import *
import pandas as pd
from random import randrange as rr


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
            index=['winner', 'avg A score', 'avg B score',
                   'A/B avg', 'all identical?']
        )

    def __str__(self):
        # print results in a nice table using a dataframe
        return str(self.df())


class Population:
    # class to manage, train, and test a population of genetic agents
    # only tests/trains against either itself, or one other agent type at a time
    def __init__(self, population: list = None, memorySize: int = 3, populationSize: int = 100):
        self.populationSize: int = populationSize if population is None else len(
            population)
        self.population: list[Agent] = [GeneticAgent(memorySize) for _ in range(populationSize)] if population is None else population

    def play(self, opponentType=GeneticAgent, gameLength: int = 50, numGames: int = 10):
        # For each matchup, if the opponent is a GeneticAgent, play against random other individual
        # If the opponent is a simple agent, train each agent against the simple agent

        for individual in self.population:
            batch = Batch(GeneticAgent, opponentType, gameLength, numGames)
            batch.predefinedAgents(individual, self.population[uniform(
                0, self.populationSize-1)] if opponentType == GeneticAgent else None)
            batch.run()

    def evolve(self):
        # keep top 10% of population, fill back up with offspring
        # resets recycled individuals' fitness to 0 and memory
        sorted(self.population, key=lambda x: x.fitness, reverse=True)
        samplesize = int(self.populationSize*0.1)
        newpop = self.population[:samplesize]
        while len(newpop) < self.populationSize:
            newpop.append(self.population[rr(0, samplesize)].reproduce(self.population[rr(0, samplesize)]))
        self.population = newpop
        for i in self.population[:samplesize]:
            i.reset()

    def train(self, ngens: int, opponentType=GeneticAgent, gameLength: int = 50, numGames: int = 10):
        # train the population for a number of generations
        for i in range(ngens):
            self.play(opponentType, gameLength, numGames)
            self.evolve()
