const socket = io(); 
let appwind, theowind, compass, airtemp, windchill, pressure, gps, pitchroll, groundspeed, gyro, humidity;  

// inits the socket connection and joins the room for client in the server, also creates an event handler
// 	for when data is recieved

const socketInit = () => {
	socket.emit('client');

    // Creates callback for when data is recieved from the server (updates all the page components)
	socket.on('updateDash', (data) => {
	console.log(data);
	/********** Apparent Wind **********/

		let appSpeed = (data.apparentWind.speed ? data.apparentWind.speed : 60);
		let appDirection = (data.apparentWind.direction ? data.apparentWind.direction : 0);
        let appOldAngle = document.querySelector('#apparentWindVectorLine').transform.baseVal[0].angle;
		let appX = appSpeed * Math.cos(0 * (Math.PI / 180));
		let appY = appSpeed * Math.sin(0 * (Math.PI / 180));
        
        // sets the correct Length of the Vector at the 0 angle
	  	d3.select('#apparentWindVectorLine')
	    	.attr('x1', (30 - appX/2).toString())
	    	.attr('y1', (30 - appY/2).toString())
	    	.attr('x2', (30 + appX/2).toString())
	    	.attr('y2', (30 + appY/2).toString());

	    // Sets the trnsition from the vector's oldAngle to the new angle
	  	d3.select('#apparentWindVectorLine')
            .transition()
            .duration(1000)
            .ease(d3.easeElasticOut, 1, 0.9)
            .attrTween("transform", () => d3.interpolateString('rotate('+ appOldAngle +', 30, 30)', 'rotate('+ -appDirection +', 30, 30)'));

		document.querySelector('#apparentWindAngle').innerHTML = appDirection;
		document.querySelector('#apparentWindMag').innerHTML = appSpeed;

	/********** Theoretical Wind **********/

        let theoSpeed = (data.theoreticalWind.speed ? data.theoreticalWind.speed : 60);
        let theoDirection = (data.theoreticalWind.direction ? data.theoreticalWind.direction : 0);
        let theoOldAngle = document.querySelector('#theoreticalWindVectorLine').transform.baseVal[0].angle;
        let theoX = theoSpeed * Math.cos(0 * (Math.PI / 180));
        let theoY = theoSpeed * Math.sin(0 * (Math.PI / 180));
        
        // sets the correct Length of the Vector at the 0 angle
        d3.select('#theoreticalWindVectorLine')
            .attr('x1', (30 - theoX/2).toString())
            .attr('y1', (30 - theoY/2).toString())
            .attr('x2', (30 + theoX/2).toString())
            .attr('y2', (30 + theoY/2).toString());

        // Sets the trnsition from the vector's oldAngle to the new angle
        d3.select('#theoreticalWindVectorLine')
            .transition()
            .duration(1000)
            .ease(d3.easeElasticOut, 1, 0.9)
            .attrTween("transform", () => d3.interpolateString('rotate('+ theoOldAngle +', 30, 30)', 'rotate('+ -theoDirection +', 30, 30)'));

        document.querySelector('#theoreticalWindAngle').innerHTML = theoDirection;
        document.querySelector('#theoreticalWindMag').innerHTML = theoSpeed;

	/********** Compass **********/ 

		// .attr('transform', 'rotate(' + Math.atan2(data.compass.y, data.compass.x) * (180/Math.PI) + ', 50, 50) translate(17, 16) scale(0.30)');
	d3.select('#compassBoat')
            .transition()
            .duration(1000)
            .ease(d3.easeElasticOut, 1, 0.9)
            .attrTween("transform", () => d3.interpolateString('rotate('+ document.querySelector('#compassBoat').transform.baseVal[0].angle +', 50, 50) translate(17, 16) scale(0.30)', 'rotate('+ -Math.atan2(data.compass.y, data.compass.x) * (180/Math.PI) +', 50, 50) translate(17, 16) scale(0.30)'));

	/*** Air Temp **********/

	airtemp.updateGauge(data.airtemp ? data.airtemp : 0);

	/*** Wind Chill **********/

	windchill.updateGauge(data.windchill ? data.windchill : 0);

	/********** Barometric Pressure **********/

	pressure.updateGauge(data.pressure ? data.pressure : 950);
	
	/********** GPS **********/

	document.querySelector('#latitude').innerHTML = data.gps.latitude ? data.gps.latitude : 0;
	document.querySelector('#longitude').innerHTML = data.gps.longitude ? data.gps.longitude : 0;
	document.querySelector('#altitude').innerHTML = data.gps.altitude ? data.gps.altitude : 0;

	/********** Pitch and Roll **********/

		// .attr('transform', 'rotate('+ (data.pitchroll.roll ? data.pitchroll.roll : 30) +' 65, 65)');
    // d3.select('#compassBoat')
	d3.select('#rollIndicator')
        .transition()
        .duration(1000)
        .ease(d3.easeElasticOut, 1, 0.9)
        .attrTween("transform", () => d3.interpolateString('rotate('+ document.querySelector('#rollIndicator').transform.baseVal[0].angle +', 65, 65)', 'rotate('+ (data.pitchroll.roll ? data.pitchroll.roll : 30) +' 65, 65)')); 
    d3.select('#pitchIndicator')
        .transition()
        .duration(1000)
        .ease(d3.easeElasticOut, 1, 0.9)
        .attrTween("transform", () => d3.interpolateString('translate(0, '+ (document.querySelector('#pitchIndicator').transform.baseVal[0].matrix.f) +')', 'translate(0, '+ (data.pitchroll.pitch ? data.pitchroll.pitch : 0) +')'));
    console.log(document.querySelector('#pitchCircle').cy.baseVal.value - 65, data.pitchroll.pitch);
	// d3.select('#pitchIndicator')
	// 	.attr('transform', 'translate(0, '+ (data.pitchroll.pitch ? data.pitchroll.pitch : 0) +')');

	/********** Ground Speed **********/

	groundspeed.updateGauge(data.groundspeed ? data.groundspeed : 0);
	
	/********** Rate Gyro **********/

	document.querySelector('#phi').innerHTML = data.gyro.phi ? data.gyro.phi : 0;
    // d3.select('#phi')
        // .transition()
        // .textTween(() => t => data.groundspeed.toFixed(6));
	document.querySelector('#theta').innerHTML = data.gyro.theta ? data.gyro.theta : 0;
	document.querySelector('#psi').innerHTML = data.gyro.psi ? data.gyro.psi : 0;

	/********** Relative Humidity **********/

	document.querySelector('#humidityVal').innerHTML = (data.groundspeed ? data.groundspeed : 0) + '%';

	});
};


