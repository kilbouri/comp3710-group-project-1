from Agents import Agent

# game class to run a game between two agents

REWARD_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)]
]
choiceMap = {
    1: "defect",
    0: "cooperate"
}

class Game:
    # Contains relevant functions to run a game between two agents
    def __init__(self, agentA: Agent, agentB: Agent, gameLength: int, debug: bool = False):
        self.agentA = agentA
        self.agentB = agentB
        self.numSteps = gameLength
        self.debug = debug

    def play(self):
        for aChoice, bChoice in self.__moves(self.agentA, self.agentB, self.numSteps):
            self.agentA.updateMemory(bChoice)
            self.agentB.updateMemory(aChoice)
            self.agentA.fitness += REWARD_TABLE[aChoice][bChoice][0]
            self.agentB.fitness += REWARD_TABLE[bChoice][aChoice][1]

            if debug:
                pprint(f"A chose to {choiceMap[aChoice]} and received {aReward} points.")
                pprint(f"B chose to {choiceMap[bChoice]} and received {bReward} points.")
                print()

        return self.agentA.fitness, self.agentB.fitness

    def __moves(agentA, agentB, numSteps):
        for _ in range(numSteps):
            aChoice = agentA.choose()
            bChoice = agentB.choose()
            yield aChoice, bChoice
