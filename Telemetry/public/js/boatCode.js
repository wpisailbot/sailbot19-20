const socket = io(); // socket initialization



// socket.emit('data', mockData); // sending to the server under the data socket

let dataInterval;

const stopMessages = () => {
	clearInterval(dataInterval);
	document.querySelector('#but').onclick = sendMockMessages;
	document.querySelector('#message').innerHTML = 'Click the button to start sending messages!';
	document.querySelector('#but').innerHTML = 'Send';
}

// sends data every 500ms
const sendMockMessages = () => {
	// timeout variable holds the timeout
	dataInterval = setInterval(() => socket.emit('data', {
		apparentWind: {speed: 10 + Math.floor(Math.random() * 50), direction: Math.floor(Math.random() * 295)},
		theoreticalWind: {speed: 10 + Math.floor(Math.random() * 50), direction: Math.floor(Math.random() * 295)},
		compass: {x: Math.floor(Math.random() * 360), y: Math.floor(Math.random() * 360), z: 'garbo'}, 
		airtemp: Math.floor(Math.random() * 35),
		windchill: Math.floor(Math.random() * 35),
		pressure: 950 + Math.floor(Math.random() * 100),
		groundspeed: Math.floor(Math.random() * 25),
		gps: {latitude: Math.floor(Math.random() * 100000)/1000, longitude: Math.floor(Math.random() * 100000)/1000, altitude: Math.floor(Math.random() * 100000)/1000}, 
		pitchroll: {pitch: Math.floor(Math.random() * 20) - 20, roll: Math.floor(Math.random() * 180) - 90},
		gyro: {phi: Math.floor(Math.random() * 100000)/1000, theta: Math.floor(Math.random() * 100000)/1000, psi: Math.floor(Math.random() * 100000)/1000}
	}), 1000);

	document.querySelector('#message').innerHTML = 'Sending...';
	document.querySelector('#but').innerHTML = 'Stop Sending';
	document.querySelector('#but').onclick = stopMessages;
}
