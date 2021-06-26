from PyQt5 import QtCore, QtWidgets


class PageWindow(QtWidgets.QMainWindow):

    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name: str) -> None:
        self.gotoSignal.emit(name)

    #def selectedConcept():

    #def conceptString():

    #def sentenceString():
        # check type out of 3

    #def questionString():
        # check type out of 3 (plus add answer string field)
