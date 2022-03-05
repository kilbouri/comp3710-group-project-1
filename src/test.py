from game import Game, Batch, mean, REWARD_TABLE
from Agents import *
from compare import Comparison, Population
from pandas import DataFrame
import csv
from os import path
from train import agentStrings

# import a trained agent
def trainedAgent(Opponent:str, csvpath:str, search:str, memSize:int=6, Fittest:bool=True) -> GeneticAgent:
    # search: str, search method used to train
    # memSize: int, memory size of agent
    # fittest: bool, if true, use fittest chromosome, if false, use average chromosome
    # csvpath: str, path to csv file containing training results

    if not path.exists(csvpath):
        raise FileNotFoundError(f'Training results file not found at {csvpath}')
    with open(csvpath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # find the row with training data that fits the parameters (memSize, fittest/avg, singleTrained)
        for row in reader:
            if row[0] == Opponent and row[3] == str(memSize) and row[7] == search:
                if Fittest:
                    ruleset = row[1]
                else:
                    ruleset = row[2]
    
    return GeneticAgent(memSize, ruleset)

def compareGAs():
    # Take a full set of trained agents, and compare them against each other.
    csvpath = '../trainingCache.csv'
    search = 'crossover'
    memSize = 6
    fittest = True
    agents = {tp: trainedAgent(tp, csvpath, search, memSize, fittest) for tp in agentStrings}
    
    # TODO: compare GAs here