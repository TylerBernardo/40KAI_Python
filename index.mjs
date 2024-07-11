import express from 'express';
//var express = require("express")
import * as boardUtil from "./gameEngine/board.mjs";
import * as unitUtil from "./gameEngine/units.mjs"
import * as diceUtil from "./gameEngine/dice.mjs"
const app = express();

var testDice = new diceUtil.Dice("D3+2D6+2")

//test dice class
/*
var total = 100000;
var average = 0;
var results = Array(17).fill(0);
for(var i = 0; i < total; i++){
  var testRoll = testDice.roll();
  var testStat = testRoll/total
  average += testStat;
  results[testRoll] += 1;
}
console.log(average);
console.log(results)
for(var index in results){
  console.log((index) + ": " + Math.round(results[index]*100/total))
}
*/
var testBoard= new boardUtil.Board(5,5)

var testUnit = new unitUtil.Unit(testBoard.getTile(2,2),"Test Unit")
testUnit.move(testBoard.getTile(3,3))

app.get('/', (req, res) => {
  res.send('Hello World!\n' + testBoard.printBoardFormatted());
});

app.listen(3000, () => {
  console.log('Express server initialized');
});