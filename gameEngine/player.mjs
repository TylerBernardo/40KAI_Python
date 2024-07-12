import * as boardUtils from "./board.mjs"
import * as diceUtils from "./dice.mjs"
import * as unitUtils from "./units.mjs"

class KTPlayer{
    playerNum = 0;
    board = null;
    operatives = []
    opponent = null;
    activationsRemaining = 0;
    constructor(player,board){
        this.playerNum = player;
        this.board = board;
    }

    setOpponent(newOpponent){
        this.opponent = newOpponent;
    }

    addOperative(toAdd){
        this.operatives.push(toAdd);
    }

    resetActivations(){
        for(var operative of operatives){
            operative.activated = false;
        }
        this.activationsRemaining = operatives.length;
    }

    //each class that implements KTPlayer should implement these functions
    chooseActivation(){}
    movement(){}
    decideFight(){}
    activationTurn(){}
}

class KT_AI_Player extends KTPlayer{
    constructor(player,board){
        super(player,board)
    }

    sortCompare(a,b){
        if(a[0] < b[0]){
            return -1
        }
        if(a[0] > b[0]){
            return 1;
        }
        return 0;
    }

    chooseActivation(){
        var possibleChoices = []
        for(var operative of this.operatives){
            if(!operative.activated){
                possibleChoices.push(operative);
            }
        }
        var toReturn = possibleChoices[Math.round(Math.random() * (possibleChoices.length-1))+1]
        toReturn.activated = true;
        return toReturn;
    }

    evaluateMove(operative,moveCords){
        var currentDistanceToEnemies = 0;
        var newDistanceToEnemies = 0;
        for(var enemy of this.opponent.operatives){
            currentDistanceToEnemies += this.board.distance(enemy.currentTile,operative.currentTile)
            newDistanceToEnemies += this.board.distance(enemy.currentTile,this.board.getTile(moveCords[0],moveCords[1]))
        }
        //TODO: Use neural network here
        //TODO: Check if move puts you in engagement range of an enemy operative
        inputs = [currentDistanceToEnemies,newDistanceToEnemies,this.board.distance(operative.currentTile,this.board.getTile(moveCords[0],moveCords[1])),operative.save,operative.defense,operative.wounds,operative.rangedWeapon.range]
        return Math.random();
    }

    evaluateShot(operative,target){
        inputs = [this.board.distance(operative.currentTile,target.currentTile),operative.rangedWeapon.ws,operative.rangedWeapon.attacks, operative.rangedWeapon.damage,target.defense, target.save,target.wounds]
        //todo: use neural network here
        return Math.random();
    }

    movement(operative){
        var possibleMoves = this.board.getValidMoves(operative.currentTile,operative.movement);
        //select move at random currently. This will eventually be done with the ai
        for(var i = 0; i < possibleMoves.length; i++){
            possibleMoves[i] = [this.evaluateMove(operative,possibleMoves[i]),possibleMoves[i]]
        }
        //account for charges
        for(var cTarget of this.opponent.operatives){
            if(this.board.distance(operative.currentTile,cTarget.currentTile) <= operative.movement + 2){
                possibleMoves.push([this.evaluateMove(operative,[cTarget.currentTile.x,cTarget.currentTile.y]),[cTarget.currentTile.x,cTarget.currentTile.y]])
            }
        }
        possibleMoves.sort(sortCompare)
        for(var move of possibleMoves){
            if(Math.random() <= move[0]){
                operative.move(this.board.getTile(move[1][0],move[1][1]))
                return;
            }
        }
    
    }

    decideShooting(operative){
        //check if shooting is even possible for this operative
        var possibleTargets = [];
        for(var target of opponent.operatives){
            //evaluate all possible targets
            if(distance(operative.currentTile,target.currentTile) > operative.rangedWeapon.range){
                possibleTargets.push([evaluateShot(operative,target),target])
            }
        }
        if(possibleTargets.length == 0){
            return
        }
        //choose which shot to take
        possibleTargets.sort(sortCompare)
        for(var pTarget of possibleTargets){
            if(Math.random() <= pTarget[0]){
                operative.attackUnitRanged(target[1]);
                return
            }
        }
    }
    //we will assume an operative will always fight in melee if it can
    activationTurn(){
        activationsRemaining--;
        var activeOperative = chooseActivation()
        this.movement(activeOperative)
        this.decideShooting(activeOperative)
    }
}


export {
    KT_AI_Player
}