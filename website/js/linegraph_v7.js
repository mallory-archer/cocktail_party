//var select_id = document.getElementById('select_phone').value;

var form_input = document.querySelector('#select_phone');
var submit_click = document.querySelector('#select_phone_button');

function renderGraph(update, select_phone){
	console.log(update)
	console.log(select_phone)
	// Import the CSV data
	d3.csv("count_text_messages_daily.csv", function(error, data){
		if (error) throw error;
		
		//Format data
		data.forEach(function(d) {
			d.date = parseDate(d.date);
			d.count = +d.count;
			d.phone = d.phone;
			});
			
		console.log(data)
			
		//Scalethe range of the data
		xScale.domain(d3.extent(data, function(d) {return d.date}));
		yScale.domain([0, d3.max(data, function(d) {return +d.count})]);
		
		if (update) {
			svgContainer.select(".line")
			.data([data.filter(function(d) {return d.phone == select_phone;})])
			.attr("class", "line")
			.attr("d", lineGen)
			.attr("stroke", "#FF1493")
			.attr("stroke-width", 2)
			.attr("fill", "none");
			} else {
				// Add the X axis
				var xAxis = svgContainer.append("g")
				.attr("transform", "translate(0," + (HEIGHT - MARGINS.top*1.5) + ")")
				.attr("class", "x axis")
				.style("font", "16px Open Sans")
				.call(d3.axisBottom(xScale)
				.ticks(10).tickFormat(d3.timeFormat("%Y-%b")))
				.selectAll("text")
					.style("text-anchor", "end").attr("transform", "rotate(-30)");
				
				svgContainer.append("text")
				.attr("transform", "translate(" + (MARGINS.left + (WIDTH - MARGINS.left - MARGINS.right)/2) + ", " + ((HEIGHT - MARGINS.top/15)) + ")")
				.style("text-anchor", "middle")
				.style("font", "18px Open Sans")
				.text("Date");
				
				// Add the Y axis
				var yAxis = svgContainer.append("g")
				.attr("transform", "translate(" + MARGINS.left + ", 0)")
				.style("font", "16px Open Sans")
				.call(d3.axisLeft(yScale)
				.ticks(10));
				
				svgContainer.append("text")
				.attr("transform", "translate(" + MARGINS.left/3 + ", " + ((HEIGHT - MARGINS.bottom - MARGINS.top)/2 + MARGINS.bottom) + ") rotate(-90)")
				.style("text-anchor", "middle")
				.style("font", "18px Open Sans")
				.text("Number of texts");
				
				svgContainer.append("path")
				.data([data])
				.attr("class", "line")
				.attr("d", lineGen)
				.attr("stroke", "#708090")
				.attr("stroke-width", 2)
				.attr("fill", "none");
				};
		});
	}

// Set margins and dimensions
var WIDTH = 500,
	HEIGHT = 500,
	MARGINS = {
		top: 50,
		bottom: 20,
		left: 75,
		right: 20
		};

// specify variable formats
var parseDate = d3.timeParse("%m/%d/%Y");

// create scales
var xScale = d3.scaleTime().range([MARGINS.left, WIDTH - MARGINS.right]);
var	yScale = d3.scaleLinear().range([HEIGHT - MARGINS.top*1.5, MARGINS.bottom]);

// define the line	
var lineGen = d3.line()
	.x(function(d) {return xScale(d.date);})
	.y(function(d) {return yScale(d.count);}); //.curve(d3.curveCardinal);
	
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// move the 'group element to the top left margin	
var svgContainer = d3.select(count_graph).append("svg")
	.attr("width", WIDTH)
	.attr("height", HEIGHT)
	.append("g")

renderGraph(false, )


submit_click.addEventListener('click', function(event){
	event.preventDefault();
	renderGraph(true, form_input.value);
})