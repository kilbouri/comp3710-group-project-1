from Agents import Agent
from pprint import pprint

# game class to run a game between two agents
REWARD_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)]
]
choiceMap = {
    1: "defect",
    0: "cooperate"
}

def mean(_: list) -> float:
    return sum(_) / len(_)

def moves(agentA, agentB, numSteps):
    for _ in range(numSteps):
        aChoice = agentA.choose()
        bChoice = agentB.choose()
        yield aChoice, bChoice

class Game:
    # Contains relevant functions to run a game between two agents
    def __init__(self, agentA: Agent, agentB: Agent, gameLength: int, debug: bool = False):
        self.agentA = agentA
        self.agentB = agentB
        self.numSteps = gameLength
        self.debug = debug

    def play(self):
        for aChoice, bChoice in moves(self.agentA, self.agentB, self.numSteps):
            self.agentA.updateMemory(bChoice)
            self.agentB.updateMemory(aChoice)
            aReward = REWARD_TABLE[aChoice][bChoice][0]
            bReward = REWARD_TABLE[aChoice][bChoice][1]
            self.agentA.fitness += aReward
            self.agentB.fitness += bReward

            if self.debug:
                pprint(f"A chose to {choiceMap[aChoice]} and received {aReward} points.")
                pprint(f"B chose to {choiceMap[bChoice]} and received {bReward} points.")
                print()

        return self.agentA.fitness, self.agentB.fitness

class Batch:
    # Class for batch testing will:

    # Initialize with two agent class types as parameters, as well as the game length in turns and the total number of games
    # Run N games between the two, recording the results of each game
    # Return a tuple, containing the average (fitness) score of each agent across the batch

    def __init__(self, classA, classB, gameLength:int=50, numGames:int=50, memorySize:int=3):
        self.classA = classA
        self.classB = classB
        self.gameLength = gameLength
        self.numGames = numGames
        self.memorySize = memorySize
        self.fitnessA = []
        self.fitnessB = []

    def run(self):
        for _ in range(self.numGames):
            agentA = self.classA(self.memorySize)
            agentB = self.classB(self.memorySize)
            game = Game(agentA, agentB, self.gameLength)
            fitnessA, fitnessB = game.play()
            self.fitnessA.append(fitnessA)
            self.fitnessB.append(fitnessB)
        return mean(self.fitnessA), mean(self.fitnessB)
