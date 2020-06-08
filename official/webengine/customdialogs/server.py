from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtNetwork import QHostAddress, QTcpServer


class Server(QObject):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.m_server = QTcpServer()
        self.m_server.newConnection.connect(self.handleNewConnection)

    @pyqtSlot()
    def run(self):
        if not self.m_server.listen(QHostAddress.LocalHost, 5555):
            print(
                f"Could not start the server -> http/proxy authentication dialog will not work. Error:{self.m_server.errorString()}"
            )

    @pyqtSlot()
    def handleNewConnection(self):
        socket = self.m_server.nextPendingConnection()
        socket.disconnected.connect(socket.deleteLater)
        socket.readyRead.connect(self.handleReadReady)

    @pyqtSlot()
    def handleReadReady(self):
        socket = self.sender()
        assert socket
        msg = socket.readAll()
        if msg.contains(b"OPEN_AUTH"):
            socket.write(
                b"HTTP/1.1 401 Unauthorized\nWWW-Authenticate: "
                b'Basic realm="Very Restricted Area"\r\n\r\n'
            )
        if msg.contains(b"OPEN_PROXY"):
            socket.write(
                b"HTTP/1.1 407 Proxy Auth Required\nProxy-Authenticate: "
                b'Basic realm="Proxy requires authentication"\r\n\r\n'
            )
