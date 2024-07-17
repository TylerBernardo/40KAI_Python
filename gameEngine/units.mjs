import {Board, BoardObject} from "./board.mjs"
import * as diceUtil from "./dice.mjs"

class Weapon{
    attacks = 0;
    ws = 7;
    damage = 0;
    strength = 0;
    keywords = [];
    range = 0;
    ap = 0;
    constructor(attacks,ws,damage,strength,keywords,range,ap){
        this.attacks = attacks;
        this.ws = ws;
        this.damage = damage;
        this.strength = strength;
        this.keywords = keywords;
        this.range = range;
        this.ap = ap;
    }
    //returns an array of length two. output[0] represents the number of succesful attack dice, and output[1] represents the number of critical successes

    attack(toughness){
        var results = diceUtil.multiD6(this.attacks);
        var hits = 0;
        for(var result of results){
            if(result >= ws){
                hits++;
            }
        }
        var woundResults = diceUtil.multiD6(hits);
        var output = 0;
        //determine what it takes to wound
        var toWound = 5;
        switch(true){
            case this.strength * 2 <= toughness:
                toWound = 6;
                break;
            case this.strength < toughness:
                toWound = 5;
                break;
            case this.strength == toughness:
                toWound = 4;
                break;
            case toughness <= this.strength * 2:
                toWound = 2;
                break;
        }

        for(var result of results){
            if(result >= toWound){
                output++;
            }
        }
        return output;
    }

}

class UnitWrapper extends BoardObject{
    units = []
    character = null;
    constructor(tile,name,units){
        super(tile,name);
        this.units = units;
    }

    //make saving throws based on the incoming attacks
    savingThrows(wounds,ap){
        var results = diceUtil.multiD6(wounds);
        var successes = 0;
        for(var result of results){
            if(result - ap >= this.units[0].save){
                successes++;
            }
        }
        //reduce the number of regular attacks based on the save
        //attackDice[0] = Math.max(0,attackDice[0]-successes[0] - 2 * successes[1]);
        return Math.max(wounds-successes,0);
    }

    //TODO: rewrite for multiple models in a unit
    takeDamage(damageToTake){
        this.units[0].wounds -= damageToTake;
        if(this.units[0].wounds <= 0){
            if(this.units.length == 1){
                this.remove();
                return;
            }
            //pull the unit from the back of the list to the front
            this.units[0] = this.units[this.units.length - 1];
            this.units.pop();
        }

    }

    attackUnitRanged(unitToAttack){
        //check if line of sight is ok
        var lineOfSight = this.board.lineOfSight(this.currentTile,unitToAttack.currentTile);
        if(!lineOfSight){
            return;
        }
        //TODO: redo this sequence for multiple attacking models and weapons of different stats
        //for now iterate over each unit and attack with each of its weapons. redo later into batches when human dice rolling is involved
        for(var unit of this.units){
            var wounds = unit.rangedWeapon.attack();

            var succesfulWounds = unitToAttack.savingThrows(wounds);
    
            for(var i = 0; i < succesfulWounds; i++){
                unitToAttack.takeDamage(unit.rangedWeapon.damage);
            }
        }
    }

    getType(){return "Unit"}
}

//40K unit
//keep array of models for wound allocation and weapon tracking
//optional character property
class Unit{
    //TODO: rewrite properties for a 40k units
    movement;
    toughness;
    save;
    wounds;
    rangedWeapon;
    meleeWeapon;
    constructor(movement,toughness,save,wounds,rangedWeapon,meleeWeapon){
        this.movement = movement;
        this.save = save;
        this.wounds = wounds;
        this.rangedWeapon = rangedWeapon;
        this.meleeWeapon = meleeWeapon;
        this.toughness = toughness;
    }

    clone(){
        return structuredClone(this);
        //return new this(this.movement,this.toughness,this.save,this.wounds.this.rangedWeapon,this.meleeWeapon)
    }
}

export {
    Weapon,
    UnitWrapper,
    Unit
}