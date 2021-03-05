import random

from Qt.QtCore import QByteArray, QDataStream, QIODevice, Qt, QTimer, Slot
from Qt.QtGui import QGuiApplication
from Qt.QtNetwork import QLocalServer
from Qt.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Server(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.server = QLocalServer(self)

        if not self.server.listen("fortune"):
            QMessageBox.critical(
                self,
                self.tr("Local Fortune Server"),
                self.tr(
                    "Unable to start the server: %s." % (self.server.errorString())
                ),
            )
            QTimer.singleShot(0, self.close)
            return

        statusLabel = QLabel()
        statusLabel.setWordWrap(True)
        statusLabel.setText(
            self.tr("The server is running.\nRun the Local Fortune Client example now.")
        )

        self.fortunes = (
            self.tr("You've been leading a dog's life. Stay off the furniture."),
            self.tr("You've got to think about tomorrow."),
            self.tr("You will be surprised by a loud noise."),
            self.tr("You will feel hungry again in another hour."),
            self.tr("You might have mail."),
            self.tr("You cannot kill time without injuring eternity."),
            self.tr("Computers are not intelligent. They only think they are."),
        )

        quitButton = QPushButton(self.tr("Quit"))
        quitButton.setAutoDefault(False)
        quitButton.clicked.connect(self.close)
        self.server.newConnection.connect(self.sendFortune)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(statusLabel)
        mainLayout.addLayout(buttonLayout)

        self.setWindowTitle(QGuiApplication.applicationDisplayName())

    @Slot()
    def sendFortune(self):
        block = QByteArray()
        out = QDataStream(block, QIODevice.WriteOnly)
        out.setVersion(QDataStream.Qt_5_10)

        message = random.choice(self.fortunes)
        out.writeUInt32(len(message))
        out.writeQString(message)

        clientConnection = self.server.nextPendingConnection()
        clientConnection.disconnected.connect(clientConnection.deleteLater)

        clientConnection.write(block)
        clientConnection.flush()
        clientConnection.disconnectFromServer()
