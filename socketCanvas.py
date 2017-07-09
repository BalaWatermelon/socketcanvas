import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt


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
        self.initUi()

    def initUi(self):
        self.setGeometry(300, 300, 280, 170)
        self.show()

    def mousePressEvent(self, event):
        self.canvas.append((event.pos().x(), event.pos().y()))
        self.update()

    def mouseMoveEvent(self, event):
        self.canvas.append((event.pos().x(), event.pos().y()))
        self.update()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.drawPoints(painter)
        painter.end()

    def drawPoints(self, painter, event=None):
        painter.setPen(Qt.red)
        for dot in self.canvas:
            painter.drawPoint(dot[0], dot[1])


if __name__ is '__main__':
    app = QApplication(sys.argv)
    mainWindow = CanvasWidget()
    sys.exit(app.exec_())
