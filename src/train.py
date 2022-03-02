from game import Game, Batch, mean, REWARD_TABLE
from Agents import *
from compare import Comparison, Population
from pandas import DataFrame
import csv
from os import path
from itertools import product
from collections import defaultdict
from Utility import mean
from progress.bar import Bar

from sys import argv # DEBUG

# Collection of different training functions]

agentStrings = {
    'RandomAgent': RandomAgent,
    'CooperativeAgent': CooperativeAgent,
    'DefectiveAgent': DefectiveAgent,
    'TFTAgent': TFTAgent,
    'TFNTAgent': TFNTAgent,
    'STFTAgent': STFTAgent,
    'PavlovAgent': PavlovAgent,
    'GeneticAgent': GeneticAgent
}

columns = ['Opponent', 'Fittest', 'Average', 'memSize', 'nGens', 'gameLen', 'nGames', 'search']

def exhaustive(opponents:list[str]):
    # opponents is a list of simple agents to test against

    memsize = 4

    results = {}
    
    # test every possible string against every listed simple agent
    for agent in opponents:
        cache = defaultdict(list)
        bar = Bar(f'exhaustive search against {agentStrings[agent](3).name} opponents', max=2 ** (2**memsize + memsize))
        for ruleset in product(['C', 'D'], repeat=(2 ** memsize + memsize)):
            bar.next()
            ruleset = ''.join(ruleset)
            batch = Batch(None, agentStrings[agent], gameLength=30,numGames=5, memorySize=memsize)
            batch.predefinedAgents(GeneticAgent(memsize, ruleset), None)
            fitnessA, fitnessB = batch.run()
            cache[mean(fitnessA)].append(ruleset)
        bar.finish()
        results[agent] = cache[max(cache.keys())]

    # print results
    for agent in results:
        print(agent, ''.join([l[0] if all(l[0] == m for m in l) else 'X' for l in zip(*results[agent])]))


def bulktrain(search:str=None):
    # Run a set of training against each simple agent. Record the results in a csv file.
    # 1000 generations, 10 games per generation, 500 agents, 64 turns per game, 3 memory

    memsize = 3
    popsize = 100
    games = 10
    turns = 64
    generations = 1000
    csvpath = '../trainingCache.csv'

    # defaults to running all methods
    if search is None:
        for s in searchMethods:
            bulktrain(s)
        return
    if search == 'exhaustive':
        return exhaustive([a for a in agentStrings.keys() if a != 'GeneticAgent'])


    allAgents = list(agentStrings.keys())
    if not path.exists(csvpath):
        with open(csvpath, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
    with open(csvpath, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for agent in allAgents:
            pop = Population(memorySize=memsize, populationSize=popsize)
            pop.train(generations, opponentType=agentStrings[agent], gameLength=turns, numGames=games, search=search)
            fittest = pop.fittestChromosome()
            average = pop.averageChromosome()
            writer.writerow([agent, fittest, average, memsize, generations, turns, games, nParents])

def testtrain(search:str):
    # Run a set of training against each simple agent. Record the results in a csv file.
    # 1000 generations, 10 games per generation, 500 agents, 64 turns per game, 3 memory
    # This one uses single reproduction
    memsize = 3
    popsize = 30
    games = 5
    turns = 30
    generations = 100
    search = search
    csvpath = '../testTrain.csv'

    allAgents = list(agentStrings.keys())
    with open(csvpath, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for agent in allAgents:
            pop = Population(memorySize=memsize, populationSize=popsize)
            pop.train(generations, opponentType=agentStrings[agent], gameLength=turns, numGames=games, search=search)
            fittest = pop.fittestChromosome()
            average = pop.averageChromosome()
            writer.writerow([agent, fittest, average, memsize, generations, turns, games, search])


def main():
    exhaustive(opponents=argv[1:])


if __name__ == "__main__":
    main()
