const socket = io(); // socket initialization

let mockData = {apparentWind: {speed: 69, direction: 60},
				theoreticalWind: {speed: 25, direction: 250},
				compass: {x: 30, y: 30, z: 30}, 
				airtemp: 15,
				windchill: 7,
				pressure: 985,
				groundspeed: 18,
				gps: {latitude: 30.91720, longitude: 3294.2910, altitude: 3000}, 
				pitchroll: {pitch: 10, roll: 30},
				gyro: {phi: 9821, theta: 0.2910, psi: 9001}};

socket.emit('data', mockData); // sending to the server under the data socket

// sends data every 500ms
setInterval(() => socket.emit('data', {
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
}), 500);