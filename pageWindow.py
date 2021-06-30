from PyQt5 import QtCore, QtWidgets


class PageWindow(QtWidgets.QMainWindow):

    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name: str) -> None:
        self.gotoSignal.emit(name)
