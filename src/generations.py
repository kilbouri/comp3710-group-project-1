from Agents import *
# we need a way to keep track of the generations

# NOTE: requires to be at least 3 memory
MEMSIZE = 3


class world:
    def __init__(self, initialpool: list):
        self.theboys: list = initialpool
        self.generation = 0
        self.max_generations = 100

    def next_generation(self):
        # take the top ten percent of the population by fitness
        self.generation += 1
        # self.theboys = self.theboys.copy()
        self.theboys = sorted(self.theboys, key=lambda x: x.fitness, reverse=True)
        self.theboys = self.theboys[:int(len(self.theboys) * 0.1)]
