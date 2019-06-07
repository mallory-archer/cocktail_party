var margin = {top: 30, right: 50, bottom: 30, left: 50};
var width = 960 - margin.left - margin.right;
var height = 500 - margin.top - margin.bottom;

var svgContainer_wc = d3.select("#wordcloud_loc").append("svg:svg")
		.attr("width", 700)
		.attr("height", 500)
        .append("g");
		
//d3.json("wordcloud_objects_all_test.json", function (error, data){
d3.json("test_json.json", function (error, data){
			if (error) throw error;
			
			console.log(data);
			
			var color = d3.scaleOrdinal(d3.schemeCategory20);
			
			var categories = d3.keys(d3.nest().key(function(d) {return d["name"]; }).map(data));
			
			console.log(d3.keys(data["+447825029400"]));
			// var categories = d3.keys(d3.nest().key(function(d) {return d;}).map(d3.keys(data["+447825029400"])));
			
			console.log(categories);
			var fontSize = d3.scalePow().exponent(5).domain([0,1]).range([40,80]);
			//var fontStyle = d3.scaleLinear().domain([categories]).range([0,1]);

var layout = d3.layout.cloud()
      .size([width, height])
      .timeInterval(20)
      .words(data)
      .rotate(function(d) { return 0; })
      .fontSize(function(d,i) { return fontSize(Math.random()); })
      .fontWeight(["bold"])
      .text(function(d) { console.log(d.name); return d.name; })
      .spiral("rectangular") // "archimedean" or "rectangular"
      .on("end", draw)
      .start();
/*
var layout = d3.layout.cloud()
      .size([width, height])
      .timeInterval(20)
      .words(d3.keys(data["+447825029400"]))
      .rotate(function(d) { return 0; })
      .fontSize(function(d,i) { return fontSize(Math.random()); })
      .fontWeight(["bold"])
      .text(function(d) { console.log(d); return d; })
      .spiral("rectangular") // "archimedean" or "rectangular"
      .on("end", draw)
      .start();
*/

	 console.log(layout.size.length) 
	  
var wordcloud = svgContainer_wc.append("g")
      .attr('class','wordcloud')
      .attr("transform", "translate(" + width/2 + "," + height/2 + ")");
      
   svgContainer_wc.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .selectAll('text')
      .style('font-size','20px')
      .style('fill',function(d) { return color(d); })
      .style('font','sans-serif');

function draw(words) {
    wordcloud.selectAll("text")
        .data(words)
        .enter().append("text")
        .attr('class','word')
        .style("fill", function(d, i) { return color(i); })
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", function(d) { return d.font; })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
        .text(function(d) { return d.text; });
};
  
});