
import http from 'http';
import WebSocket from 'ws';

const WebSocketServer = WebSocket.Server;

const HTTP_PORT = 8443;

const httpServer = http.createServer().listen(HTTP_PORT);

// Create a server for handling websocket calls
const wss = new WebSocketServer({ server: httpServer });

wss.on('connection', function (ws) {
  ws.on('message', function (message) {
    // Broadcast any received message to all clients
    console.log('received: %s', message);
    wss.broadcast(message);
  });

  ws.on('error', () => ws.terminate());
});

wss.broadcast = function (data) {
  this.clients.forEach(function (client) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(data);
    }
  });
};

console.log(`WebRTC server is running on ${HTTP_PORT} port!`);
