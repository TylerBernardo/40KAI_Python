#import server packages
from flask import Flask

#40k AI files
import gameEngine.board as board;
import gameEngine.dice as dice
import gameEngine.player as player
import gameEngine.units as units
#create flask app
app = Flask(__name__)




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

boltRifle = units.Weapon(3,3,1,4,24,1)

intercessorModel = units.Unit(6,3,1,3,3,14,boltRifle,None)

testUnit = units.UnitWrapper(testBoard.getTile(2,2),"Test Unit",testBoard,[intercessorModel.clone()])
#testUnit.move(testBoard.getTile(3,3))

testUnit2 = units.UnitWrapper(testBoard.getTile(2,2),"Test Unit2",testBoard,[intercessorModel.clone()])

testPlayer = player.Warhammer_AI_Player(1,testBoard)
testPlayer.addUnit(testUnit)
testPlayer.addUnit(testUnit2)

#testUnit2.attackUnitRanged(testUnit)

#async function demo(socket){
#  for(var i = 0; i < 10; i++){
#    testPlayer.movement(testUnit)
#    io.emit("setModel",testUnit.currentTile.x,testUnit.currentTile.y,"testUnit","1")
#    await delay(1000)
#    testPlayer.movement(testUnit2)
#    io.emit("setModel",testUnit2.currentTile.x,testUnit2.currentTile.y,"testUnit2","2")
#    await delay(1000)
#  }
#}

@app.route("/")
def handleMain():
    return "<b>test</b>"

#io.on('connection', (socket) => {
#  console.log("user connected")#
#
#  socket.on("ready", () => {
#    console.log("user is ready")
#    io.emit("buildTable",30,22)
#    io.emit("setModel",testUnit.currentTile.x,testUnit.currentTile.y,"testUnit","1")
#    io.emit("setModel",testUnit2.currentTile.x,testUnit2.currentTile.y,"testUnit2","2")
#    demo(socket)
#  })
#})

#server.listen(3000, () => {
#  console.log('server initialized');
#});