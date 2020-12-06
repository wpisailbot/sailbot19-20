let map, boatPath;


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


const initMap = () => {
    const attitash = { lat: 42.8489, lng: -70.9829 };
    // The map, centered at attitash
    map = new google.maps.Map(document.getElementById('mapCanvas'), {
        zoom: 16,
        center: attitash,
        mapTypeId: 'terrain',
        // mapTypeId: 'satellite',
        // tilt: 60,
    });

    const mockBoatPathCoords = [
        { lat: 42.849810669147935, lng: -70.98818573987138 }
    ];

    const boatSVG = {
        anchor: new google.maps.Point(200, 0),
        path: "M186.771 14.593 C 69.712 144.111,10.495 260.896,1.632 379.716 C 1.113 386.673,0.815 469.496,0.813 606.694 L 0.811 822.718 200.425 822.718 L 400.039 822.718 399.782 598.580 C 399.508 360.108,399.687 371.991,395.966 345.639 C 381.460 242.897,332.445 145.393,247.094 49.493 C 237.349 38.544,200.549 0.793,199.660 0.833 C 199.401 0.844,193.601 7.036,186.771 14.593 M219.254 69.986 C 298.936 158.616,345.383 247.655,360.672 341.084 C 365.511 370.652,365.353 366.198,365.687 482.556 L 365.995 589.858 200.442 589.858 L 34.888 589.858 34.897 489.858 C 34.902 429.782,35.231 385.971,35.722 380.122 C 44.327 277.595,94.918 173.447,189.731 63.071 L 200.719 50.281 203.874 53.335 C 205.610 55.015,212.531 62.508,219.254 69.986 M365.923 706.694 L 365.923 789.452 200.406 789.452 L 34.888 789.452 34.888 706.694 L 34.888 623.935 200.406 623.935 L 365.923 623.935 365.923 706.694",
        strokeColor: "#FFF",
        fillOpacity: 1,
        scale: 0.025,
    };

    boatPath = new google.maps.Polyline({
        path: mockBoatPathCoords,
        icons: [
                {
                    icon: {
                        path: "M 0,-1 0,1",
                        strokeColor: "#CC33FF",
                        strokeOpacity: 1,
                        scale: 4,
                    },
                    offset: "0",
                    repeat: "20px"
                },
                {
                    icon: {
                        path: "M -2,0 0,-2 2,0 0,2 z",
                        strokeColor: "#F00",
                        fillColor: "#F00",
                        fillOpacity: 1,
                      },
                    offset: "0%"
                },
                {
                    icon: boatSVG,
                    offset: "100%",
                }],
        geodesic: true,
        strokeOpacity: 0,
        map,
    });
    let mock = []
    map.addListener("click", (event) => {
        boatPath.getPath().push(event.latLng);
        console.log('{ lat: '+ event.latLng.lat() +', lng: '+ event.latLng.lng() +' }');
        mock.push('{ lat: '+ event.latLng.lat() +', lng: '+ event.latLng.lng() +' }');
        console.log(mock);
    });

    const waypoint = {
            path: 'M -2,0 a 2,2 0 1,0 4,0 a 2,2 0 1,0 -4,0',
            scale: 3,
            strokeColor: '#004d00',
            fillColor: '#00e600',
            fillOpacity: .5,
    }

    // waypoint
    new google.maps.Marker({
        position: { lat: 42.84780, lng: -70.9849 },
        icon: waypoint,
        map,
        title: 'second',
    });

    new google.maps.Marker({
        position: { lat: 42.84780, lng: -70.9809 },
        icon: waypoint,
        map,
        title: 'second',
    });

    new google.maps.Marker({
        position: { lat: 42.8499, lng: -70.9829 },
        icon: waypoint,
        map,
        title: 'second',
    });
};