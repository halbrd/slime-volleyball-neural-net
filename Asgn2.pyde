from Game import Game
from NeuralNet import Bot
from NeuralNet import Perceptron
from Selector import Selector
from Selector import getLatestGenData
from Selector import getSpecificGenData
import json
import random

BOT_MODE = False    # False for testing against a bot, True to run evolutionary arms race
BOT_V_BOT = False    # True to run a non-learning bot showmatch

TEST_GEN = None    # None for latest gen, positive integer to test that specific generation
TEST_INDEX = None    # None for random bot from given generation, positive integer to choose particular bot in generation to load


def setup():
    global game, keysDown, selector
    
    size(800, 800)
    frameRate(60)
    
    if BOT_MODE:
        selector = Selector()
    else:
        opponentBot = Bot()
        selfBot = None
        
        if TEST_GEN is None:
            # Check for existing generations
            genData = getLatestGenData()
        else:
            genData = getSpecificGenData(TEST_GEN)
        
        if genData is not None:
            # Make a bot from a random new gen bot on the list
            loadedBot = Bot()
            loadedPF = Perceptron(8)
            loadedPB = Perceptron(8)
            loadedPJ = Perceptron(8)
            randomBotIndex = (TEST_INDEX if TEST_INDEX is not None else random.randint(0, 9))
            print("Chose opponent bot " + str(randomBotIndex))
            newBotsData = genData[str(randomBotIndex)]
            loadedPF.weights = newBotsData[0]
            loadedPB.weights = newBotsData[1]
            loadedPJ.weights = newBotsData[2]
            loadedBot.setPerceptrons(loadedPF, loadedPB, loadedPJ)
            opponentBot = loadedBot
            
            # Get another bot if it's a bot vs bot showmatch
            if BOT_V_BOT:
                loadedPF = Perceptron(8)
                loadedPB = Perceptron(8)
                loadedPJ = Perceptron(8)
                randomBotIndex = random.randint(0, 9)
                print("Chose self bot " + str(randomBotIndex))
                newBotsData = genData[str(randomBotIndex)]
                loadedPF.weights = newBotsData[0]
                loadedPB.weights = newBotsData[1]
                loadedPJ.weights = newBotsData[2]
                loadedBot.setPerceptrons(loadedPF, loadedPB, loadedPJ)
                selfBot = loadedBot
            
        game = Game(selfBot, opponentBot)
    
    keysDown = {}
    
def draw():
    global game, keysDown
    
    background(255)

    if BOT_MODE:
        selector.run()
    else:
        game.update(keysDown)
        game.draw()
    
def keyPressed():
    global keysDown
    keysDown[key] = True
    
def keyReleased():
    global keysDown
    keysDown[key] = False