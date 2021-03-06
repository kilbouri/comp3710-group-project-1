# from msilib.schema import Error
from random import uniform, choice
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

class GeneticAgent(Agent):
    def __init__(self, memorySize, ruleset: str = None) -> None:
        # ruleset can be either str or list[int]
        super().__init__(memorySize)
        self.name = f"GeneticAgent"
        self.memorySize = memorySize
        self.ruleset = ruleset
        self.rslen = 2 ** memorySize + memorySize
        if isinstance(self.ruleset, str):
            self.ruleset = [{'C':0, 'D':1}[c] for c in self.ruleset]
        if self.ruleset is None:
            self.ruleset = [choice([0,1]) for _ in range(self.rslen)]
        if self.rslen != len(self.ruleset):
            raise ValueError(
                "Ruleset does not cover all (or covers too many) possible memory states")

    def evolvestr(self, search:str='random', partner:Agent=None) -> str:
        if search == 'crossover':
            assert(self.memorySize == partner.memorySize)
            if partner.fitness == 0:
                partner.fitness = 1
            rs = [c[int(uniform(0, 1) > max(min(self.fitness / partner.fitness, 0.8), 0.2))]
                  for c in zip(self.ruleset, partner.ruleset)]
        elif search == 'random':
            mutationRate = 0.1
            rs = [rule if uniform(0, 1) > mutationRate else int(not rule) for rule in self.ruleset]
        else:
            raise ValueError(f"Invalid search type {search}")
        return rs

    def reproduce(self, search:str='random', partner:Agent=None) -> Agent:
        return GeneticAgent(self.memorySize, self.evolvestr(search, partner))

    def choose(self) -> int:
        if len(self.memory) < self.memorySize:
            move = self.ruleset[len(self.ruleset) -
                                self.memorySize + len(self.memory)]
        else:
            move = self.ruleset[int("".join(map(str, self.memory)), 2)]
        return move

class GeneticAgent2(GeneticAgent):
    # GeneticAgent2 is a GeneticAgent, but it keeps track of both the opponent's moves, as well as its own

    def __init__(self, memorySize:int, ruleset: str = None) -> None:
        super().__init__(memorySize)
        self.name = f"GeneticAgent2"
        self.ruleset = ruleset
        self.rslen = 2 ** (2*self.memorySize) + memorySize
        if isinstance(self.ruleset, str):
            self.ruleset = [{'C':0, 'D':1}[c] for c in self.ruleset]
        if self.ruleset is None:
            self.ruleset = [choice([0,1]) for _ in range(self.rslen)]
        if self.rslen != len(self.ruleset):
            raise ValueError(
                "Ruleset does not cover all (or covers too many) possible memory states")
        self.memorySelf:list[int] = []

    def reproduce(self, search:str='random', partner:Agent=None) -> Agent:
        return GeneticAgent2(self.memorySize, self.evolvestr(search, partner))

    def choose(self) -> int:
        if len(self.memory) < self.memorySize:
            move = self.ruleset[len(self.ruleset) -
                                self.memorySize + len(self.memory)]
        else:
            self.memorySelf = self.memorySelf[-3:]
            move = self.ruleset[int("".join(map(str, self.memorySelf + self.memory)), 2)]
        self.memorySelf.append(move)
        return move

    def reset(self):
        super().reset()
        self.memorySelf = []
        


agentStrings = {
    'RandomAgent': RandomAgent,
    'CooperativeAgent': CooperativeAgent,
    'DefectiveAgent': DefectiveAgent,
    'TFTAgent': TFTAgent,
    'TFNTAgent': TFNTAgent,
    'STFTAgent': STFTAgent,
    'PavlovAgent': PavlovAgent,
    'GeneticAgent': GeneticAgent,
    'GeneticAgent2': GeneticAgent2
}