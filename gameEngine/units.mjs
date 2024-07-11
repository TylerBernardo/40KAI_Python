import {BoardObject} from "./board.mjs"

class Weapon{

}
//warhammer 40k unit
class Unit extends BoardObject{
    movement;
    actionPoints;
    groupActivation;
    save;
    wounds;
    constructor(tile,name,movement,actionPoints,groupActivation,save,wounds){
        super(tile,name);
        this.movement = movement;
        this.actionPoints = actionPoints;
        this.groupActivation = groupActivation;
        this.save = save;
        this.wounds = wounds;
    }
}
//Kill Team operative

export {
    Weapon,
    Unit
}