// uses dependecy (d3gauge.js) to draw all of the gauges
const gaugeInit = () => {
    // default options
	const options = {gaugeRadius: 65,
					edgeWidth: .025, 
					tickLengthMin: 0, 
					needleLengthNeg: -0.25, 
					pivotRadius: 0,
					tickEdgeGap: -.1,
					tickFont: "'Lato', sans-serif", 
					unitsFont: "'Lato', sans-serif",
					labelFontSize: 22, 
					outerEdgeCol: 'black',
					tickColMaj: 'black',
					needleCol: 'red'};

	airtemp = new drawGauge({divID: 'airtempDisp', 
							minVal: 0, 
							maxVal: 35, 
							needleVal: 0,
							tickSpaceMajVal: 5, 
							gaugeUnits: 'Celcius', 
							...options});
	windchill = new drawGauge({divID: 'windchillDisp', 
							minVal: 0, 
							maxVal: 35, 
							needleVal: 0,
							tickSpaceMajVal: 5, 
							gaugeUnits: 'Celcius', 
							...options});
	pressure = new drawGauge({divID: 'pressureDisp', 
							minVal: 950, 
							maxVal: 1050, 
							needleVal: 950,
							tickSpaceMajVal: 15, 
							gaugeUnits: 'MiliBars', 
							...options});
	groundspeed = new drawGauge({divID: 'speedDisp', 
							minVal: 0, 
							maxVal: 25, 
							needleVal: 0,
							tickSpaceMajVal: 5, 
							gaugeUnits: 'Knots', 
							...options});

};


// Create the svg using d3 and inserts it into the given div
const displayCompass = (div) => {
	d3.select('#' + div)
		.append('svg')
		.attr('id', 'svg-' + div)
        .attr('viewport', '0 0 350 350')
        .attr('height', '100px')
        .attr('width', '100px')
        .attr({'xmlns': 'http://www.w3.org/2000/svg','xmlns:xlink': 'http://www.w3.org/1999/xlink'});
    
    let svg = d3.select('#svg-' + div);

    svg.append('circle')
    	.attr('cx', '50px')
    	.attr('cy', '50px')
    	.attr('r', '48')
    	.attr('stroke', 'black')
    	.attr('stroke-width', '1')
    	.attr('fill', 'white')

    svg.append('image')
    	.attr('id', 'compassBoat')
    	.attr('href', '../assets/boat.png')
    	.attr('transform', 'translate(17, 16) scale(0.30)');
}

