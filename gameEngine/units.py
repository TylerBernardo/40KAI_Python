import gameEngine.board as board;
import gameEngine.dice as dice;
import math;
import copy

class Weapon:
    attacks = 0;
    ws = 7;
    damage = 0;
    strength = 0;
    keywords = [];
    range = 0;
    ap = 0;
    def __init__(self,attacks:int,ws:int,damage:int,strength:int,keywords:list[str],range:int,ap:int):
        self.attacks = attacks;
        self.ws = ws;
        self.damage = damage;
        self.strength = strength;
        self.keywords = keywords;
        self.range = range;
        self.ap = ap;
    
    #returns an array of length two. output[0] represents the number of succesful attack dice, and output[1] represents the number of critical successes

    def attack(self,toughness:int)->int:
        results = dice.multiD6(self.attacks);
        hits = 0;
        for result in results:
            if(result >= self.ws):
                hits+=1;
        woundResults = dice.multiD6(hits);
        output = 0;
        #determine what it takes to wound
        toWound = 5;

        if self.strength * 2 <= toughness:
            toWound = 6;
        if self.strength < toughness:
            toWound = 5;
        if self.strength == toughness:
            toWound = 4;
        if toughness <= self.strength * 2:
            toWound = 2;

        for result in results:
            if(result >= toWound):
                output+=1;
    
        return output;

#40K unit
#keep array of models for wound allocation and weapon tracking
#optional character property
class Unit:
    #TODO: rewrite properties for a 40k units
    movement:int=0;
    toughness:int=0;
    save:int=0;
    wounds:int=0;
    rangedWeapon:Weapon=None;
    meleeWeapon:Weapon=None;
    def __init__(self,movement:int,toughness:int,save:int,wounds:int,rangedWeapon:Weapon,meleeWeapon:Weapon):
        self.movement = movement;
        self.save = save;
        self.wounds = wounds;
        self.rangedWeapon = rangedWeapon;
        self.meleeWeapon = meleeWeapon;
        self.toughness = toughness;
    

    def clone(self):
        return copy.deepcopy(self) #structuredClone(this);
        #return new this(this.movement,this.toughness,this.save,this.wounds.this.rangedWeapon,this.meleeWeapon)

class UnitWrapper(board.BoardObject):
    units = []
    character = None;
    def __init__(self,tile : board.Tile,name : str,units:list[Unit]):
        board.BoardObject.__init__(self,tile,name);
        self.units = units;
    

    #make saving throws based on the incoming attacks
    def savingThrows(self,wounds:int,ap:int)->int:
        results = dice.multiD6(wounds);
        successes = 0;
        for result in results:
            if(result - ap >= self.units[0].save):
                successes+=1;

        #reduce the number of regular attacks based on the save
        #attackDice[0] = Math.max(0,attackDice[0]-successes[0] - 2 * successes[1]);
        return max(wounds-successes,0);

    #TODO: rewrite for multiple models in a unit
    def takeDamage(self,damageToTake:int)->None:
        self.units[0].wounds -= damageToTake;
        if(self.units[0].wounds <= 0):
            if(len(self.units) == 1):
                self.remove();
                return;
            #pull the unit from the back of the list to the front
            self.units[0] = self.units[len(self.units) - 1];
            self.units.pop();

    def attackUnitRanged(self,unitToAttack:Unit) -> None:
        #check if line of sight is ok
        lineOfSight = self.board.lineOfSight(self.currentTile,unitToAttack.currentTile);
        if(not lineOfSight):
            return;
        
        #TODO: redo this sequence for multiple attacking models and weapons of different stats
        #for now iterate over each unit and attack with each of its weapons. redo later into batches when human dice rolling is involved
        for unit in self.units:
            wounds = unit.rangedWeapon.attack();

            succesfulWounds = unitToAttack.savingThrows(wounds);
    
            for i in range(succesfulWounds):
                unitToAttack.takeDamage(unit.rangedWeapon.damage);

    def getType() -> str:
        return "Unit"


