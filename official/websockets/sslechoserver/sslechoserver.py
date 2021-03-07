# -*- coding: utf-8 -*-
from Qt import __binding__
from Qt.QtCore import QFile, QIODevice, QObject
from Qt.QtNetwork import (
    QHostAddress,
    QSsl,
    QSslCertificate,
    QSslConfiguration,
    QSslKey,
    QSslSocket,
)
from Qt.QtWebSockets import QWebSocketServer


class SslEchoServer(QObject):
    def __init__(self, port, parent=None):
        super().__init__(parent)

        sslConfiguration = QSslConfiguration()
        certFile = QFile(":/localhost.cert")
        keyFile = QFile(":/localhost.key")
        certFile.open(QIODevice.ReadOnly)
        keyFile.open(QIODevice.ReadOnly)
        certificate = QSslCertificate(certFile, QSsl.Pem)
        if __binding__ == "PyQt5":
            sslKey = QSslKey(keyFile, QSsl.Rsa, QSsl.Pem)
        else:
            sslKey = QSslKey(keyFile.readAll(), QSsl.Rsa, QSsl.Pem)
        certFile.close()
        keyFile.close()
        sslConfiguration.setPeerVerifyMode(QSslSocket.VerifyNone)
        sslConfiguration.setLocalCertificate(certificate)
        sslConfiguration.setPrivateKey(sslKey)

        if __binding__ == "PySide2":
            QSslConfiguration.setDefaultConfiguration(sslConfiguration)

        self.m_pWebSocketServer = QWebSocketServer(
            "SSL Echo Server", QWebSocketServer.SecureMode, self
        )

        self.m_clients = []

        if __binding__ == "PyQt5":
            self.m_pWebSocketServer.setSslConfiguration(sslConfiguration)

        if self.m_pWebSocketServer.listen(QHostAddress.Any, port):
            print("SSL Echo Server listening on port", port)
            self.m_pWebSocketServer.newConnection.connect(self.onNewConnection)
            self.m_pWebSocketServer.sslErrors.connect(self.onSslErrors)

    def onNewConnection(self):
        pSocket = self.m_pWebSocketServer.nextPendingConnection()

        print("Client connected:", pSocket.peerName(), pSocket.origin())

        pSocket.textMessageReceived.connect(self.processTextMessage)
        pSocket.binaryMessageReceived.connect(self.processBinaryMessage)
        pSocket.disconnected.connect(self.socketDisconnected)

        self.m_clients.append(pSocket)

    def processTextMessage(self, message):
        pClient = self.sender()
        if pClient is not None:
            pClient.sendTextMessage(message)

    def processBinaryMessage(self, message):
        pClient = self.sender()
        if pClient is not None:
            pClient.sendBinaryMessage(message)

    def socketDisconnected(self):
        print("Client disconnected")
        pClient = self.sender()
        if pClient is not None:
            self.m_clients.remove(pClient)
            pClient.deleteLater()

    def onSslErrors(self, errors):
        print("Ssl errors occurred")
