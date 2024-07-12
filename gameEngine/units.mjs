import {BoardObject} from "./board.mjs"
import * as diceUtil from "./dice.mjs"

class KTWeapon{
    attacks = 0;
    ws = 7;
    damage = 0;
    criticalDamage;
    keywords = [];
    range = 0;
    constructor(attacks,ws,damage,criticalDamage,keywords,range){
        this.attacks = attacks;
        this.ws = ws;
        this.damage = damage;
        this.criticalDamage = damage;
        this.keywords = keywords;
        this.range = range;
    }
    //returns an array of length two. output[0] represents the number of succesful attack dice, and output[1] represents the number of critical successes
    attack(){
        var results = diceUtil.multiD6(this.attacks);
        var output = [0,0]
        for(var result of results){
            if(result >= this.ws){
                if(result == 6){
                    output[1]++;
                }else{
                    output[0]++;
                }
            }
        }
        return output;
    }

}
//kill team unit
class Operative extends BoardObject{
    movement;
    actionPoints;
    groupActivation;
    defense;
    save;
    wounds;
    rangedWeapon;
    meleeWeapon;
    board;
    constructor(tile,name,movement,actionPoints,groupActivation,defense,save,wounds,rangedWeapon,meleeWeapon,board){
        super(tile,name);
        this.movement = movement;
        this.actionPoints = actionPoints;
        this.groupActivation = groupActivation;
        this.save = save;
        this.wounds = wounds;
        this.rangedWeapon = rangedWeapon;
        this.meleeWeapon = meleeWeapon;
        this.defense = defense;
        this.board = board;
    }

    //make saving throws based on the incoming attacks
    defend(attackDice){
        var results = diceUtil.multiD6(this.defense);
        var successes = [0,0];
        for(var result of results){
            if(result >= this.save){
                if(result == 6){
                    successes[1] += 1
                }else{
                    successes[0] += 1;
                }
            }
        }
        if(attackDice[1] != 0){
            //pick the smaller of the 2 quantities
            var diceToRemove = Math.min(attackDice[1] , successes[1])
            //each critical attack is counteracted by a critical save
            attackDice[1] -= diceToRemove;
            successes[1] -= diceToRemove;
        }
        //reduce the number of regular attacks based on the save
        attackDice[0] = Math.max(0,attackDice[0]-successes[0] - 2 * successes[1]);
        return attackDice;
    }

    takeDamage(damageToTake){
        this.wounds -= damageToTake;
        if(this.wounds <= 0){
            this.remove();
        }
    }

    attackUnitRanged(unitToAttack){
        //check if line of sight is ok
        var lineOfSight = this.board.lineOfSight(this.currentTile,unitToAttack.currentTile);
        if(!lineOfSight){
            return;
        }
        var attackDice = this.rangedWeapon.attack();

        var succesfulAttacks = unitToAttack.defend(attackDice);

        var totalDamage = succesfulAttacks[0] * this.rangedWeapon.damage + succesfulAttacks[1] * this.rangedWeapon.criticalDamage;

        unitToAttack.takeDamage(totalDamage);
    }
}

export {
    KTWeapon,
    Operative
}