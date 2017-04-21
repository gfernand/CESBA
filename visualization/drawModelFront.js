
var MapVisualization = function(width, height, gridWidth, gridHeight, context) {
	var width = width;
	var height = height;
	var context = context;
	// Find cell size:
	var cellWidth = Math.floor(width / gridWidth);
	var cellHeight = Math.floor(height / gridHeight);
	var maxR = Math.min(cellHeight, cellWidth)/2 - 1;

	// Draws walls
	this.drawRooms = function(array_rooms){
		context.font = "15px Arial"
		rooms = array_rooms;
		for (var i in rooms){
			var room = rooms[i];
			room.y = gridHeight - room.y - 1;
			if(room.type != 'out'){
				for(var i=0; i < 4; i++){
					this.drawRectangle(room.x, room.y, 1, 1,"Brown", false);
				}
				this.drawRectangle(room.x, room.y, 1, 1,"Brown", false , room.text, "black");
			}
			else{
				var cx = (room.x + 0.5) * cellWidth;
                var cy = (room.y + 0.5) * cellHeight;
                context.fillStyle = 'black';
                context.textAlign = 'center';
                context.textBaseline= 'middle';
                context.fillText(room.text, cx, cy);
			}
			context.font = "20px Arial"
			var cx = (room.x + 0.25) * cellWidth;
			var cy = (room.y + 0.35) * cellHeight;
			color = 'blue'
			if(room.perAgents > 50){
				color = 'red'
			}		
            context.fillStyle = color;
            context.textAlign = 'right';
            context.textBaseline = 'bottom';
            context.fillText(room.nAgents, cx, cy);
            context.font = "15px Arial"
            if(room.type != 'out'){
	            var cx = (room.x + 0.75) * cellWidth;
				var cy = (room.y + 0.35) * cellHeight;
				color = 'green'
	            context.fillStyle = color;
	            context.textAlign = 'left';
	            context.textBaseline = 'bottom';
	            context.fillText(room.TZ, cx, cy);
	            var cx = (room.x + 0.25) * cellWidth;
				var cy = (room.y + 0.75) * cellHeight;
				color = 'red'
	            context.fillStyle = color;
	            context.textAlign = 'left';
	            context.textBaseline = 'bottom';
	            context.fillText(room.tra, cx, cy);
	            var cx = (room.x + 0.75) * cellWidth;
				var cy = (room.y + 0.75) * cellHeight;
				color = 'blue'
	            context.fillStyle = color;
	            context.textAlign = 'left';
	            context.textBaseline = 'bottom';
	            context.fillText(room.comfort, cx, cy);
        	}
		}
		for (var o in rooms){
			for (var p in rooms){
				var room1 = rooms[o]
				var room2 = rooms[p]
				adj = this.areAdj(room1, room2)
				if (adj){
					if (room1.name == room2.name){
						if(room1.y == room2.y){
							x = (room1.x + room2.x + 1)/2
							y1 = room1.y 
							y2 = room1.y + 1
							for(var i=0; i < 6; i++){
								this.drawLine(x, y1, x, y2, '#eee');
							}
						}
						if(room1.x == room2.x){
							y = (room1.y + room2.y + 1)/2
							x1 = room1.x
							x2 = room1.x + 1
							for(var i=0; i < 6; i++){
								this.drawLine(x1, y, x2, y, '#eee');
							}
						}
					}
				}
			}
		}
	}
	
	this.areAdj = function(room1, room2){
		x1 = room1.x
		y1 = room1.y
		adj = false
		if (room2.x == room1.x){
			if (room2.y == (room1.y+1) || room2.y == (room1.y-1))
				adj = true
		}
		if (room2.y == room1.y){
			if (room2.x == (room1.x+1) || room2.x == (room1.x-1))
				adj = true
		}
		return adj

	}

	// Draws doors
	this.drawDoors = function(array_doors){
		doors = array_doors;
		for (var i in doors){
			var door = doors[i];
			console.log(door)
			var yDraw = 0
			var xDraw = 0
			if(door.x1 == door.x2){
				xDraw = door.x1;
				yDraw = (door.y1 + door.y2)/2;
				yDraw = gridHeight - yDraw - 1;
				console.log(yDraw)
				var color = "red";
				if (door.state == true){
					color = "Green";
				}
				this.drawRectangle(xDraw, yDraw, 0.25, 0.05, color, true);
			}
			if(door.y1 == door.y2){
				yDraw = door.y1;
				xDraw = (door.x1 + door.x2)/2;
				yDraw = gridHeight - yDraw - 1;
				console.log(yDraw)
				var color = "red";
				if (door.state == true){
					color = "Green";
				}
				this.drawRectangle(xDraw, yDraw, 0.05, 0.25, color, true);
			}
		}	
	}

	// Calls the appropriate shape(agent)
    this.drawLayer = function(portrayalLayer) {
		for (var i in portrayalLayer) {
			var p = portrayalLayer[i];

	            p.y = gridHeight - p.y - 1;
				if (p.Shape == "rect"){
					w = 1
					h = 1
					this.drawRectangle(p.x, p.y, w, h, p.Color, p.Filled, p.text, p.text_color);
				}
				else if (p.Shape == "circle"){
					this.drawCircle(p.x, p.y, p.r, p.Color, p.Filled, p.text, p.text_color);
				}
	            else if (p.Shape == "arrowHead"){
					this.drawArrowHead(p.x, p.y, p.heading_x, p.heading_y, p.scale, p.Color, p.Filled, p.text, p.text_color);
	            }
			
		}
	};




	this.drawLine = function(x1,y1,x2,y2,color) {
		var dx1 = x1 * cellWidth;
		var dy1 = y1 * cellHeight;
		var dx2 = x2 * cellWidth;
		var dy2 = y2 * cellHeight;

		context.beginPath();
		context.moveTo(dx1, dy1);
		context.lineTo(dx2, dy2);
		context.lineWidth = 1;
		context.strokeStyle = color;
		context.stroke();

	};



	this.drawCircle = function(x, y, radius, color, fill, text, text_color) {
		var cx = (x + 0.5) * cellWidth;
		var cy = (y + 0.5) * cellHeight;
		var r = radius * maxR

		context.beginPath();
		context.arc(cx, cy, r, 0, Math.PI * 2, false);
		context.closePath();

		context.strokeStyle = color;
		context.stroke();

		if (fill) {
			context.fillStyle = color;
			context.fill();
		}

                // This part draws the text inside the Circle
                if (text !== undefined) {
                        context.fillStyle = text_color;
                        context.textAlign = 'center';
                        context.textBaseline= 'middle';
                        context.fillText(text, cx, cy);
                }

	};

	this.drawRectangle = function(x, y, w, h, color, fill, text, text_color) {
		context.beginPath();
		var dx = w * cellWidth;
		var dy = h * cellHeight;

		// Keep in the center of the cell:
		var x0 = (x + 0.5) * cellWidth - dx/2;
		var y0 = (y + 0.5) * cellHeight - dy/2;

		context.strokeStyle = color;
		context.fillStyle = color;
		if (fill)
			context.fillRect(x0, y0, dx, dy);
		else
			context.strokeRect(x0, y0, dx, dy);

                // This part draws the text inside the Rectangle
                if (text !== undefined) {
                        var cx = (x + 0.5) * cellWidth;
                        var cy = (y + 0.5) * cellHeight;
                        context.fillStyle = text_color;
                        context.textAlign = 'center';
                        context.textBaseline= 'middle';
                        context.fillText(text, cx, cy);
                }
	};


    this.drawGridLines = function() {
    	context.beginPath();
		context.strokeStyle = "#eee";
		maxX = cellWidth * gridWidth;
		maxY = cellHeight * gridHeight;

		// Draw horizontal grid lines:
		for(var y=0; y<=maxY; y+=cellHeight) {
			context.moveTo(0, y+0.5);
			context.lineTo(maxX, y+0.5);
		}

		for(var x=0; x<=maxX; x+= cellWidth) {
			context.moveTo(x+0.5, 0);
			context.lineTo(x+0.5, maxY);
		}
		context.stroke();
	};

	this.resetCanvas = function() {
		context.clearRect(0, 0, width, height);
		context.beginPath();
	};

};

