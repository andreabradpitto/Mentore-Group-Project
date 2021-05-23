from PyQt5 import QtCore, QtGui, QtWidgets
import mainMentore
import addMentore

class windowController:
    def __init__(self):
        self.mainWindow = mainMentore.MainWindow()
        self.addWindow = addMentore.addWindow()

        self.mainWindow.closed.connect(self.addWindow.show())
        self.mentoreWindow.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    controller = windowController()

    sys.exit(app.exec_())