from numpy import append
from game import *
from Agents import *
from compare import Comparison, Population
from pandas import DataFrame
import csv
from os import path, remove
from sys import argv
from itertools import product
from Utility import *
from progress.bar import Bar
from progress.counter import Counter
from random import choice,randint
from collections import defaultdict

# Collection of different training functions]

columns = ['GA','Opponent', 'Fittest', 'memSize', 'nGens', 'gameLen', 'nGames', 'search']

searchMethods = ['crossover', 'random', 'exhaustive', 'hillclimbgreedy', 'hillclimbsteep', 'tabuSerach']

def exhaustive(opponents:list[str], memsize:int, csvpath:str, GA='GeneticAgent'):
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
            batch.predefinedAgents(agentStrings[GA](memsize, ruleset), None)
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
            writer.writerow([GA(3).name, agent, ruleset, memsize,'', gamelen, numgames, 'exhaustive'])

# Stochastic hill climbing
# One Genetic Agent is created with a (random) ruleset. As it plays against a agent, it ajusts its ruleset
# to a neighbor of its current ruleset (flips a random single bit) and plays against the same agent.
# The agent with the best fitness is saved as the fittest agent and continues.
# If the agent does not improve, it is discarded and a new agent is created with a random ruleset from the fittest
# agent. This process continues until the fittest agent is found(the new agent was worse than the prev).
def hillclimbgreedy(opponents:list[str], memsize:int, csvpath:str, GA='GeneticAgent'):
    # opponents is a list of simple agents to test against
    # memsize = 4

    results = {}
    bitschanged = []
    
    # test every possible string against every listed simple agent
    for agent in opponents:
        bar = Counter(f'hill climb greedy against {agentStrings[agent](3).name} opponents ')
        ruleset = ''.join({0:'C',1:'D'}[i] for i in agentStrings[GA](memsize).ruleset)
        topAgentFit = 0
        topAgentRuleset = ruleset
        changeswithoutimprovement = 0

        maxnotfound = 1
        while maxnotfound:
            bar.next()
            batch = Batch(None, agentStrings[agent], gameLength=30,numGames=5, memorySize=memsize)
            batch.predefinedAgents(agentStrings[GA](memsize, ruleset), None)
            fitnessA, fitnessB = batch.run()
            #if the agent has improved, save the ruleset and reset the counter
            if mean(fitnessA) > topAgentFit:
                topAgentFit = mean(fitnessA)
                topAgentRuleset = ruleset
                bitschanged.clear()
            #if the agent has not improved, increment the try counter
            else:
                break
            #change ruleset by flipping a random bit
            ruleset = list(ruleset)
            #check if the bit was changed already and change a new one if it was
            bit = randint(0, len(ruleset)-1)
            bitschanged.append(bit)
            ruleset[bit] = 'C' if ruleset[bit] == 'D' else 'D'
            ruleset = ''.join(ruleset)
        bar.finish()

    with open(csvpath, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for agent, ruleset in results.items():
            writer.writerow([agentStrings[GA](3).name, agent, ruleset, memsize,'', 30, 5, 'hillclimbgreedy'])


# Steepest-Ascent Hill climbing
# One Genetic Agent is created with a (random) ruleset. A population of agents is created with the neighbor ruleset.
# (A single bit is flipped in each position of the ruleset as a new agent) and all agents play against the same agent.
# The fittest agent is saved as the fittest agent and continues (with its ruleset).
# If the fittest agent does not improve, then break and return the fittest agent.
def hillclimbsteep(opponents:list[str], memsize:int, csvpath:str, GA='GeneticAgent'):
    # opponents is a list of simple agents to test against
    # memsize = 4

    results = {}
    bitschanged = []
    agentList = []
    
    # test every possible string against every listed simple agent
    for agent in opponents:
        bar = Counter(f'hill climb steep against {agentStrings[agent](3).name} opponents ')
        ruleset = ''.join({0:'C',1:'D'}[i] for i in agentStrings[GA](memsize).ruleset)
        while True:
            #add the original ruleset agent and all its neighbors to the list
            agentList.append(agentStrings[GA](memsize, ruleset))
            for n in range(agentList[-1].rslen):
                #invert the bit at the nth position
                neighbor = ruleset
                neighbor = list(neighbor)
                neighbor[n] = 'C' if neighbor[n] == 'D' else 'D'
                neighbor = ''.join(neighbor)
                agentList.append(agentStrings[GA](memsize, ''.join(neighbor)))
            #run the batch
            pop = Population(population=agentList, memorySize=memsize, populationSize=1)
            pop.play(opponentType=agentStrings[agent], gameLength=30, numGames=5)
            fittest = pop.fittestChromosome()
            #if the agent hasnt improved, break
            ruleset = ''.join(ruleset)
            if fittest == ruleset:
                results[agent] = fittest
                break
            #if the agent has improved, save the ruleset
            else:
                ruleset = fittest
                agentList.clear()
            bar.next()
        bar.finish()

    # print results
    # print results
    with open(csvpath, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for agent, ruleset in results.items():
            writer.writerow([GA, agent, ruleset, memsize,'', 30, 5, 'hillclimbsteep'])

# Tabu Search
# One Genetic Agent is created with a (random) ruleset. As it plays against a agent, it ajusts its ruleset
# to a neighbor of its current ruleset (flips a random single bit) and plays against the same agent.
# As the agent plays, the .
# If the agent does not improve, it is discarded and a new agent is created with a random ruleset from the fittest
# agent. This process continues until the fittest agent is found(until all posibilities have been tried).
def tabuSerach(opponents:list[str], memsize:int, csvpath:str, GA='GeneticAgent'):
    # opponents is a list of simple agents to test against
    # memsize = 4

    results = {}

    tabuListSize = (2**memsize+memsize)
    
    # test every possible string against every listed simple agent
    for agent in opponents:
        bar = Counter(f'tabu search against {agentStrings[agent](3).name} opponents ')
        ruleset = ''.join({0:'C',1:'D'}[i] for i in agentStrings[GA](memsize).ruleset)
        topAgentFit = 0
        topAgentRuleset = ruleset
        changeswithoutimprovement = 0

        tabuSerach = []

        maxnotfound = 1
        while maxnotfound:
            bar.next()
            tabuSerach.append(agentStrings[GA](memsize, ruleset))
            batch = Batch(None, agentStrings[agent], gameLength=30,numGames=5, memorySize=memsize)
            batch.predefinedAgents(agentStrings[GA](memsize, ruleset), None)
            fitnessA, fitnessB = batch.run()
            #if the agent has improved, save the ruleset
            if mean(fitnessA) > topAgentFit:
                print(fitnessA)
                topAgentFit = mean(fitnessA)
                topAgentRuleset = ruleset
                changeswithoutimprovement = 0
            #if the agent has not improved, increment the try counter
            else:
                ruleset = topAgentRuleset
                changeswithoutimprovement += 1
            #if no improvement has been made for all neighbors, break
            if changeswithoutimprovement > (len(topAgentRuleset))-1:
                maxnotfound = 0
                results[agent] = topAgentRuleset
                break
            #change ruleset by flipping a random bit
            ruleset = list(ruleset)
            #check if the ruleset has already been tried and change a new one if it was
            prevrs = ruleset
            while ruleset in tabuSerach:
                ruleset = prevrs
                bit = randint(0, len(ruleset)-1)
                ruleset[bit] = 'C' if ruleset[bit] == 'D' else 'D'
            tabuSerach.append(ruleset)
            if(len(tabuSerach) > tabuListSize):
                tabuSerach.pop(0)
            ruleset = ''.join(ruleset)
        bar.finish()

    with open(csvpath, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for agent, ruleset in results.items():
            writer.writerow([agentStrings[GA](3).name, agent, ruleset, memsize,'', 30, 5, 'tabusearch'])

def bulktrain(csvpath:str, search=None, memsize:int=3, popsize:int=100, games:int=10, turns:int=64, generations:int=1000, GA='GeneticAgent'):
    # search=None will run all possible search methods
    # search=str will only run specified search method
    # search=list will run all specified search methods

    # defaults to running all methods
    if search is None:
        search = searchMethods
    if isinstance(search, list):
        for s in search:
            bulktrain(csvpath, s, memsize, popsize, games, turns, generations, GA)
        return
    if search == 'exhaustive':
        return exhaustive(list(agentStrings.keys()), memsize, csvpath, GA)
    if search == 'hillclimbgreedy':
        return hillclimbgreedy(list(agentStrings.keys()), memsize, csvpath, GA)
    if search == 'hillclimbsteep':
        return hillclimbsteep(list(agentStrings.keys()), memsize, csvpath, GA)
    if search == 'tabusearch':
        return tabuSerach(list(agentStrings.keys()), memsize, csvpath, GA)

    allAgents = list(agentStrings.keys())
    if not path.exists(csvpath):
        with open(csvpath, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
    with open(csvpath, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for agent in allAgents:
            pop = Population(memorySize=memsize, populationSize=popsize, GA=agentStrings[GA])
            pop.train(generations, opponentType=agentStrings[agent], gameLength=turns, numGames=games, search=search)
            fittest = pop.fittestChromosome()
            writer.writerow([GA, agent, fittest, memsize, generations, turns, games, search])

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
    GA = 'GeneticAgent2'

    if path.exists(csvpath):
        remove(csvpath)
    return bulktrain(csvpath, search=['crossover'], memsize=memsize, popsize=popsize, games=games, turns=turns, generations=generations, GA=GA)

def main():
    
    csvpath = '../GA2Train.csv'
    bulktrain(csvpath, search=[argv[1]], GA='GeneticAgent')
    # ['crossover', 'random', 'hillclimbgreedy', 'hillclimbSteep']
    # testtrain()
    


if __name__ == "__main__":
    main()
