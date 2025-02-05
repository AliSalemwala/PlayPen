document.addEventListener ("DOMContentLoaded", function (){
fetch ('http://localhost:5000/alerts/alerts/')
    .then(function(response) {
      return response.json();
    }).then (function (myJson){
      var file_deets;
      Object.keys (myJson).map ((_key) => file_deets = myJson[_key]);
      var files = document.getElementById ("file-list");
      Object.keys(file_deets).map ((key) => addListItem (files, file_deets[key]))
    });
});

function addListItem (table, data){
    let row = table.insertRow();

    row.insertCell().innerHTML = data.md5;
    row.insertCell().innerHTML = data.entropy;
    row.insertCell().innerHTML = data.filesize;
    row.insertCell().innerHTML = data.timestamp;
    
    localStorage.md5Name = data.md5;

    var infobtn = document.createElement ("button");
    infobtn.className = "btn";
    infobtn.innerHTML = "<img src='../imgs/info.png'/>";
    infobtn.addEventListener ("click", () => {
      document.getElementById("heading").textContent = data.md5;
      document.getElementById("info-container").innerHTML = data.html
      document.getElementById("big-info-container").scrollIntoView({block: 'start', behavior: 'smooth'});
    });
    row.insertCell().appendChild (infobtn);

    var phylobtn = document.createElement ("button");
    phylobtn.className = "btn";
    phylobtn.innerHTML = "<img src='../imgs/smol.svg'/>";
    phylobtn.addEventListener ("click", () => {
      document.getElementById("heading").textContent = "CLOSEST FILES";
      document.getElementById("info-container").innerHTML = "";
      this.work(data.md5);
      document.getElementById("big-info-container").scrollIntoView({block: 'start', behavior: 'smooth'});
      localStorage.md5Name = data.md5;
    });
    row.insertCell().appendChild (phylobtn);
}


function work(filename){
  var width = 960,
  height = 500,
  barHeight = height / 2 - 40;
  
  var formatNumber = d3.format("s");
  
  var color = d3.scale.ordinal()
  .range(["#7fff00","#4d4dff","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"]);
  
  var svg = d3.select('#info-container').append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g")
  .attr("transform", "translate(" + width/2 + "," + height/2 + ")");
  
  d3.csv("http://localhost:8000/" + filename +".csv", function(error, data) {
    data.sort(function(a,b) { return b.value - a.value; });
  
    var extent = d3.extent(data, function(d) { return d.value; });
    
    var barScale = d3.scale.linear()
      .domain(extent)
      .range([0, barHeight]);
    
    var keys = data.map(function(d,i) { return d.name; });
    var numBars = keys.length;
    
    var x = d3.scale.linear()
      .domain(extent)
      .range([0, -barHeight]);
    
    var xAxis = d3.svg.axis()
      .scale(x).orient("left")
      .ticks(3)
      .tickFormat(formatNumber);
    
    var circles = svg.selectAll("circle")
      .data(x.ticks(3))
      .enter().append("circle")
      .attr("r", function(d) {return barScale(d);})
      .style("fill", "none")
      .style("stroke", "white")
      .style("stroke-dasharray", "2,2")
      .style("stroke-width",".5px");

    var arc = d3.svg.arc()
      .startAngle(function(d,i) { return (i * 2 * Math.PI) / numBars; })
      .endAngle(function(d,i) { return ((i + 1) * 2 * Math.PI) / numBars; })
      .innerRadius(0);

    var segments = svg.selectAll("path")
      .data(data)
      .enter().append("path")
      .each(function(d) { d.outerRadius = 0; })
      .style("fill", function (d) { return color(d.name); })
      .attr("d", arc)
      .on("click", (d) => (
        openCFGS(d)
      ));
    
    segments.transition().ease("elastic").duration(1000).delay(function(d,i) {return (25-i)*100;})
      .attrTween("d", function(d,index) {
        var i = d3.interpolate(d.outerRadius, barScale(+d.value));
        return function(t) { d.outerRadius = i(t); return arc(d,index); };
      });
    
    svg.append("circle")
      .attr("r", barHeight)
      .classed("outer", true)
      .style("fill", "none")
      .style("stroke", "black")
      .style("stroke-width","1.5px");
    
    var lines = svg.selectAll("line")
      .data(keys)
      .enter().append("line")
      .attr("y2", -barHeight - 20)
      .style("stroke", "black")
      .style("stroke-width",".5px")
      .attr("transform", function(d, i) { return "rotate(" + (i * 360 / numBars) + ")"; });
    
    svg.append("g")
      .attr("class", "x axis")
      .call(xAxis);
    
    // Labels
    var labelRadius = barHeight * 1.025;
    
    var labels = svg.append("g")
      .classed("labels", true);
    
    labels.append("def")
      .append("path")
      .attr("id", "label-path")
      .attr("d", "m0 " + -labelRadius + " a" + labelRadius + " " + labelRadius + " 0 1,1 -0.01 0");
    /*
    labels.selectAll("text")
      .data(keys)
      .enter().append("text")
      .style("text-anchor", "middle")
      .style("font-weight","bold")
      .style("fill", function(d, i) {return "#3e3e3e";})
      .append("textPath")
      .attr("xlink:href", "#label-path")
      .attr("startOffset", function(d, i) {return i * 100 / numBars + 50 / numBars + '%';})
      .text(function(d) {return d.toUpperCase(); });*/
    });
}

function openCFGS (graph){
  var temp = graph.name; 
  localStorage.neighbourName = temp.substring (temp.lastIndexOf ('/') + 1);
  popupwindow("../html/cfg.html", "Control Flow Graphs", 1000, 650);
}

function popupwindow(url, title, w, h) {
  var left = (screen.width/2)-(w/2);
  var top = (screen.height/2)-(h/2);
  return window.open(url, title, 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width='+w+', height='+h+', top='+top+', left='+left);
} 