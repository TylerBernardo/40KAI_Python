import gameEngine.board as Board
import gameEngine.dice as dice
import gameEngine.units as Units
import math
from random import random
import tensorflow as tf
import QNetwork.qnetwork as qnetwork;

def dense_layer(num_units):
  return tf.keras.layers.Dense(
      num_units,
      activation=tf.keras.activations.relu,
      kernel_initializer=tf.keras.initializers.VarianceScaling(
          scale=2.0, mode='fan_in', distribution='truncated_normal'))

class WarhammerPlayer:
    playerNum = 0;
    board = None;
    units = []
    opponent = None;
    def __init__(self,player : int,board : Board.Board):
        self.playerNum = player;
        self.board = board;
    

    def setOpponent(self,newOpponent):
        self.opponent = newOpponent;
    

    def addUnit(self,toAdd : Units.UnitWrapper):
        self.units.append(toAdd);

    #each class that implements WarhammerPlayer should implement these functions
    def movement():
        return;
    def decideShooting():
        return;
    def turn():
        return;
    #TODO: Add charging

class Warhammer_AI_Player(WarhammerPlayer):
    #DeepQ network for moving
    #Inputs: unit position, board information, in cover currently, in cover when ending, distance to closest enemy, movement value
    #Outputs: Q score for each tile on the board
    #For early testing, only pass in board, unit position, and movement characteristic.for board 0 represents empty, -1 = friendly unit, -2 = terrain, and n > 0 represent an enemy with toughness n
    moveNet : qnetwork.QNetwork = qnetwork.QNetwork(22*30+3,[50],22*30);

    def __init__(self,player : int,_board : Board.Board):
        WarhammerPlayer.__init__(self,player,_board)
    
    def sortCompare(a : list[int],b : list[int]) -> bool:
        if(a[0] < b[0]):
            return -1
        if(a[0] > b[0]):
            return 1;
        return 0;
    

    def evaluateMove(self, unit : Units.UnitWrapper ,moveCords : list[int]) -> float:
        currentDistanceToEnemies = 0;
        newDistanceToEnemies = 0;
        if(self.opponent != None):
            for enemy in self.opponent.units:
                currentDistanceToEnemies += self.board.distance(enemy.currentTile,unit.currentTile)
                newDistanceToEnemies += self.board.distance(enemy.currentTile,self.board.getTile(moveCords[0],moveCords[1]))
        
        #TODO: Use neural network here
        #TODO: Check if move puts you in engagement range of an enemy operative
        inputs = [currentDistanceToEnemies,newDistanceToEnemies,self.board.distance(unit.currentTile,self.board.getTile(moveCords[0],moveCords[1])),unit.units[0].save,unit.units[0].toughness,unit.units[0].movement,unit.units[0].rangedWeapon.range]
        return random();
    
    #dont use neural net for shooting. For now just calculate the expected value of a combat and use that to fuel decisions
    def evaluateShot(self,unit : Units.UnitWrapper,target :Units.UnitWrapper) -> float:
        #TODO:redo inputs for new data scheme
        #inputs = [self.board.distance(unit.currentTile,target.currentTile),unit.rangedWeapon.ws,unit.rangedWeapon.attacks, unit.rangedWeapon.damage,target.defense, target.save,target.wounds]
        #score a shot based on how many wounds you deal scaled by how tough the target was. This should work decently to pick up small units, while still ensures it takes shots against tanks when it can.
        return unit.estimateAttack(target) * target.units[0].toughness/4
    

    def movement(self, unit : Units.UnitWrapper,e : int) -> None:
        if(random() <= e):
            unit.move(self.board.getTile(math.floor(random()*self.board.width),math.floor(random() * self.board.height)))
            return;
        
        inputs = self.board.buildInput(self.playerNum) + [unit.x(),unit.y(),unit.units[0].movement]
        qValues = self.moveNet.calc(inputs);
        #print(qValues);
        #print(type(qValues))
        largestIndex = int(tf.math.argmax(qValues,1).numpy()[0]);
        #print(largestIndex)
        c = largestIndex % self.board.width;
        r = (largestIndex - c) / self.board.width;
        #print(c,r)
        unit.move(self.board.getTile(int(c),int(r)));

    def decideShooting(self,unit : Units.UnitWrapper) -> None:
        #TODO: make more efficent. No need to save all targets now that we just take the one with the best score
        #check if shooting is even possible for this operative
        possibleTargets = [];
        for target in self.opponent.units:
            #evaluate all possible targets
            if(self.distance(unit.currentTile,target.currentTile) > unit.units[0].rangedWeapon.range):
                possibleTargets.append([self.evaluateShot(unit,target),target])
            
        if(len(possibleTargets) == 0):
            return
        
        #choose which shot to take
        #possibleTargets.sort(sortCompare)
        possibleMoves = sorted(possibleMoves, key= lambda shot : shot[0], reverse=True)
        unit.attackUnitRanged(possibleMoves[1])

    def turn(self)->None:
        #move all units
        for unit in self.units:
            self.movement(unit)
        
        #shoot with all units
        for unit in self.units:
            self.decideShooting(unit)