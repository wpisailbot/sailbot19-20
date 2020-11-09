const express = require('express');
const http = require('http');
const socketIO = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);
const port = 3000;

let db = [];

app.use(express.static('public'));

io.on('connection', (socket) => {
	socket.on('client', () => socket.join('clients'));

	socket.on('data', (data) => {
		io.to('clients').emit('updateDash', data);
		addToDB(data);
	});

	console.log('User Connected:', socket.id);
});

const addToDB = (data) => {
	db.push(data); // implement real online and offline database eventually
}

server.listen(port, () => console.log('Listening on port: ' + port));