var htmlDiv = $("#main");
var width = htmlDiv.width();
var height = width * 1.2;
htmlDiv.height(height);
var svg = d3.select("#main").append("svg")
  .attr("width", width).attr("height", height);
var lineCount = 20;
var padding = width / (lineCount + 1);

var rectGroup = svg.append("g")
  .attr("width", width).attr("height", width).attr("class", "rectGroup");
var scoreboardGroup = svg.append("g")
  .attr("transform", "translate(" + padding + "," + width + ")")
  .attr("width", width).attr("height", width * 0.2);
var text1 = scoreboardGroup.append("text").text("READY").attr("dy", 35).style("font-size", 60);

function getLocation(position) {
  return padding * position + padding;
}

for (var i = 0; i < 20; i++) {
  rectGroup.append('line')
    .attr('x1', getLocation(0))
    .attr('y1', getLocation(i))
    .attr('x2', getLocation(19))
    .attr('y2', getLocation(i))
    .attr('stroke', 'black')
    .attr('stroke-width', 1);
  rectGroup.append('line')
    .attr('y1', getLocation(0))
    .attr('x1', getLocation(i))
    .attr('y2', getLocation(19))
    .attr('x2', getLocation(i))
    .attr('stroke', 'black')
    .attr('stroke-width', 1);
}

var counter = 0;
var data = document.getElementById("output").textContent.split("\n");

function Drop(value, x, y) {
  console.log(x + " " +  y +  " " + value);
  rectGroup.append('circle')
    .attr('cx', getLocation(x))
    .attr('cy', getLocation(y))
    .attr('r', padding * (1 - 0.618))
    .attr('fill', value == 1 ? "white" : "black")
    .attr('stroke', 'black')
    .attr('stroke-width', 1);
  text1.text((value == 1 ? "WHITE" : "BLACK") + ": (" + x + ", " + y + ")");
}

var timer = setInterval(function () {
  if (counter < data.length - 1) {
    eval(data[counter++]);
  }
  else clearInterval(timer);
}, 1000);