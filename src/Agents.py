# from msilib.schema import Error
from random import uniform
from Utility import endsWith


class Agent:
    # An "empty" agent which serves as the base of all other agents
    def __init__(self, memorySize: int) -> None:
        self.name = "Empty"
        self.memory: list[int] = []
        self.memorySize: int = memorySize
        self.fitness: int = 0

    def choose(self) -> int:
        # choose should be overloaded
        pass

    def updateMemory(self, opponentMove: int):
        if len(self.memory) >= self.memorySize:
            self.memory.pop(0)  # remove first element
        self.memory.append(opponentMove)

    def __str__(self) -> str:
        return f"{self.name} Agent"


class RandomAgent(Agent):
    # An agent which picks a random move on each turn
    def __init__(self, memorySize, defectProbability: int = 0.5) -> None:
        super().__init__(memorySize)
        self.name = "Random"
        self.defectProbability = defectProbability

    def choose(self) -> int:
        return uniform(0, 1) >= self.defectProbability


class CooperativeAgent(Agent):
    # An agent which always cooperates
    def __init__(self, memorySize) -> None:
        super().__init__(memorySize)
        self.name = "Cooperative"

    def choose(self) -> int:
        return 0


class DefectiveAgent(Agent):
    # An agent which always defects
    def __init__(self, memorySize) -> None:
        super().__init__(memorySize)
        self.name = "Defective"

    def choose(self) -> int:
        return 1


class TFTAgent(Agent):
    # An agent which picks a tit for tat move on each turn
    # first move, always cooperate
    # choose opponent's last move as next move
    def __init__(self, memorySize) -> None:
        super().__init__(memorySize)
        self.name = "Tit For Tat"

    def choose(self) -> int:
        return 0 if len(self.memory) == 0 else self.memory[-1]


class TFNTAgent(Agent):
    # An agent which picks a tit for N tat move on each turn
    # first two moves, always cooperate
    # if the opponent defects twice in a row, defect
    # 0 is cooperate, 1 is defect
    def __init__(self, memorySize, tatLength=2) -> None:
        super().__init__(memorySize)
        self.name = f"Tit For {tatLength} Tat"
        self.tatLength = tatLength

    def choose(self) -> int:
        return int(endsWith([1] * self.tatLength, self.memory))


class STFTAgent(Agent):
    # defects on first move, then duplicates the opponent's last move
    def __init__(self, memorySize) -> None:
        super().__init__(memorySize)
        self.name = "Suspicious Tit For Tat"

    def choose(self) -> int:
        return 1 if len(self.memory) == 0 else self.memory[-1]


class PavlovAgent(Agent):
    # Conditions opponent to cooperate, then betrays them
    def __init__(self, memorySize: int, pavLength: int = 3) -> None:
        super().__init__(memorySize)
        self.name = "Pavlov"
        self.pavLength = pavLength

    def choose(self) -> int:
        if len(self.memory) < self.pavLength:
            return 0

        return int(not endsWith([0] * self.pavLength, self.memory))


# class GeneticAgent(Agent):
#     # Uses a custom ruleset by indexing a bit string with
#     # the binary number represented by the memory state
#     # TODO: need to keep track of own previous moves, as well as opponent's
#     # TODO: Create a mutator constructor, that makes some change to the ruleset
#     # TODO: rename 'ruleset' to 'chromosome'?
#     # TODO: Create a fitness function (just return score)
#     # TODO: need a way to encode move history into an integer to read from chromosome/ruleset
#     def __init__(self, memorySize: int, ruleset: str) -> None:
#         super().__init__(memorySize)
#         self.ruleset = ruleset
#         self.name = f"Ruleset '{ruleset}'"

#         if (2 ** memorySize - 1) != len(ruleset):
#             raise Error("Ruleset does not cover all (or covers too many) possible memory states")

#     def choose(self) -> int:
#         idx = int("".join(self.memory), 2)
#         return int(self.ruleset[idx])
