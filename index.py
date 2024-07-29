#import server packages
from flask import Flask,send_from_directory
from flask_socketio import SocketIO,send,emit
from time import sleep
#40k AI files
import gameEngine.board as board;
import gameEngine.dice as dice
import gameEngine.player as player
import gameEngine.units as units
import QNetwork.training as training
#create flask app
app = Flask(__name__)
socketio = SocketIO(app);

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')


#var testDice = new diceUtil.Dice("D3+2D6+2")
#var total = 100000;
#var average = 0;
#var results = Array(17).fill(0);
##for(var i = 0; i < total; i++){
#  var testRoll = testDice.roll();
#  var testStat = testRoll/total
#  average += testStat;
#  results[testRoll] += 1;
#}
#console.log(average);
#console.log(results)
#for(var index in results){
#  console.log((index) + ": " + Math.round(results[index]*100/total))
#}
#*/
testBoard= board.Board(22,30)


boltRifle = units.Weapon(dice.Dice("3"),3,1,4,None,24,1)

intercessorModel = units.Unit(6,4,3,2,boltRifle,None)

testUnit = units.UnitWrapper(testBoard.getTile(2,2),"Test Unit",[intercessorModel.clone()],1)

#testUnit.move(testBoard.getTile(3,3))

testUnit2 = units.UnitWrapper(testBoard.getTile(5,3),"Test Unit2",[intercessorModel.clone()],1)

testPlayer = player.Warhammer_AI_Player(1,testBoard)
testPlayer.addUnit(testUnit)
testPlayer.addUnit(testUnit2)

#testUnit2.attackUnitRanged(testUnit)

training.train(300,100,0,.01);

@app.route("/")
def handleMain():
    return send_from_directory("UI","index.html")



@app.route('/UI/<path:path>')
def send_report(path):
    return send_from_directory('UI', path)


@socketio.on("connection")
def onConnect():
    print("test");
    

@socketio.on("ready")
def onReady():
    emit("buildTable",(30,22));
    emit("setModel",(testUnit.currentTile.x,testUnit.currentTile.y,"testUnit",1))
    emit("setModel",(testUnit2.currentTile.x,testUnit2.currentTile.y,"testUnit2",2))
    sleep(3)
    testPlayer.movement(testUnit)
    emit("setModel",(testUnit.currentTile.x,testUnit.currentTile.y,"testUnit","1"))
    #for i in range(10):
        #testPlayer.movement(testUnit)
        #emit("setModel",(testUnit.currentTile.x,testUnit.currentTile.y,"testUnit","1"))
        #sleep(1)
        #testPlayer.movement(testUnit2)
        #emit("setModel",(testUnit2.currentTile.x,testUnit2.currentTile.y,"testUnit2","2"))
        #sleep(1)