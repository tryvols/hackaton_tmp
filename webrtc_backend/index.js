
import fs from 'fs';
import http from 'http';
import https from 'https';
import WebSocket from 'ws';

const WebSocketServer = WebSocket.Server;

const HTTPS_PORT = 8443;
const HTTP_PORT = 8008;

// Yes, TLS is required
const httpsServer = https.createServer({
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem'),
  passphrase: 'Nick'
});

httpsServer.listen(HTTPS_PORT);

// Create a server for handling websocket calls
const wss = new WebSocketServer({ server: httpsServer });

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

console.log(`WebRTC server is running on ${HTTPS_PORT} port!`);

// Separate server to redirect from http to https
http.createServer((req, res) => {
    console.log(req.headers['host']+req.url);
    res.writeHead(301, { "Location": "https://" + req.headers['host'] + req.url });
    res.end();
}).listen(HTTP_PORT);

console.log(`Redirect HTTP to HTTPS server is running on ${HTTP_PORT} port`);