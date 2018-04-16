var htmlDiv = $("#main");
var width = htmlDiv.width();
var height = width * 1.2;
htmlDiv.height(height);
var svg = d3.select("#main").append("svg")
  .attr("width", width).attr("height", height);
var padding = 20;
var pieceWidth = (width - 5 * padding) / 4;
var rectGroup = svg.append("g")
  .attr("width", width).attr("height", width).attr("class", "scatterPlot");
var scoreboardGroup = svg.append("g")
  .attr("transform", "translate(0," + width + ")")
  .attr("width", width).attr("height", width * 0.2);
var text1 = scoreboardGroup.append("text")
  .text("Score: 0")
  .attr("x", 30)
  .attr("y", width * 0.1)
  .style("font-size", "50px")
  .attr("fill", "white");
var nowScore, nextInst;

function getLocation(position) {
  return ((position + 1) * padding) + (position * pieceWidth);
}

var background = rectGroup.append('rect')
  .attr('width', '100%')
  .attr('height', '100%')
  .attr('rx', 5)
  .attr('ry', 5)
  .style('fill', '#bbada0');

for (var i = 0; i < 4; i++) {
  for (var j = 0; j < 4; j++) {
    rectGroup.append('rect')
      .attr('x', getLocation(i))
      .attr('y', getLocation(j))
      .attr('width', pieceWidth)
      .attr('height', pieceWidth)
      .attr('rx', 5)
      .attr('ry', 5)
      .style('fill', 'rgba(238, 228, 218, 0.35)');
  }
}

var counter = 0;
var data = document.getElementById("output").textContent.split("\n");
var colors = {
  2: '#eee4da',
  4: '#ede0c8',
  8: '#f2b179',
  16: '#f59563',
  32: '#f67c5f',
  64: '#f65e3b',
  128: '#edcf72',
  256: '#edcc61',
  512: '#edc850',
  1024: '#edc53f',
  2048: 'red'
};

tileLocations = [
  [{value: 0}, {value: 0}, {value: 0}, {value: 0}],
  [{value: 0}, {value: 0}, {value: 0}, {value: 0}],
  [{value: 0}, {value: 0}, {value: 0}, {value: 0}],
  [{value: 0}, {value: 0}, {value: 0}, {value: 0}]
];

function drawTile(location, value) {
  tileLocations[location.y][location.x].rect = rectGroup.append('g').attr("class", "tiles");
  tileLocations[location.y][location.x].rect.append('rect')
    .style('fill', colors[tileLocations[location.y][location.x].value])
    .attr('x', getLocation(location.x) + pieceWidth / 2 - 15)
    .attr('y', getLocation(location.y) + pieceWidth / 2 + 20)
    .attr('width', 0)
    .attr('height', 0)
    .attr('rx', 5)
    .attr('ry', 5);
  tileLocations[location.y][location.x].rect.append('text')
    .text(tileLocations[location.y][location.x].value)
    .style('fill', '#776e65')
    .style('font-size', '50px')
    .attr('text-anchor', 'middle')
    .attr('x', getLocation(location.x) + pieceWidth / 2)
    .attr('y', getLocation(location.y) + pieceWidth / 2 + 20);
  tileLocations[location.y][location.x].rect.select('rect')
    .transition('slide')
      .attr('x', getLocation(location.x))
      .attr('y', getLocation(location.y));
  tileLocations[location.y][location.x].rect.select('rect')
    .transition('size')
      .attr('width', pieceWidth)
      .attr('height', pieceWidth);
}

function drawBoard(d) {
  rectGroup.selectAll(".tiles").remove();
  for(var i = 0; i < 4; i++) {
    for(var j = 0; j < 4; j++) {
      tileLocations[i][j].value = d[i][j];
      if (tileLocations[i][j].value > 0)
        drawTile({x: j, y: i}, tileLocations[i][j].value);
    }
  }
}

function updateScoreAndIns() {
  text1.text("Score: " + nowScore + " (next: " + nextInst + ")");
}

function score(d) {
  nowScore = d;
  updateScoreAndIns();
}

function pressKey(d) {
  nextInst = d;
  updateScoreAndIns();
}

var timer = setInterval(function () {
  if (counter < data.length - 3) {
    eval(data[counter++]);
    eval(data[counter++]);
    eval(data[counter++]);
  }
  else clearInterval(timer);
}, 1000);