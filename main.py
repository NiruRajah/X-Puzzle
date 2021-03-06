import os
from os import path
from math import cos
import time as time
import random
import common
from state import State
from ucs import UniformCostSearch
from astar import Astar
from gbfs import GBFS

# inputPath="randomInput.txt"
inputPath="samplePuzzles.txt"
if path.exists("analysis.csv"):
    os.remove("analysis.csv")


def generateRandomPuzzle():
    with open("randomInput.txt", "w") as file:
        for i in range(0, 50):
            print(i)
            r = random.sample(range(8), 8)
            file.write(common.stateToString(r)+"\n")


def analysis():
    aFile = open("analysis.csv","w+")
    aFile.write("algo, totLengthOfSolution, avgLenghtOfSolution, totNoSolution, avgNoSolution, totExec, avgExec, optimality")
    file = open(inputPath,"r")
    pNum = 0
    for line in file:
        algoAnalysis(Astar(puzzleNumber=pNum, input=line, heuristic="h1"))
        
    aFile.close()


def algoAnalysis(algorithm):
    algo = algorithm
    start = time.time()
    algo.start()
    end = time.time()
    duration = end-start
    heuristic = algorithm.heuristic
    lenOfSolution = algo.solutionFile(duration)
    lenOfSearch = algo.searchFile()
    noSolution = 1
    cost = 0
    if algo.foundState is not None:
        noSolution = 0
        cost = algo.foundState.totalG

    return heuristic, lenOfSolution, lenOfSearch, noSolution, cost, duration

def runAlgorithm(algo):
    file = open(inputPath,"r")
    afile = open("analysis.csv","a")
    afile.write("\nAlgorithm, Puzzle, Cost, Length Of Solution, Length Of Search, Execution, No Solution, Optimality\n")

    goalstate1 = "1 2 3 4 5 6 7 0"
    goalstate2 = "1 3 5 7 2 4 6 0"

    totalLengthOfSolution = 0
    totalLengthOfSearch = 0
    totalNoSolution = 0
    totalCost = 0
    totalExecutionTime = 0
    counter = 0

    averageCost = averageExecutionTime = averageLengthOfSearch = averageLengthOfSolution = averageNoSolution = 0

    i = 0
    for line in file:
        lengthOfSolution = 0
        lengthOfSearch = 0
        duration = 0
        cost = 0
        analysis = None

        if algo == ucs:
            analysis = algoAnalysis(UniformCostSearch(puzzleNumber = i, initial = line.strip(), goal_state1 = goalstate1,goal_state2 = goalstate2))

        elif algo == gbfsH0:
            analysis = algoAnalysis(GBFS(num = i, input = line.strip(), heuristic="h0",  openList = [], closedList = [], goalState1=goalstate1, goalState2=goalstate2))
        
        elif algo == gbfsH1:
            analysis = algoAnalysis(GBFS(num = i, input = line.strip(), heuristic="h1",  openList = [], closedList = [], goalState1=goalstate1, goalState2=goalstate2))

        elif algo == gbfsH2:
            analysis = algoAnalysis(GBFS(num = i, input = line.strip(), heuristic="h2",  openList = [], closedList = [], goalState1=goalstate1, goalState2=goalstate2))
        
        elif algo == gbfsH3:
            analysis = algoAnalysis(GBFS(num = i, input = line.strip(), heuristic="h3",  openList = [], closedList = [], goalState1=goalstate1, goalState2=goalstate2))

        elif algo == astarH0:
            analysis = algoAnalysis(Astar(puzzleNumber = i, input = line.strip(), heuristic="h0", goalState1=goalstate1, goalState2=goalstate2, monotonic=False))
        
        elif algo == astarH1:
            analysis = algoAnalysis(Astar(puzzleNumber = i, input = line.strip(), heuristic="h1", goalState1=goalstate1, goalState2=goalstate2, monotonic = False))
        
        elif algo == astarH2:
            analysis = algoAnalysis(Astar(puzzleNumber = i, input = line.strip(), heuristic="h2", goalState1=goalstate1, goalState2=goalstate2, monotonic=True))
        
        elif algo == astarH3:
            analysis = algoAnalysis(Astar(puzzleNumber = i, input = line.strip(), heuristic="h3", goalState1=goalstate1, goalState2=goalstate2, monotonic=False))

        duration = analysis[5]
        lengthOfSolution = analysis[1]
        lengthOfSearch = analysis[2]
        
        if analysis[3] == 0:
            cost = analysis[4]
            counter = counter + 1
        totalCost = totalCost+cost
        totalExecutionTime = totalExecutionTime + duration
        totalLengthOfSearch = totalLengthOfSearch + lengthOfSearch
        if lengthOfSolution != 0:
            totalLengthOfSolution = totalLengthOfSolution + lengthOfSolution
        else:
            totalNoSolution = totalNoSolution + 1

        afile.write(algo +", "+ str(i)+", "+str(cost)+", "+str(lengthOfSolution)+", "+str(lengthOfSearch)+", "+str(duration)+","+str(analysis[3])+",,"+line.strip()+"\n")
        i = i + 1

    afile.write("Total-"+algo+", , "+str(totalCost)+","+str(totalLengthOfSolution)+", "+str(totalLengthOfSearch)+", "+str(totalExecutionTime)+","+str(totalNoSolution)+"\n")

    if(i != 0 and counter != 0):
        averageCost = totalCost/counter
        averageExecutionTime = totalExecutionTime/counter
        averageLengthOfSearch = totalLengthOfSearch/i
        averageLengthOfSolution = totalLengthOfSolution/counter
        averageNoSolution = totalNoSolution/i

    afile.write("Average-"+algo+", , "+str(averageCost)+","+str(averageLengthOfSolution)+", "+str(averageLengthOfSearch)+", "+str(averageExecutionTime)+","+str(averageNoSolution)+"\n")
    file.close()
    afile.close()

