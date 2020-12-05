const http = require('http');
const express = require('express');
const socketIO = require('socket.io');
const bodyParser = require('body-parser');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);
const port = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(express.static('public'));

let db = [];

app.post('/boat', (req, res) => {
	console.log(req.body);
	io.to('clients').emit('updateDash', req.body);
	res.send(200);
});

// Inits Socket Connection from each client
io.on('connection', (socket) => {
	// If designated as a client, socket is sent to a room where the data will be emitted once recieved
	socket.on('client', () => socket.join('clients'));

	// once data is recieved emits to all clients in clients room
	socket.on('data', (data) => {
		io.to('clients').emit('updateDash', data);
		addToDB(data);
	});
});

// Function that will add to a database in the future
const addToDB = (data) => {
	db.push(data); // implement real online and offline database eventually
}

// Server listen function
server.listen(port, () => console.log('Listening on port: ' + port));