var CanvasModule = function(canvas_width, canvas_height, grid_width, grid_height) {
	// Create the element
	// ------------------

	// Create the tag:
	var canvas_tag = "<canvas width='" + canvas_width + "' height='" + canvas_height + "' ";
	canvas_tag += "style='border:1px dotted'></canvas>";
	// Append it to body:
	var canvas = $(canvas_tag)[0];
	$("body").append(canvas);

	// Create the context and the drawing controller:
	var context = canvas.getContext("2d");
	var canvasDraw = new MapVisualization(canvas_width, canvas_height, grid_width, grid_height, context);

	this.render = function(data) {
		canvasDraw.resetCanvas();
		canvasDraw.drawGridLines();
		canvasDraw.drawRooms(data[10]);
		canvasDraw.drawDoors(data[20]);
			for (var layer in data)
		canvasDraw.drawLayer(data[layer]);
	};

	this.reset = function() {
		canvasDraw.resetCanvas();
	};

};

var GraphVisualization = function() {

    	// Watch
    var wacth_tag_script = "<script type=\"text/javascript\" src=\"canvasjs.min.js\"></script><script>function setTime(time){document.getElementById(\"wacth\").innerHTML = time;}</script>"
    var wacth_tag_body = "<div id = \"wacth\"><div>"
    $("head").append(wacth_tag_script);
    $("body").append(wacth_tag_body);


    	// Value by step
        
        var chart_tag1 = "<div id=\"chartContainer1\" style=\"height: 200px; width:100%;\">hola</div>";

   	// Append it to body:
    var chart1 = chart_tag1;
    $("body").append(chart1);

    var chart_tag2 = "<script type=\"text/javascript\">";
    chart_tag2 +="var dps = [];";
    chart_tag2 += "var chart1 = new CanvasJS.Chart(\"chartContainer1\",{title :{text:\"Consumed Energy\"},data: [{type: \"line\",dataPoints: dps}]});";
    chart_tag2 += "var xVal = 0;var grapho = function(x, y) {var dataLength = 1500;";
    chart_tag2 += "var updateChart = function (count) {count = count || 1;";
    chart_tag2 += "dps.push({x: x,y: y});";
    chart_tag2 += "chart1.render();};updateChart(dataLength);";
    chart_tag2 += "}";
    chart_tag2 += "</script>";

    // Append it to head:
    var chart2 = chart_tag2;
    $("head").append(chart2);

    
    	// Value by day
    var chart_tag4 = "<div id=\"chartContainer2\" style=\"height: 200px; width:100%;\"></div>";

   	// Append it to body:
    var chart4 = chart_tag4;
    $("body").append(chart4);

    var chart_tag3 = "<script type=\"text/javascript\">";
    chart_tag3 += "var currentDay = 0;var chart2 = 0; var value1 = 0; var value2 = 0; var value3 = 0; var value4 = 0; var value5 = 0; var value6 = 0; var value7 = 0; var value8 = 0; var value9 = 0; var value10 = 0; var value11 = 0; var value12 = 0;var value13 = 0;var value14 = 0;var value15 = 0;var value15 = 0;";
    chart_tag3 += "var rend = function(){chart2 = new CanvasJS.Chart(\"chartContainer2\",{title:{text: \"Consumed Energy by Day\"},axisY:{title:\"kW\"},animationEnabled:true,";
    chart_tag3 += "data: [{type: \"stackedColumn\",toolTipContent: \"{label}<br/><span style='\\\"'color:";
    chart_tag3 += "{color};'\\\"'><strong>{name}</strong></span>: {y}kW\",name: \"PCs\",showInLegend: \"true\",dataPoints: [{  y: value1 , label: \"Day 1\"},{  y: value2,";
    chart_tag3 += "label: \"Day 2\" },{  y: value3, label: \"Day 3\" },{  y: value4, label: \"Day 4\" },{  y:value5, label: \"Day 5\"}]}, {type:";
    chart_tag3 += "\"stackedColumn\",toolTipContent: \"{label}<br/><span style='\\\"'color: {color};'\\\"'><strong>{ name}</strong></span>: {y}kW\",name: \"Lights\",showInLegend:";
    chart_tag3 += "\"true\",dataPoints: [{  y: value6 , label: \"Day 1\"},{  y: value7, label: \"Day 2\" },{  y: value8, label: \"Day 3\" },{  y: value9, label: \"Day 4\" },{  y: value10, label: \"Day 5\"}]},";
    chart_tag3 += "{type: \"stackedColumn\",toolTipContent: \"{label}<br/><span style='\\\"'color:"
    chart_tag3 += "{color};'\\\"'><strong>{name}</strong></span>: {y}kW\",name: \"HVAC\",showInLegend: \"true\",dataPoints: [{  y: value11 , label: \"Day 1\"},{  y: value12,"
    chart_tag3 += "label: \"Day 2\" },{  y: value13, label: \"Day 3\" },{  y: value14, label: \"Day 4\" },{  y:value15, label: \"Day 5\"}]}"
    chart_tag3 += "],legend:{cursor:\"pointer\",itemclick: function(e){if (typeof (e.dataSeries.visible) ===  \"undefined\" || e.dataSeries.visible) {e.dataSeries.visible = true;}";
	chart_tag3 +=" else{e.dataSeries.visible = true;}chart2.render();}}});chart2.render();};rend();";
    chart_tag3 += "</script>";

    // Append it to head:
    var chart3 = chart_tag3;
    $("head").append(chart3);



    this.render = function(data){
    	grap = data[1] +24*data[0];
    	grapho(grap, data[2]);
    	time = 'Day '+ (data[0]+1)+' - Hour.Minute: '+ data[1];
    	setTime(time);

    	//PCLightHVAC By Day
    	value1 = data[3][0];
    	value2 = data[3][1];
    	value3 = data[3][2];
    	value4 = data[3][3];
    	value5 = data[3][4];
    	value6 = data[4][0];
    	value7 = data[4][1];
    	value8 = data[4][2];
    	value9	= data[4][3];
    	value10	= data[4][4];
    	value11 = data[5][0];
    	value12 = data[5][1];
    	value13 = data[5][2];
    	value14	= data[5][3];
    	value15	= data[5][4];
    	if (currentDay != data[0]){
    	currentDay = data[0];
		rend();
		}
   	}


    this.reset = function() {
       
    };
};
