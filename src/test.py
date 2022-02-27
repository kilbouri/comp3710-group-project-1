from game import Game, Batch, mean, REWARD_TABLE
from Agents import *
from compare import Comparison, Population
from pandas import DataFrame
import csv
from os import path
from train import agentStrings

# import a trained agent
def trainedAgent(Opponent:str, csvpath:str, nParents:int=2, memSize:int=6, Fittest:bool=True) -> GeneticAgent:
    # singleTrained: bool, if true, use single reproduction trained agent
    # memSize: int, memory size of agent
    # fittest: bool, if true, use fittest chromosome, if false, use average chromosome
    # csvpath: str, path to csv file containing training results

    if not path.exists(csvpath):
        raise FileNotFoundError(f'Training results file not found at {csvpath}')
    with open(csvpath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # find the row with training data that fits the parameters (memSize, fittest/avg, singleTrained)
        for row in reader:
            if row[0] == Opponent and row[3] == str(memSize) and row[7] == str(nParents):
                if Fittest:
                    ruleset = row[1]
                else:
                    ruleset = row[2]
    
    return GeneticAgent(memSize, ruleset)

def compareGAs():
    pass
