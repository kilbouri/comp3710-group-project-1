from pprint import pprint
from game import Game, Batch, mean, REWARD_TABLE
from Agents import *
from compare import Comparison, Population
from pandas import DataFrame

GAME_LENGTH = 10
MEMORY_SIZE = 3


def testGame():
    agentA = CooperativeAgent(MEMORY_SIZE)
    agentB = TFTAgent(MEMORY_SIZE)

    # scoreA = 0
    # scoreB = 0

    print(f"Starting {GAME_LENGTH}-move game...")
    print(f"Using {agentA} for A and {agentB} for B")
    print()

    scoreA, scoreB = Game(agentA, agentB, GAME_LENGTH, debug=True).play()

    # for aChoice, bChoice in moves(agentA, agentB, GAME_LENGTH):
    #     aReward, bReward = REWARD_TABLE[aChoice][bChoice]
    #     scoreA += aReward
    #     scoreB += bReward

    #     pprint(f"A chose to {choiceMap[aChoice]} and received {aReward} points.")
    #     pprint(f"B chose to {choiceMap[bChoice]} and received {bReward} points.")

    #     agentA.updateMemory(bChoice)
    #     agentB.updateMemory(aChoice)

    #     print()

    if (scoreA == scoreB):
        print(f"{agentA} and {agentB} tied")
    else:
        winner = agentA if scoreA > scoreB else agentB
        print(f"The {winner} won with a score of {max(scoreA, scoreB)}")


def testBatch():
    batch = Batch(DefectiveAgent, TFTAgent, GAME_LENGTH, numGames=10, memorySize=MEMORY_SIZE)
    aScore, bScore = batch.run()
    print(f"Average score for A: {aScore}")
    print(f"Average score for B: {bScore}")


def testCompare():
    # run one with only three agents, print result to terminal
    classes = [RandomAgent, TFTAgent, PavlovAgent]
    comp = Comparison(classes, GAME_LENGTH, numGames=10, memorySize=MEMORY_SIZE)
    comp.run()
    print(comp)

    # run again, but this time with ALL simple agents
    classes = [RandomAgent, CooperativeAgent, DefectiveAgent,TFTAgent, TFNTAgent, STFTAgent, PavlovAgent]
    comp = Comparison(classes, GAME_LENGTH, numGames=10, memorySize=MEMORY_SIZE)
    comp.run()
    # output comp dataframe to csv
    comp.df().to_csv("../simple.csv")


def testTrain():
    pop = Population(memorySize=MEMORY_SIZE, populationSize=100)
    pop.train(100, opponentType=TFTAgent)
    print(f'fittest ruleset is {pop.fittestChromosome()}')
    print(f'average ruleset is {pop.averageChromosome()}')

    # now, run a batch between the average ruleset and the fittest ruleset
    batch = Batch(None, None, gameLength=64, numGames=10)
    batch.predefinedAgents(GeneticAgent(ruleset=pop.fittestChromosome()), GeneticAgent(ruleset=pop.averageChromosome()))
    aScore, bScore = batch.run()
    print(f"Average score for fittest: {mean(aScore)}")
    print(f"Average score for average: {mean(bScore)}")

def main():
    testTrain()


if __name__ == "__main__":
    main()
