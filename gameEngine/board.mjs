//represents a single tile in the board. holds information about that tile. Each tile represents a 1 inch x 1 inch square on a in person board
class Tile{
    x = -1;
    y = -1;
    blocksLOS = false;
    boardObjects = Array();
    constructor(x,y){
        this.x = x;
        this.y = y;
    }
    //remove the BoardObject that has the name "objectName"
    removeObject(objectName){
        for(var i = 0; i < this.boardObjects.length;i++){
            if(this.boardObjects[i].name == objectName){
                this.boardObjects.splice(i,1);
                return true;
            }
        }
        return false;
    }

    toString(){
        var output = "";
        //console.log(this.boardObjects)
        for(var object of this.boardObjects){
            output += object.name;
            if(object.getType() == "Operative"){
                output += "(" + object.wounds + ")"
            }
        }
        return output;
    }
    
        /*
        //target tile should always be greater than the 
        if(targetTile.x < this.x || targetTile.y < this.y){
            return targetTile.lineOfSight(this);
        }
            */

};

//represents the game board. Keeps track of unit positions, tiles on the board, and other things.
class Board{
    height = 0;
    width = 0;
    tiles = [];
    constructor(height,width){
        this.height = height;
        this.width = width;
        this.tiles = Array(height);
        //create array of tiles
        for(var r = 0; r < height; r++){
            this.tiles[r] = Array(width);
            for(var c = 0; c < width; c++){
                this.tiles[r][c] = new Tile(c,r);
            }
        }
    }

    printBoard(){
        var output = "";
        for(var r = 0; r < this.height; r++){
            for(var c = 0; c < this.width; c++){
                output += "[ " + this.tiles[r][c].toString() + "] "
            }
            output += '\n';
        }
        return output;
    }

    printBoardFormatted(){
        var output = "<table>";
        for(var r = 0; r < this.height; r++){
            output += "<tr>"
            for(var c = 0; c < this.width; c++){
                output += "<td>a" + this.tiles[r][c].toString() + "</td>"
            }
            output += '</tr>';
        }
        return output + "</table>";
    }

    getTile(x,y){
        return this.tiles[y][x]
    }

    //https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    lineOfSight(startTile,targetTile){
        //if the points are oriented wrong, swap them.
        if(targetTile.x < startTile.x){
            //console.log(targetTile.x,targetTile.y)
            return this.lineOfSight(targetTile,startTile)
        }
        var dx = targetTile.x - startTile.x;
        var dy = targetTile.y - startTile.y;
        var D = 2 * dy - dx;
        var y = startTile.y;
        for(var x = startTile.x; x <= targetTile.x; x += 1){
            if(this.tiles[y][x].blocksLOS){
                return false;
            }
            if(D > 0){
                y = y + 1;
                D = D - 2 * dx;
            }
            D = D + 2 * dy;
        };
        return true;
    }

    distance(tile1,tile2){
        return Math.sqrt( (tile1.x-tile2.x)^2 + (tile1.y-tile2.y)^2 )
    }

    getValidMoves(tile,movement){
        var validMoves = []
        for(var x = Math.max(0,tile.x - movement); x <Math.min(tile.x + movement,this.width); x++){
            for(var y = Math.max(0,tile.y - movement); y < Math.min(tile.y + movement,this.height); y++){
                if(Math.sqrt(x^2 + y^2) <= movement){
                    validMoves.push([x,y])
                }
            }
        }
        return validMoves;
    }
};

//represents a object on the board
class BoardObject{
    name = "";
    currentTile = null;
    constructor(tile,name){
        this.name = name;
        this.currentTile = tile;
        tile.boardObjects.push(this);
    }
    //move this object to the given tile
    move(dTile){
        dTile.boardObjects.push(this);
        if(this.currentTile != null){
            this.currentTile.removeObject(this.name);
        }
        this.currentTile = dTile;
    }
    //remove this object from the board
    remove(){
        if(this.currentTile != null){
            this.currentTile.removeObject(this.name);
        }
        delete this;
    }

    getType(){return "BoardObject"}
}

//can block line of sight, block movement, or both
class Terrain extends BoardObject{
    blocksMovement = false;
    blocksLOS = false;
    constructor(tile,name,blocksMovement,blocksLOS){
        super(tile,name);
        this.blocksMovement = blocksMovement;
        this.blocksLOS = blocksLOS;
        tile.blocksLOS = blocksLOS;
    }

    getType(){return "Terrain"}
}

export {
    Tile,
    Board,
    BoardObject
}