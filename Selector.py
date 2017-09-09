from Game import Game
from NeuralNet import Bot
from NeuralNet import Perceptron
import datetime
import random
import os.path
import json

class Selector:
    poolSize = 10
    runtime = 10
    
    def __init__(self):
        self.bots = [Bot() for _ in range(self.poolSize)]
        self.scores = [0 for _ in range(self.poolSize)]
        
    def run(self):
        # Check for existing generations
        lastGenerationData = getLatestGenData()
        if lastGenerationData is not None:
            self.loadBotsFromData(lastGenerationData)
        
        # Run round robin of bot vs bot games
        gameNo = 0
        self.scores = [0 for _ in range(self.poolSize)]   # Reset scores to zero each tournament
        for i in range(len(self.bots)):
            for j in range(i + 1, len(self.bots)):
                gameNo += 1
                
                textSize(24)
                textAlign(CENTER, CENTER)
                fill(0)
                text("Running simulation...", width / 2, 100)
                
                thisBot = self.bots[i]
                opponent = self.bots[j]

                startTime = datetime.datetime.now()
                finishTime = startTime + datetime.timedelta(seconds = self.runtime)
                
                game = Game(thisBot, opponent)
                
                # Run game for 10 seconds
                while not datetime.datetime.now() > finishTime:
                    game.update(None)
                    game.draw()    # Unfortunately this entire function is basically one big blocking call so the game doesn't get rendered real-time 
                    
                print("FINISHED GAME " + str(gameNo) + " Bot " + str(i) + "vs" + str(j) + " " + str(game.player1.points) + ":" + str(game.player2.points))
                
                thisBotNetScore = game.player1.points - game.player2.points
                opponentNetScore = game.player2.points - game.player1.points
                
                self.scores[i] += thisBotNetScore
                self.scores[j] += opponentNetScore
                
        print("Scores: ")
        print(self.scores)
        
        # Select the two bots with the best genes
        bestIndices = getBestTwo(self.scores)
        bestBot = self.bots[bestIndices[0]]
        secondBestBot = self.bots[bestIndices[1]]
        
        print("Best scores: ")
        print(str(self.scores[bestIndices[0]]) + ", " + str(self.scores[bestIndices[1]]))
        
        # Create a new generation of poolSize children
        newGen = []
        for _ in range(self.poolSize):
            child = crossover(bestBot, secondBestBot)
            mutate(child)
            newGen.append(child)
            
        #print("New generation: ")
        #for bot in newGen:
        #    print(str(bot.pForward.weights) + "  |  " + str(bot.pBackward.weights) + "  |  " + str(bot.pJump.weights))
        
        # Save new generation to file
        newGenDict = {}
        for i in range(len(newGen)):
            bot = newGen[i]
            genes = [bot.pForward.weights, bot.pBackward.weights, bot.pJump.weights]
            newGenDict[i] = genes
        
        generationIndex = 0
        while os.path.isfile("generation" + str(generationIndex) + ".txt"):
            generationIndex += 1
        fileName = "generation" + str(generationIndex) + ".txt"
        with open(fileName, "w") as f:
            f.write(json.dumps(newGenDict, indent=4))
            
    def loadBotsFromData(self, data):
        for key in data:
            loadedBot = Bot()
            loadedPF = Perceptron(8)
            loadedPB = Perceptron(8)
            loadedPJ = Perceptron(8)
            newBotsData = data[key]
            loadedPF.weights = newBotsData[0]
            loadedPB.weights = newBotsData[1]
            loadedPJ.weights = newBotsData[2]
            loadedBot.setPerceptrons(loadedPF, loadedPB, loadedPJ)
            self.bots[int(key)] = loadedBot
            #print("Loaded bot for index " + str(key))


def getBestTwo(array):
    best = array[0]
    secondBest = array[1]
    if secondBest > best:
        best, secondBest = secondBest, best
        
    for i in range(len(array)):
        if array[i] > best:
            secondBest = best
            best = array[i]
        elif array[i] > secondBest:
            secondBest = array[i]
        
    #print(best)
    #print(secondBest)
        
    best = array.index(best)
    secondBest = array.index(secondBest)
        
    #print(best)
    #print(secondBest)
        
    return [best, secondBest]
    
def crossover(bot1, bot2):
    n = len(bot1.pForward.weights)
    newPForward = Perceptron(n)
    newPBackward = Perceptron(n)
    newPJump = Perceptron(n)
    
    # New forward perceptron
    perc1 = bot1.pForward
    perc2 = bot2.pForward
    
    for i in range(n):
        if random.randint(0, 1) == 1:
            newPForward.weights[i] = perc1.weights[i]
        else:
            newPForward.weights[i] = perc2.weights[i]
    
    # New backward perceptron
    perc1 = bot1.pBackward
    perc2 = bot2.pBackward
    
    for i in range(n):
        if random.randint(0, 1) == 1:
            newPBackward.weights[i] = perc1.weights[i]
        else:
            newPBackward.weights[i] = perc2.weights[i]
            
    # New jump perceptron
    perc1 = bot1.pJump
    perc2 = bot2.pJump
    
    for i in range(n):
        if random.randint(0, 1) == 1:
            newPJump.weights[i] = perc1.weights[i]
        else:
            newPJump.weights[i] = perc2.weights[i]
            
    child = Bot()
    child.setPerceptrons(newPForward, newPBackward, newPJump)
    
    return child

def mutate(bot):
    for i in range(len(bot.pForward.weights)):
        if random.randint(0, 10) == 0:
            bot.pForward.weights[i] = random.uniform(-1, 1)
    
    for i in range(len(bot.pBackward.weights)):
        if random.randint(0, 10) == 0:
            bot.pBackward.weights[i] = random.uniform(-1, 1)
            
    for i in range(len(bot.pJump.weights)):
        if random.randint(0, 10) == 0:
            bot.pJump.weights[i] = random.uniform(-1, 1)
    
            
    
def getLatestGenData():
    if not os.path.isfile("generation0.txt"):
        return None
    else:
        # Find the latest generation
        generationIndex = 1
        while os.path.isfile("generation" + str(generationIndex) + ".txt"):
            generationIndex += 1
        # Load last generation
        generationIndex -= 1
        print("Loading generation " + str(generationIndex))
        lastGenerationName = "generation" + str(generationIndex) + ".txt"
        with open(lastGenerationName, "r") as f:
            lastGenerationData = json.load(f)
        return lastGenerationData

def getSpecificGenData(gen):
    if not os.path.isfile("generation" + str(gen) + ".txt"):
        return None
    else:
        # Load generation
        print("Loading generation " + str(gen))
        generationName = "generation" + str(gen) + ".txt"
        with open(generationName, "r") as f:
            genData = json.load(f)
        return genData