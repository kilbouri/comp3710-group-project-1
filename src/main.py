from pprint import pprint
from game import Game, Batch, mean
from Agents import *

GAME_LENGTH = 50
MEMORY_SIZE = 3
REWARD_TABLE = [
    [(3, 3), (0, 5)],
    [(5, 0), (1, 1)]
]

# choiceMap = {
#     1: "defect",
#     0: "cooperate"
# }

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

def main():
    testBatch()

if __name__ == "__main__":
    main()