ucs = "ucs"
gbfsH0 = "gbfsH0"
gbfsH1 = "gbfsH1"
gbfsH2 = "gbfsH2"
gbfsH3 = "gbfsH3"
astarH0 = "astarH0"
astarH1 = "astarH1"
astarH2 = "astarH2"
astarH3 = "astarH3"

print("Welcome to X-Puzzle")
choice = ''; 
# inputPath = "randomInput.txt"
while choice != 'q':
    print("\nMake sure the samplePuzzles.txt file is the main directory ")
    print("\n[1] Enter 1 to solve the puzzle using uniform cost search. ")
    print("[2] Enter 2 to solve the puzzle using greedy best first search with h0. (Given Heuristic)")
    print("[3] Enter 3 to solve the puzzle using greedy best first search with h1. (Hamming Distance)")
    print("[4] Enter 4 to solve the puzzle using greedy best first search with h2. (Custom Manhattan)")
    print("[5] Enter 5 to solve the puzzle using greedy best first search with h3. (Sum of Permutation)")
    print("[6] Enter 6 to solve the puzzle using A* with h0. (Given Heuristic)")
    print("[7] Enter 7 to solve the puzzle using A* with h1. (Hamming Distance) uses monotonic method")
    print("[8] Enter 8 to solve the puzzle using A* with h2. (Custom Manhattan)")
    print("[9] Enter 9 to solve the puzzle using A* with h3. (Sum of Permutation)")
    print("[10] Enter 10 to run analysis on all search methods with h1, h2 as heuristics using samplePuzzle.txt ")
    print("[q] Enter q to quit. ")

    choice = input("\nHow would you like to solve the puzzle? ")

    if choice == '1':
        runAlgorithm(ucs)
    elif choice == '2':
        runAlgorithm(gbfsH0)
    elif choice == '3':
        runAlgorithm(gbfsH1)
    elif choice == '4':
        runAlgorithm(gbfsH2)
    elif choice == '5':
        runAlgorithm(gbfsH3)
    elif choice == '6':
        runAlgorithm(astarH0)
    elif choice == '7':
        runAlgorithm(astarH1)
    elif choice == '8':
        runAlgorithm(astarH2)
    elif choice == '9':
        runAlgorithm(astarH3)
    elif choice == '10':
        inputPath = "samplePuzzles.txt"
        runAlgorithm(ucs)
        # runAlgorithm(gbfsH0)
        runAlgorithm(gbfsH1)
        runAlgorithm(gbfsH2)
        # runAlgorithm(gbfsH3)
        # runAlgorithm(astarH0)
        runAlgorithm(astarH1)
        runAlgorithm(astarH2)
        # runAlgorithm(astarH3)
        print("\nYou can find the result in the analysis.csv :)\n")
    elif choice == 'q':
        print("\nThanks for playing. Hope you were impressed :)\n")
    else:
        print("\nI don't understand that choice, please try again.\n")




