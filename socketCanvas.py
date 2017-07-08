import sys
from PyQt5.QtWidgets import QApplication, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setWindowTitle('Hello World!')


if __name__ is '__main__':
    app = QApplication(sys.argv)
    mainWindow = MyWidget()
    sys.exit(app.exec_())