// creates a vector component a nd places into the given div using d3
const displayVector = (div) => {
	d3.select('#' + div)
		.append('svg')
		.attr('id', 'svg-' + div)
        .attr('viewport', '0 0 350 350')
        .attr('height', '60px')
        .attr('width', '60px')
        .attr({'xmlns': 'http://www.w3.org/2000/svg','xmlns:xlink': 'http://www.w3.org/1999/xlink'});
    
    let svg = d3.select('#svg-' + div);

    // add marker definitions
    svg.append('defs')
    	.append('marker')
    	.attr('id', 'arrowhead')
    	.attr('markerWidth', '10')
    	.attr('markerHeight', '7')
    	.attr('refX', '0')
    	.attr('refY', '3.5')
    	.attr('orient', 'auto')
    	.append('polygon')
    	.attr('points', '0 0, 10 3.5, 0 7');

    // add vector line and stuff
    let appwind = svg.append('line')
    	.attr('id', div + 'Line')
    	.attr('x1', '30')
    	.attr('y1', '60')
    	.attr('x2', '30')
    	.attr('y2', '10')
    	.attr('transform', 'rotate(0, 30, 30)')
    	.attr('stroke', '#000')
    	.attr('stroke-width', '1')
    	.attr('marker-end', 'url(#arrowhead)');

    // add middle circle for vector
    svg.append('circle')
    	.attr('cx', '30px')
    	.attr('cy', '30px')
    	.attr('r', '2');
};


