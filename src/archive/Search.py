from Agents import Agent


class Search:
    def __init__(self, against: Agent) -> None:
        self.name = "Empty"
        self.agentToCounter = against
        self.agents: list[Agent] = []
        self.generationsCompleted = 0
        pass

    def doGeneration(self):
        self.generationsCompleted += 1
        pass

    def top(self, count: int) -> list[Agent]:
        self.agents.sort(key=lambda a: a.fitness)
        return self.agents[-count:]

    def __str__(self) -> str:
        return f"{self.name} search (gen. {self.generationsCompleted}"


class HillClimbSearch(Search):
    def __init__(self, against: Agent) -> None:
        super().__init__(against)


class TabuSearch(Search):
    def __init__(self, against: Agent) -> None:
        super().__init__(against)
