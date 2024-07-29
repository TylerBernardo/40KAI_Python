import tensorflow as tf;
import keras;
import gameEngine.board as board;
import gameEngine.dice as dice;
import gameEngine.player as player;
import gameEngine.units as units;
import math;
from random import random;

def checkValidMove(oldTile : board.Tile, newTile : board.Tile,movement : int) -> bool:
   # print(movement)
    #print(math.sqrt((oldTile.x - newTile.x)**2 + (oldTile.y - newTile.y)**2))
    return math.sqrt((oldTile.x - newTile.x)**2 + (oldTile.y - newTile.y)**2) <= movement
    
def train(epochs : int, evalsPerEpoch : int, discount : float, learnRate : float):

    e = 1;
    #setup a board and ai player to test with
    testBoard= board.Board(22,30)

    boltRifle = units.Weapon(dice.Dice("3"),3,1,4,None,24,1)

    intercessorModel = units.Unit(6,4,3,2,boltRifle,None)

    testUnit = units.UnitWrapper(testBoard.getTile(2,2),"Test Unit",[intercessorModel.clone()],1)

    #testUnit.move(testBoard.getTile(3,3))

    #testUnit2 = units.UnitWrapper(testBoard.getTile(5,3),"Test Unit2",[intercessorModel.clone()],2)

    testPlayer1 = player.Warhammer_AI_Player(1,testBoard)
    testPlayer2 = player.Warhammer_AI_Player(2,testBoard)
    testPlayer1.addUnit(testUnit)
    #testPlayer2.addUnit(testUnit2)

    presetSpots = [None] * evalsPerEpoch

    for i in range(evalsPerEpoch):
        presetSpots[i] = testBoard.getTile(math.floor(random() * testBoard.width),math.floor(random() * testBoard.height))
    
    #test model pre training
    for i in range(10):
        testUnit.move(testBoard.getTile(math.floor(random() * testBoard.width),math.floor(random() * testBoard.height)))
        #testUnit2.move(testBoard.getTile(math.floor(random() * testBoard.width),math.floor(random() * testBoard.height)))
        oldPos = [testUnit.x(),testUnit.y()];
        #have the network move testUnit based on the network.
        testPlayer1.movement(testUnit,-1)
        #use the new position to calculate the index in the output array
        newPos = [testUnit.x(),testUnit.y()];
        if(checkValidMove(testBoard.getTile(oldPos[0],oldPos[1]),testUnit.currentTile,testUnit.units[0].movement)):
            print("Moved from (" + str(oldPos[0]) + "," + str(oldPos[1]) + ") to (" + str(newPos[0]) + "," + str(newPos[1]) + "), which is a valid move")
        else:
            print("Moved from (" + str(oldPos[0]) + "," + str(oldPos[1]) + ") to (" + str(newPos[0]) + "," + str(newPos[1]) + "), which is not a valid move")
    #train
    optimalNetwork = testPlayer1.moveNet
    changeOptimal = 10;
    for epoch in range(epochs):
        experience = [None] * evalsPerEpoch;
        #collect experience
        for eval in range(evalsPerEpoch):
            toAdd = [None] * 4;
            #set both units to a random position
            testUnit.move(presetSpots[eval])
            #testUnit2.move(testBoard.getTile(math.floor(random() * testBoard.width),math.floor(random() * testBoard.height)))
            #save state to the current experience
            toAdd[0] = testBoard.buildInput(1) + [testUnit.x(),testUnit.y(),testUnit.units[0].movement];
            #save the old position of testUnit
            oldPos = [testUnit.x(),testUnit.y()];
            #have the network move testUnit based on the network.
            testPlayer1.movement(testUnit,e)
            #use the new position to calculate the index in the output array
            newPos = [testUnit.x(),testUnit.y()];
            toAdd[1] = newPos[1] * testBoard.width + newPos[0];
            #give a reward based on whether the move was valid
            if(checkValidMove(presetSpots[eval],testUnit.currentTile,testUnit.units[0].movement)):
                toAdd[2] = 10;
            else:
                toAdd[2] = -1 - 1 * (math.sqrt((newPos[0] - oldPos[0])**2 + (newPos[1] - oldPos[1])**2) - testUnit.units[0].movement);
            #toAdd[2] = 40 - 10 * math.sqrt((newPos[0] - 2)**2 + (newPos[1] - 2)**2)
            toAdd[3] = testBoard.buildInput(1) + [testUnit.x(),testUnit.y(),testUnit.units[0].movement];
            experience[eval] = toAdd;
        #now that experience is collected, calculate the loss
        losses = []
        for exp in experience:
            with tf.GradientTape() as tape:
                qValues = testPlayer1.moveNet.calc(exp[0])
                loss = tf.abs(exp[2] + discount * (tf.math.argmax(optimalNetwork.calc(exp[3]),1).numpy()[0]) - (qValues[0,exp[1]]))**2
            losses.append(float(loss));
            #backpropagate here
            #print(loss)
            #print(testPlayer1.moveNet.q_net.trainable_variables)
            grad = tape.gradient(loss,testPlayer1.moveNet.q_net.trainable_variables)
            #print(grad)
            testPlayer1.moveNet.applyGradients(grad,learnRate)
        
        meanReward = 0;
        for exp in experience:
            meanReward += exp[2] / evalsPerEpoch;
        print("Mean loss: " + str(sum(losses)/len(losses)) + ". Mean Reward:" + str(meanReward))
        e -= .9/epochs;
        if(eval % changeOptimal == 0):
            optimalNetwork = testPlayer1.moveNet
        if(abs(sum(losses)/len(losses)) <= 1):
            break;
    #test if training worked
    for spot in presetSpots:
        testUnit.move(spot)
       # testUnit2.move(testBoard.getTile(math.floor(random() * testBoard.width),math.floor(random() * testBoard.height)))
        oldPos = [testUnit.x(),testUnit.y()];
        #have the network move testUnit based on the network.
        testPlayer1.movement(testUnit,-1)
        #use the new position to calculate the index in the output array
        newPos = [testUnit.x(),testUnit.y()];
        if(checkValidMove(testBoard.getTile(oldPos[0],oldPos[1]),testUnit.currentTile,testUnit.units[0].movement)):
            print("Moved from (" + str(oldPos[0]) + "," + str(oldPos[1]) + ") to (" + str(newPos[0]) + "," + str(newPos[1]) + "), which is a valid move")
        else:
            print("Moved from (" + str(oldPos[0]) + "," + str(oldPos[1]) + ") to (" + str(newPos[0]) + "," + str(newPos[1]) + "), which is not a valid move")
            