import math;
#import typing

#represents a single tile in the board. holds information about that tile. Each tile represents a 1 inch x 1 inch square on a in person board
class Tile:
    x = -1;
    y = -1;
    blocksLOS = False;
    #TODO: Update this to just be names so that up to date information can be pulled from the board object
    
    def __init__(self,_x:int,_y:int):
        self.boardObjects = [];
        self.x = _x;
        self.y = _y;
    
    #remove the BoardObject that has the name "objectName"
    def removeObject(self,objectName:str) -> bool:
        for i in range(len(self.boardObjects)):
            if(self.boardObjects[i].name == objectName):
                del self.boardObjects[i]
                return True;
        return False;

    def toString(self) -> str:
        output = ""#"(" + str(self.x) + "," + str(self.y) + "): ";
        #console.log(this.boardObjects)
        for object in self.boardObjects:
            output += object.name;
        return output;
    

#represents the game board. Keeps track of unit positions, tiles on the board, and other things.
class Board:
    height : int = 0;
    width : int = 0;
    tiles : list[list[Tile]] = [];
    def __init__(self,_height:int,_width:int):
        self.height = _height;
        self.width = _width;
        self.tiles = [None] * _height;
        #create array of tiles
        for r in range(_height):
            self.tiles[r] = [None] * _width;
            for c in range(_width):
                self.tiles[r][c] = Tile(c,r);
    

    def printBoard(self) -> str:
        output = "";
        for r in range(self.height):
            for c in range(self.width):
                output += "[ " + self.tiles[r][c].toString() + "] "
            output += '\n';
        return output;
    

    def printBoardFormatted(self) -> str:
        output = "<table>";
        for r in range(self.height):
            output += "<tr>"
            for c in range(self.width):
                output += "<td>a" + self.tiles[r][c].toString() + "</td>"
            output += '</tr>';
        return output + "</table>";
    

    def getTile(self,x:int,y:int) -> Tile:
        return self.tiles[y][x]
    

    #https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    def lineOfSight(self,startTile : Tile,targetTile : Tile) -> bool:
        #if the points are oriented wrong, swap them.
        if(targetTile.x < startTile.x):
            #console.log(targetTile.x,targetTile.y)
            return self.lineOfSight(targetTile,startTile)
        
        dx = targetTile.x - startTile.x;
        dy = targetTile.y - startTile.y;
        D = 2 * dy - dx;
        y = startTile.y;
        
        for x in range(startTile.x,targetTile.x):
            if(self.tiles[y][x].blocksLOS):
                return False;
            
            if(D > 0):
                y = y + 1;
                D = D - 2 * dx;
            
            D = D + 2 * dy;
        
        return True;
    

    def distance(self,tile1 : Tile,tile2 : Tile) -> float:
        return math.sqrt( (tile1.x-tile2.x)**2 + (tile1.y-tile2.y)**2 )
    

    def getValidMoves(self,tile : Tile,movement : int) -> list[list[int]]:
        validMoves = []
        for  x in range(max(0,tile.x - movement),min(tile.x + movement,self.width)):
            for y in range(max(0,tile.y - movement),min(tile.y + movement,self.height)):
                if(math.sqrt(x**2 + y**2) <= movement):
                    validMoves.append([x,y])
        return validMoves;

    def buildInput(self,player:int):
        output = [0] * (self.height * self.width);
        for r in range(self.height):
            for c in range(self.width):
                if(len(self.tiles[r][c].boardObjects) > 0):
                    if(self.tiles[r][c].boardObjects[0].getType() == "Unit"):
                        if(self.tiles[r][c].boardObjects[0].player == player):
                            output[(r * self.width) + c] = -1;
                        else:
                            output[r * self.width + c] = self.tiles[r][c].boardObjects[0].units[0].toughness;
                    if(self.tiles[r][c].boardObjects[0].getType() == "Terrain"):
                        output[r * self.width + c] = -2;
        return output;
                        


#if(len(self.tiles[r][c].boardObjects) > 0):
#    if(self.tiles[r][c].boardObjects[0].getType() == "Unit"):
#        if(self.tiles[r][c].boardObjects[0].player == player):
#            output[(r * self.width) + c] = 0;
#        else:
#            output[r * self.width + c] = self.tiles[r][c].boardObjects[0].units[0].toughness;
#    if(self.tiles[r][c].boardObjects[0].getType() == "Terrain"):
#        output[r * self.width + c] = -2;

#represents a object on the board
class BoardObject:
    name = "";
    currentTile = None;
    def __init__(self,_tile : Tile,_name : str):
        self.name = _name;
        self.currentTile = _tile;
        _tile.boardObjects.append(self);
    
    #move this object to the given tile
    def move(self, dTile : Tile) -> None:
        dTile.boardObjects.append(self);
        if(self.currentTile != None):
            self.currentTile.removeObject(self.name);  
        self.currentTile = dTile;
    
    #remove this object from the board
    def remove(self) -> None:
        if(self.currentTile != None):
            self.currentTile.removeObject(self.name);
        #delete this;
    

    def getType(self) -> str:
        return "BoardObject"
    
    def x(self) -> int :
        return self.currentTile.x;

    def y(self) -> int :
        return self.currentTile.y;


#can block line of sight, block movement, or both
class Terrain(BoardObject):
    blocksMovement = False;
    blocksLOS = False;
    def __init__(self,tile : Tile,name : str,blocksMovement : bool,blocksLOS : bool):
        BoardObject.__init__(self,tile,name)
        self.blocksMovement = blocksMovement;
        self.blocksLOS = blocksLOS;
        self.blocksLOS = blocksLOS;
    

    def getType(self) -> str:
        return "Terrain"