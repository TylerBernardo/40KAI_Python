var socket;
var body;
var tableList = []
var widthG,heightG;
var currentModels = {}

var selected = false;
var selectedModel;
var selectedModelPlayer;

function onloadF(){
  body = document.getElementsByTagName("body")[0]
  socket = io();

  socket.on('buildTable', function(width, height){
    widthG = width;
    heightG = height;
    console.log(width,height)
    var table = document.createElement("table")
    for(var r = 0; r < height; r++){
      var tr = document.createElement("tr")
      for(var c = 0; c < width; c++){
        var link = document.createElement("a")
        link.href = "#"
        link.addEventListener("click",moveModel)
        var cell = document.createElement("td")
        cell.innerHTML = c + "," + r
        cell.id = c + "," + r
        //cell.addEventListener("click",moveModel)
        tableList.push(cell)
        link.appendChild(cell)
        tr.appendChild(link)
      }
      table.appendChild(tr)
    }
    body.appendChild(table)
  })

  socket.on('setModel', function(x,y,modelName,player){
    setModelPosition(x,y,modelName,player)
  })

  socket.emit("ready")
}

function setModelPosition(x,y,modelName,player){
  console.log(modelName,x,y)
    var celltoChange = tableList[y * widthG + x]
    celltoChange.innerHTML = '<p class = "player' +  player + '">'+ modelName + "</p>"
  //celltoChange.innerHTML = '<a href = "#" class = "player' +  player + '" onclick="moveModel(event)">'+ modelName + "</a>"
    if(currentModels[modelName] == undefined){
      currentModels[modelName] = y * widthG + x
    }else{
      var _y = Math.floor(currentModels[modelName] / widthG)
      var _x = Math.round(((currentModels[modelName] / widthG) - _y) * widthG)
      if(x == _x && y == _y){
        
      }else{
        tableList[currentModels[modelName]].innerHTML = _x + "," + _y
        currentModels[modelName] = y * widthG + x
      }
    }
  }

function moveModel(e){
  e.preventDefault()
  var target = e.target
  console.log(target)
  var player = parseInt(target.className.split("player")[1])
  console.log(player)
  if(!isNaN(player) && !selected){
    selected = true;
    selectedModel = target.innerHTML
    selectedModelPlayer = target.classList[0].split("player")[1]
    return
  }
  if(selected && isNaN(player)){
    selected = false;
    var posString = target.id;
    var pos = posString.split(",")
    console.log(pos)
    setModelPosition(parseInt(pos[0]),parseInt(pos[1]),selectedModel,selectedModelPlayer)
  }else if(selected){
    selected = false;
  }
}






