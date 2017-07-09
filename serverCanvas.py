import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtNetwork, QtCore
import pickle
HOST = "localhost"
PORT = 9999


class Server(QMainWindow):

    def __init__(self, host='localhost', port=9999):
        super().__init__()
        self.tcpServer = QtNetwork.QTcpServer()
        self.tcpServer.listen(QtNetwork.QHostAddress(HOST), PORT)
        self.tcpServer.newConnection.connect(self.addConnection)
        self.statusBar
        self.canvas = []
        self.initUi()

    def initUi(self):
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Server')
        self.show()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.drawPoints(painter)
        painter.end()

    def drawPoints(self, painter, event=None):
        painter.setPen(Qt.red)
        for dot in self.canvas:
            painter.drawPoint(dot[0], dot[1])

    def addConnection(self):

        try:

            self.clientConnection = self.tcpServer.nextPendingConnection()
            self.clientConnection.nextBlockSize = 0

            self.clientConnection.readyRead.connect(self.receiveMessage)
            self.clientConnection.disconnected.connect(self.removeConnection)
            self.clientConnection.error.connect(self.socketError)

        except Exception as ex:

            QtGui.QMessageBox.information(None, "Network Error", ex.message)

    def receiveMessage(self):

        if self.clientConnection.bytesAvailable() > 0:
            stream = QtCore.QDataStream(self.clientConnection)
            stream.setVersion(QtCore.QDataStream.Qt_4_2)

            if self.clientConnection.nextBlockSize == 0:

                if self.clientConnection.bytesAvailable() < 4:
                    return

                self.clientConnection.nextBlockSize = stream.readUInt32()

            if self.clientConnection.bytesAvailable() < self.clientConnection.nextBlockSize:
                return

            self.Message = stream.readBytes()
            self.clientConnection.nextBlockSize = 0
            self.clientConnection.nextBlockSize = 0
            self.canvas += pickle.loads(self.Message)
            self.update()

    def removeConnection(self):
        pass

    def socketError(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Server()
    sys.exit(app.exec_())
