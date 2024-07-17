import math

#each entry in the array represents the sides of that dice. Returns an array of the results for each dice
def rollNSidedDice(diceArray : list[int]) -> list[int]:
    output = list(diceArray.length);
    for n in diceArray:
        output[n] = math.round(math.random() * (diceArray[n] - 1) + 1);
    return output;


#roll "count" 6-sided dice
def multiD6(count : int) -> list[int]:
    return rollNSidedDice([6] * count);


#a dice class capable of rolling the result of any combination of dice
class Dice:
    #Example diceString: 2d6+3
    constantTerm = 0;
    dice = [];
    def __init__(self,diceString : str):
        diceString = diceString.lower()
        #get each individual term of the expression
        terms = diceString.split("+")
        for term in terms:
            #split it between the count of the dice and the sides of the dice
            info = term.split('d');
            if len(info) == 1:
                #constant term
                self.constantTerm += int(term);
            else:
                #dice are being rolled
                if info[0] == '':
                    self.dice.append(int(info[1]));
                    continue;
                for i in int(info[0]):
                    self.dice.append(int(info[1]));
                
            
        
        #console.log(this.constantTerm)
        #console.log(this.dice);
    
    #get the total sum of the results
    def roll(self):
        results = rollNSidedDice(self.dice);
        output = 0;
        for result in results :
            output += result;
        
        return self.constantTerm + output;
    

