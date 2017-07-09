import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtCore, QtNetwork
import pickle


class CanvasApplication(QMainWindow):
    def __init__(self):
        super.__init__()
        self.initUi()

    def initUi(self):
        myCanvas = CanvasWidget(parent=self)
        vbox = QVBoxLayout()
        vbox.addWidget(myCanvas)
        self.setLayout(vbox)
        self.show()


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = []
        self.buffer = []
        self.Clientsocket = QtNetwork.QTcpSocket()
        # Initialize data IO variables
        self.nextBlockSize = 0
        self.request = None

        self.Clientsocket.disconnected.connect(self.serverHasStopped)
        self.initUi()

    def SendData(self):

        TargetSystem = 'localhost'
        Msg2Send = pickle.dumps(self.buffer)
        self.buffer = []
        self.Clientsocket.connectToHost(TargetSystem, 9999)
        # This is required data to be writing
        self.Clientsocket.waitForConnected(-1)
        self.request = QtCore.QByteArray()
        stream = QtCore.QDataStream(
            self.request, QtCore.QIODevice.WriteOnly)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)
        stream.writeUInt32(0)
        stream.writeBytes(Msg2Send)
        stream.device().seek(0)
        stream.writeUInt32(self.request.size() - 4)
        self.Clientsocket.write(self.request)
        self.nextBlockSize = 0
        self.request = None
        # .close() is not closing the socket connection, so i changed it this
        self.Clientsocket.disconnectFromHost()

    def serverHasStopped(self):

        self.Clientsocket.close()

    def serverHasError(self):
        self.ServerError = self.Clientsocket.errorString()
        self.emit(QtCore.SIGNAL('SocketError'))
        self.Clientsocket.close()

    def ShowMessage():

        QtGui.QMessageBox.information(None, "Message", server.Message)

    def initUi(self):
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('happy client')
        self.show()

    def mousePressEvent(self, event):
        self.canvas.append((event.pos().x(), event.pos().y()))
        self.buffer.append((event.pos().x(), event.pos().y()))
        self.update()

    def mouseMoveEvent(self, event):
        self.canvas.append((event.pos().x(), event.pos().y()))
        self.buffer.append((event.pos().x(), event.pos().y()))
        self.update()

    def mouseReleaseEvent(self, e):
        self.SendData()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.drawPoints(painter)
        painter.end()

    def drawPoints(self, painter, event=None):
        painter.setPen(Qt.red)
        for dot in self.canvas:
            painter.drawPoint(dot[0], dot[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CanvasWidget()
    sys.exit(app.exec_())
