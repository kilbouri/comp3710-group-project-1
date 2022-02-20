from Agents import Agent


def moves(agentA, agentB, numSteps):
    for _ in range(numSteps):
        aChoice = agentA.choose()
        bChoice = agentB.choose()

        yield aChoice, bChoice

# game class to run a game between two agents


GAME_LENGTH = 4
MEMORY_SIZE = 4
REWARD_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)]
]


class Game:
    def __init__(self, agentA: Agent, agentB: Agent):
        self.agentA = agentA
        self.agentB = agentB
        self.numSteps = GAME_LENGTH

    def play(self):
        for aChoice, bChoice in moves(self.agentA, self.agentB, self.numSteps):
            self.agentA.updateMemory(bChoice)
            self.agentB.updateMemory(aChoice)
            self.agentA.fitness += REWARD_TABLE[aChoice][bChoice][0]
            self.agentB.fitness += REWARD_TABLE[bChoice][aChoice][1]

        return self.agentA.fitness, self.agentB.fitness
