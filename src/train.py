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

def exhaustive(opponents:list[str], memsize:int, csvpath:str):
    # opponents is a list of simple agents to test against

    # memsize = 3
    gamelen = 30
    numgames = 5
    results = {}
    
    # test every possible string against every listed simple agent
    for agent in opponents:
        cache = defaultdict(list)
        bar = Bar(f'exhaustive search against {agentStrings[agent](3).name} opponents', max=2 ** (2**memsize + memsize))
        for ruleset in product(['C', 'D'], repeat=(2 ** memsize + memsize)):
            bar.next()
            ruleset = ''.join(ruleset)
            batch = Batch(None, agentStrings[agent], gameLength=gamelen,numGames=numgames, memorySize=memsize)
            batch.predefinedAgents(GeneticAgent(memsize, ruleset), None)
            fitnessA, fitnessB = batch.run()
            cache[mean(fitnessA)].append(ruleset)
        bar.finish()
        results[agent] = cache[max(cache.keys())]

    # compile results, taking into account 'dont care' conditions
    results = {k:''.join([l[0] if allsame(l) else 'X' for l in zip(*v)]) for k,v in results.items()}
    if not path.exists(csvpath):
        with open(csvpath, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
    with open(csvpath, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for agent, ruleset in results.items():
            writer.writerow([agent, ruleset, '', memsize,'', gamelen, numgames, 'exhaustive'])


def bulktrain(csvpath:str, search=None, memsize:int=3, popsize:int=100, games:int=10, turns:int=64, generations:int=1000):
    # search=None will run all possible search methods
    # search=str will only run specified search method
    # search=list will run all specified search methods

    # defaults to running all methods
    if search is None:
        search = searchMethods
    if isinstance(search, list):
        for s in search:
            bulktrain(csvpath, s, memsize, popsize, games, turns, generations)
        return
    if search == 'exhaustive':
        return exhaustive([a for a in agentStrings.keys() if a != 'GeneticAgent'], memsize, csvpath)

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
            writer.writerow([agent, fittest, average, memsize, generations, turns, games, search])

def testtrain():
    # Run a set of training against each simple agent. Record the results in a csv file.
    # 1000 generations, 10 games per generation, 500 agents, 64 turns per game, 3 memory
    # This one uses single reproduction
    memsize = 3
    popsize = 30
    games = 5
    turns = 30
    generations = 100
    search = searchMethods
    csvpath = '../testTrain.csv'

    return bulktrain(csvpath, search, memsize, popsize, games, turns, generations)


def main():
    testtrain()


if __name__ == "__main__":
    main()
