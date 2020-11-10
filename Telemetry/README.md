# Telemetry

This is the Land Code for the for the Telemetry

## Usage

For the Server:
```bash
npm start
```
Navigate to [localhost:3000](http://localhost:3000) for the client dashboard

For mock data to be sent to all clients, open a new tab to [localhost:3000/boat.html](http://localhost:3000/boat.html) and close this tab when mock data should be stopped

For the mock heroku app, navigate to http://sailbot2021.herokuapp.com/ for the normal dashboard and http://sailbot2021.herokuapp.com/boat.html to start sending data to the dashboards that are open

## Descriptions

The purpose of this is to display the Relevant statistics from the sailbot on a land Computer. The Sailbot and computer should be connected to same network, possibly through the telemetry modules, and then the Sailbot should send jsons to the server into the **data** socket, using **socket.io** in the format listed below:
```json
{
	apparentWind: {speed: 0 - 55, direction: 0 - 360},
	theoreticalWind: {speed: 0 - 55, direction: 0 0- 360},
	compass: {x: 0 - 360, y: 0 - 360, z: 'unnecessary'}, 
	airtemp: 0 - 35,
	windchill: 0 - 35,
	pressure: 950 - 1050,
	groundspeed: 0 - 25,
	gps: {latitude: float, longitude: float, altitude: float},
	pitchroll: {pitch: (-20) - 20, roll: (-90) - 90,
	gyro: {phi: float, theta: float, psi: float}
}
```


