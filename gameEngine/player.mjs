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

class KT_AI_Player{
    constructor(player,board){
        super(player,board)
    }

    chooseActivation(){
        var possibleChoices = []
        for(var operative of operatives){
            if(!operative.activated){
                possibleChoices.push(operative);
            }
        }
        var toReturn = possibleChoices[Math.round(Math.random() * (possibleChoices.length-1))+1]
        toReturn.activated = true;
        return toReturn;
    }

    movement(operative){
        var possibleMoves = board.getValidMoves(operative.currentTile,operative.movement);
        //select move at random currently. This will eventually be done with the ai
        var moveToMake = possibleMoves[Math.round(Math.random() * (possibleMoves.length-1))+1]
        operative.move(board.getTile(moveToMake[0],moveToMake[1]))
    }

    decideShooting(operative){
        var possibleTargets = opponent.operatives;
        var done = false;
        while(!done){
            var target = possibleTargets[Math.round(Math.random() * (possibleTargets.length -1))+1]
            if(distance(operative.currentTile,target.currentTile) > operative.rangedWeapon.range){
                continue;
            }
            operative.attackUnitRanged(target);
        }
    }

    activationTurn(){
        var activeOperative = chooseActivation()
        this.movement(operative)
        this.decideShooting(operative)
    }
}


export {
    KT_AI_Player
}