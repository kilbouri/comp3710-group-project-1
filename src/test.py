from game import *
from Agents import *
from compare import Comparison, Population
from pandas import DataFrame
import csv
from os import path

columns = ['GA','Opponent', 'Ruleset', 'memSize', 'search', 'GAscore', 'opponentscore']

# import a trained agent
def trainedAgent(Opponent:str, csvpath:str, search:str, memSize:int=6, Fittest:bool=True) -> GeneticAgent:
    # search: str, search method used to train
    # memSize: int, memory size of agent
    # fittest: bool, if true, use fittest chromosome, if false, use average chromosome
    # csvpath: str, path to csv file containing training results

    if not path.exists(csvpath):
        raise FileNotFoundError(f'Training results file not found at {csvpath}')
    ruleset = None
    with open(csvpath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # find the row with training data that fits the parameters (memSize, fittest/avg, singleTrained)
        for row in reader:
            if row[0] == Opponent and row[3] == str(memSize) and row[7] == search:
                if Fittest:
                    ruleset = row[1]
                else:
                    ruleset = row[2]

    return GeneticAgent(memSize, ruleset) if ruleset is not None else None

def compareGAs():
    # Take a full set of trained agents, and compare them against each other.
    csvpath = '../trainingCache.csv'
    search = 'crossover'
    memSize = 3
    fittest = True
    agents = {tp: trainedAgent(tp, csvpath, search, memSize, fittest) for tp, search in agentStrings}
    
    # TODO: compare GAs here

def testAgents():
    # test all agents in trainingCache.csv against the opponent they were trained against, and print results
    csvpath = '../trainingCache.csv'
    outpath = '../testResults.csv'

    with open(csvpath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        outfile = open(outpath, 'w')
        writer = csv.writer(outfile)
        writer.writerow(columns)
        for row in reader:
            GA, opponent, ruleset, memsize, generations, turns, games, search = row
            try:
                memsize, turns, games = map(int, [memsize, turns, games])
            except ValueError:
                print(f'Error: {row}')
                raise
            agent = agentStrings[GA](memsize, ruleset)
            opponent = agentStrings[opponent](memsize)
            print(f'{agent.name}({search}) vs {opponent}: {Game(agent, opponent, turns).play()}')
            writer.writerow([GA, opponent, ruleset, memsize, search, *Game(agent, opponent, turns).play()])
        outfile.close()


            
def main():
    testAgents()

if __name__ == '__main__':
    main()