from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from VectorSender import VectorSender

class SimpleEcho(WebSocket):
    """def __init__(self, type1, type2, server, sock, address):
        super().__init__(server, sock, address)"""


    def handleMessage(self):
        if self.data is None:
            self.data = ''

        # echo message back to client
        self.vectorSender = VectorSender(self)
        self.sendMessage(str(self.data))

    def send(self, data):
        self.sendMessage(data)
    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 9073, SimpleEcho)
server.serveforever()