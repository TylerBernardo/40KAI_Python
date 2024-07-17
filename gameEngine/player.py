import board
import dice
import units
import math

class WarhammerPlayer:
    playerNum = 0;
    board = None;
    units = []
    opponent = None;
    def __init__(self,player,board):
        self.playerNum = player;
        self.board = board;
    

    def setOpponent(self,newOpponent):
        self.opponent = newOpponent;
    

    def addUnit(self,toAdd):
        self.units.push(toAdd);

    #each class that implements WarhammerPlayer should implement these functions
    def movement():
        return;
    def decideShooting():
        return;
    def turn():
        return;
    #TODO: Add charging

class Warhammer_AI_Player(WarhammerPlayer):
    def __init__(player : int,_board : board.Board):
        WarhammerPlayer.__init__(player,_board)
    

    def sortCompare(a : list[int],b : list[int]) -> bool:
        if(a[0] < b[0]):
            return -1
        if(a[0] > b[0]):
            return 1;
        return 0;
    

    def evaluateMove(self, unit : units.Unit ,moveCords : list[int]) -> float:
        currentDistanceToEnemies = 0;
        newDistanceToEnemies = 0;
        for enemy in self.opponent.units:
            currentDistanceToEnemies += self.board.distance(enemy.currentTile,unit.currentTile)
            newDistanceToEnemies += self.board.distance(enemy.currentTile,self.board.getTile(moveCords[0],moveCords[1]))
        
        #TODO: Use neural network here
        #TODO: Check if move puts you in engagement range of an enemy operative
        inputs = [currentDistanceToEnemies,newDistanceToEnemies,self.board.distance(unit.currentTile,self.board.getTile(moveCords[0],moveCords[1])),unit.units[0].save,unit.units[0].toughness,unit.units[0].movement,unit.units[0].rangedWeapon.range]
        return math.random();
    

    def evaluateShot(self,unit : units.Unit,target :units.Unit) -> float:
        #TODO:redo inputs for new data scheme
        inputs = [self.board.distance(unit.currentTile,target.currentTile),unit.rangedWeapon.ws,unit.rangedWeapon.attacks, unit.rangedWeapon.damage,target.defense, target.save,target.wounds]
        #TODO: use neural network here
        return math.random();
    

    def movement(self, unit : units.Unit) -> None:
        possibleMoves = self.board.getValidMoves(unit.currentTile,unit.movement);
        #select move at random currently. This will eventually be done with the ai
        for i in range(len(possibleMoves)):
            possibleMoves[i] = [self.evaluateMove(unit,possibleMoves[i]),possibleMoves[i]]
        
        #possibleMoves.sort(sortCompare)
        possibleMoves = sorted(possibleMoves, key= lambda move : move[0], reverse=True)
        for move in possibleMoves:
            if(math.random() <= move[0]):
                unit.move(self.board.getTile(move[1][0],move[1][1]))
                return;

    def decideShooting(self,unit : units.Unit) -> None:
        #check if shooting is even possible for this operative
        possibleTargets = [];
        for target in self.opponent.units:
            #evaluate all possible targets
            if(self.distance(unit.currentTile,target.currentTile) > unit.units[0].rangedWeapon.range):
                possibleTargets.append([self.evaluateShot(unit,target),target])
            
        if(possibleTargets.length == 0):
            return
        
        #choose which shot to take
        #possibleTargets.sort(sortCompare)
        possibleMoves = sorted(possibleMoves, key= lambda shot : shot[0], reverse=True)
        for  pTarget in possibleTargets:
            if(math.random() <= pTarget[0]):
                unit.attackUnitRanged(target[1]);
                return
            
        
    

    def turn(self)->None:
        #move all units
        for unit in units:
            self.movement(unit)
        
        #shoot with all units
        for unit in units:
            self.decideShooting(unit)