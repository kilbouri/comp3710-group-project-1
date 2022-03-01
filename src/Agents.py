# from msilib.schema import Error
from random import uniform
from Utility import endsWith
from collections import defaultdict


class Agent:
    # An "empty" agent which serves as the base of all other agents
    def __init__(self, memorySize: int = 3) -> None:
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

    def reset(self):
        self.fitness = 0
        self.memory = []

    def __str__(self) -> str:
        return f"{self.name} Agent"


class RandomAgent(Agent):
    # An agent which picks a random move on each turn
    def __init__(self, memorySize, defectProbability: int = 0.5) -> None:
        super().__init__(memorySize)
        self.name = "Random"
        self.defectProbability = defectProbability

    def choose(self) -> int:
        return int(uniform(0, 1) >= self.defectProbability)


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


searchMethods = ['crossover', 'random']

class GeneticAgent(Agent):
    def __init__(self, memorySize, ruleset: str = None) -> None:
        # ruleset can be either str or list[int]
        super().__init__(memorySize)
        self.name = f"Genetic"
        self.memorySize = memorySize
        self.ruleset = ruleset
        if isinstance(self.ruleset, str):
            self.ruleset = [{'C':0, 'D':1}[c] for c in self.ruleset]
        # self.rulefreq = defaultdict(int) # keep track of frequency of each move
        # self.rulehist = []
        if self.ruleset is None:
            self.ruleset = [round(uniform(0, 1))
                            for _ in range(2 ** memorySize + memorySize)]
        if (2 ** memorySize + memorySize) != len(self.ruleset):
            raise ValueError(
                "Ruleset does not cover all (or covers too many) possible memory states")

    def reproduce(self, search:str='random', partner:Agent=None) -> None:
        # two parents produce a child, child inherits more genes from fitter parent, up to 80% favoritism
        if search == 'crossover':
            assert(self.memorySize == partner.memorySize and isinstance(partner, Agent))
            if partner.fitness == 0:
                partner.fitness = 1
            rs = [c[int(uniform(0, 1) > max(min(self.fitness / partner.fitness, 0.8), 0.2))]
                  for c in zip(self.ruleset, partner.ruleset)]
        elif search == 'random': # if partner is None, then this is a reproduction with one parent, using a mutation rate
            mutationRate = 0.1
            rs = [rule if uniform(0, 1) > mutationRate else int(not rule) for rule in self.ruleset]
        else:
            raise ValueError("Invalid search type")
        return GeneticAgent(self.memorySize, rs)

    def choose(self) -> int:
        if len(self.memory) < self.memorySize:
            # first few moves, use the sequence at the end of ruleset
            move = self.ruleset[len(self.ruleset) -
                                self.memorySize + len(self.memory)]
        else:
            move = self.ruleset[int("".join(map(str, self.memory)), 2)]
            # self.rulefreq[move] += 1
        # self.rulehist.append(move)
        return move

    def reset(self):
        # here for if I want to add extra stuff to reset
        super().reset()
        # self.rulefreq = defaultdict(int)
        # self.rulehist = []