// creates the pitchroll svg component using d3 and inserts into the div
const displayPitchRoll = (div) => {
	d3.select('#' + div)
		.append('svg')
		.attr('id', 'svg-' + div)
        .attr('viewport', '0 0 350 350')
        .attr('height', '130px')
        .attr('width', '130px')
        .attr({'xmlns': 'http://www.w3.org/2000/svg','xmlns:xlink': 'http://www.w3.org/1999/xlink'});

    let svg = d3.select('#svg-' + div);

    let borders = svg.append('g')
        	.attr('id','borders');

    // Outer Circle
    borders.append('circle')
        .attr('cx', 65)
        .attr('cy', 65)
        .attr('r', 64)
        .style('fill', 'white')
        .style('stroke', 'black');
    // Inner Circle
    borders.append('circle')
        .attr('cx', 65)
        .attr('cy', 65)
        .attr('r', 45)
        .style('fill', 'white')
        .style('stroke', 'black');

    // Horizontal Ticks
    let horizonTicks = svg.append('g')
    	.attr('id', 'horizonTicks');

    /************************\

    TODO: TUNE THE locations of the lines and ticks SO ITS ACTUALLY CORRECT 
    (PROBABLY 0 horizon OR SOMETHING FOR A BOAT)

    \*************************/
    horizonTicks.append('line')
    	.attr('id', 'horizon')
    	.attr('x1', 5)
    	.attr('y1', 85)
    	.attr('x2', 125)
    	.attr('y2', 85)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 1);
    horizonTicks.append('line')
    	.attr('id', '5degrees')
    	.attr('x1', 52)
    	.attr('y1', 72)
    	.attr('x2', 78)
    	.attr('y2', 72)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 1);
    horizonTicks.append('line')
    	.attr('id', '10degrees')
    	.attr('x1', 52)
    	.attr('y1', 59)
    	.attr('x2', 78)
    	.attr('y2', 59)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 1);
    horizonTicks.append('line')
    	.attr('id', '15degrees')
    	.attr('x1', 52)
    	.attr('y1', 46)
    	.attr('x2', 78)
    	.attr('y2', 46)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 1);

    // Roll ticks around the edges (corrected to the angle)
    let rollTicks = svg.append('g')
    	.attr('id', 'rollTicks');
    let largeTickLen = 19, smallTickLen = 10, innerRad = 45, center = 65;
    let angle, sin, cos;
    // A LOT OF TRIG WENT INTO FINDING THESE X'S AND Y'S

    angle = 15, sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
    rollTicks.append('line')
    	.attr('id', '15degrees')
    	.attr('x1', center + innerRad * sin)
    	.attr('y1', center - innerRad * cos)
    	.attr('x2', (center + innerRad * sin) + smallTickLen * sin)
    	.attr('y2', (center - innerRad * cos) - smallTickLen * cos)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 1);
    angle = -15, sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
    rollTicks.append('line')
    	.attr('id', '-15degrees')
    	.attr('x1', center + innerRad * sin)
    	.attr('y1', center - innerRad * cos)
    	.attr('x2', (center + innerRad * sin) + smallTickLen * sin)
    	.attr('y2', (center - innerRad * cos) - smallTickLen * cos)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 1);

    angle = 25, sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
    rollTicks.append('line')
    	.attr('id', '25degrees')
    	.attr('x1', center + innerRad * sin)
    	.attr('y1', center - innerRad * cos)
    	.attr('x2', (center + innerRad * sin) + smallTickLen * sin)
    	.attr('y2', (center - innerRad * cos) - smallTickLen * cos)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 1);
    angle = -25, sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
    rollTicks.append('line')
    	.attr('id', '-25degrees')
    	.attr('x1', center + innerRad * sin)
    	.attr('y1', center - innerRad * cos)
    	.attr('x2', (center + innerRad * sin) + smallTickLen * sin)
    	.attr('y2', (center - innerRad * cos) - smallTickLen * cos)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 1);

    angle = 45, sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
    rollTicks.append('line')
    	.attr('id', '45degrees')
    	.attr('x1', center + innerRad * sin)
    	.attr('y1', center - innerRad * cos)
    	.attr('x2', (center + innerRad * sin) + largeTickLen * sin)
    	.attr('y2', (center - innerRad * cos) - largeTickLen * cos)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 3);
    angle = -45, sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
    rollTicks.append('line')
    	.attr('id', '-45degrees')
    	.attr('x1', center + innerRad * sin)
    	.attr('y1', center - innerRad * cos)
    	.attr('x2', (center + innerRad * sin) + largeTickLen * sin)
    	.attr('y2', (center - innerRad * cos) - largeTickLen * cos)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 3);

    angle = 65, sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
    rollTicks.append('line')
    	.attr('id', '45degrees')
    	.attr('x1', center + innerRad * sin)
    	.attr('y1', center - innerRad * cos)
    	.attr('x2', (center + innerRad * sin) + largeTickLen * sin)
    	.attr('y2', (center - innerRad * cos) - largeTickLen * cos)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 3);
    angle = -65, sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
    rollTicks.append('line')
    	.attr('id', '-45degrees')
    	.attr('x1', center + innerRad * sin)
    	.attr('y1', center - innerRad * cos)
    	.attr('x2', (center + innerRad * sin) + largeTickLen * sin)
    	.attr('y2', (center - innerRad * cos) - largeTickLen * cos)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 3);

    angle = 90, sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
    rollTicks.append('line')
    	.attr('id', '45degrees')
    	.attr('x1', center + innerRad * sin)
    	.attr('y1', center - innerRad * cos)
    	.attr('x2', (center + innerRad * sin) + largeTickLen * sin)
    	.attr('y2', (center - innerRad * cos) - largeTickLen * cos)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 3);
    angle = -90, sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
    rollTicks.append('line')
    	.attr('id', '-45degrees')
    	.attr('x1', center + innerRad * sin)
    	.attr('y1', center - innerRad * cos)
    	.attr('x2', (center + innerRad * sin) + largeTickLen * sin)
    	.attr('y2', (center - innerRad * cos) - largeTickLen * cos)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 3);

    /**** TODO: ADD TICK LABELS TO THE PITCHROLL COMPONENT *****/
    // let tickLabels = svg.append('g')
    // 	.attr('id', 'tickLabels');
    // let angles = [15, 25, 45, 65, 90];

    // angles.forEach((angle) => {
	   //  let sin = Math.sin(angle * Math.PI/180), cos = Math.cos(angle * Math.PI/180);
	   //  tickLabels.append('text')
	   //  	.attr('x', 48 + 52*sin)
	   //  	.attr('y', 14 + 20/cos)
	   //      .style("font-weight", "300")
	   //      .style("font-size", "10px")
	   //      .attr("font-family", 'Lato')
	   //      .text(angle);

    // });

    // Top triangle thing in the roll part
    let centerRoll = svg.append('g')
    	.attr('id', 'centerRoll');

    centerRoll.append('polygon')
    	.attr('points', '65,20 75,2 55,2')
    	.attr('style', 'fill:DarkOrchid;');


    let movingParts = svg.append('g')
    	.attr('id', 'movingParts');

    // purple roll indicator (smaller triangle)
    movingParts.append('polygon')
    	.attr('id', 'rollIndicator')
    	.attr('points', '65,20 70,30 60,30')
    	.attr('style', 'fill:DarkOrchid;')
        .attr('transform', 'translate(0, 0)');

    let pitchIndicator = movingParts.append('g')
    	.attr('id', 'pitchIndicator')
        .attr('transform', 'translate(0, 0)');

    // path and circle code for the pitch indicator thingy
    pitchIndicator.append('path')
    	.attr('d', 'm30,72 h15 a1,1 0 0,0 39,0 h15')
    	.attr('fill', 'none')
    	.attr('stroke', 'black');
    pitchIndicator.append('circle')
        .attr('id', 'pitchCircle')
    	.attr('cx', 65)
    	.attr('cy', 74)
    	.attr('r', 2)
    	.attr('stroke', 'black')
    	.attr('stroke-width', 1);

}


// calls once when page is first loaded
window.onload = () => {
	socketInit();

	displayVector('apparentWindVector');
	displayVector('theoreticalWindVector');
	displayCompass('compassImage');
	displayPitchRoll('pitchrollDisp');
    
	gaugeInit();
};
