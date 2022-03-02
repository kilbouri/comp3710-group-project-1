from scipy import rand
from game import Game, Batch, mean, REWARD_TABLE
from Agents import *
from compare import Comparison, Population
from pandas import DataFrame
import csv
from os import path
from itertools import product
from progress.counter import Counter
from random import choice,randint
from collections import defaultdict

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

# def exhaustive(opponents:list):
#     memsize = 3

#     cache = {}  # {fitness:[chromosomes]}
#     # test every possible string against every possible simple agent
#     for ruleset in product(['C', 'D'], repeat=(2 ** memsize + memsize)):
#         ruleset = ''.join(ruleset)


def bulktrain(search:str=None):
    # Run a set of training against each simple agent. Record the results in a csv file.
    # 1000 generations, 10 games per generation, 500 agents, 64 turns per game, 3 memory

    memsize = 3
    popsize = 500
    games = 10
    turns = 64
    generations = 1000
    csvpath = '../trainingCache.csv'

    # defaults to running all methods
    if search is None:
        for s in searchMethods:
            bulktrain(s)
        return
    # if search == 'exhaustive':
    #     return exhaustive([a for a in agentStrings.values() if a != GeneticAgent])


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

def testtrain(search:str=None):
    # Run a set of training against each simple agent. Record the results in a csv file.
    # 1000 generations, 10 games per generation, 500 agents, 64 turns per game, 3 memory
    # This one uses single reproduction
    memsize = 3
    popsize = 30
    games = 5
    turns = 30
    generations = 100
    search = 'crossover'
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

def hillclimbgreedy(opponents:list[str]):
    # opponents is a list of simple agents to test against

    memsize = 4

    results = {}
    bitschanged = []
    
    # test every possible string against every listed simple agent
    for agent in opponents:
        bar = Counter(f'hill climb greedy against {agentStrings[agent](3).name} opponents ')
        ruleset = [choice('CD') for _ in range(2 ** memsize + memsize)]
        ruleset = ''.join(ruleset)
        topAgentFit = 0
        topAgentRuleset = ruleset
        changeswithoutimprovement = 0

        maxnotfound = 1
        while maxnotfound:
            bar.next()
            batch = Batch(None, agentStrings[agent], gameLength=30,numGames=5, memorySize=memsize)
            batch.predefinedAgents(GeneticAgent(memsize, ruleset), None)
            fitnessA, fitnessB = batch.run()
            #if the agent has improved, save the ruleset and reset the counter
            if mean(fitnessA) > topAgentFit:
                topAgentFit = mean(fitnessA)
                topAgentRuleset = ruleset
                bitschanged.clear()
            #if the agent has not improved, increment the try counter
            else:
                ruleset = topAgentRuleset
                changeswithoutimprovement += 1
            #if no improvement has been made for all neighbors, break
            if changeswithoutimprovement > (2 ** memsize + memsize)-1:
                maxnotfound = 0
                results[agent] = topAgentRuleset
                break
            #change ruleset by flipping a random bit
            ruleset = list(ruleset)
            #check if the bit was changed already and change a new one if it was
            bit = randint(0, len(ruleset)-1)
            while bit in bitschanged:
                bit = randint(0, len(ruleset)-1)
            bitschanged.append(bit)
            ruleset[bit] = 'C' if ruleset[bit] == 'D' else 'D'
            ruleset = ''.join(ruleset)
        bar.finish()

    # print results
    for agent in results:
        print(f'{agent} {results[agent]}')


def main():
    hillclimbgreedy(agentStrings.keys())


if __name__ == "__main__":
    main()
