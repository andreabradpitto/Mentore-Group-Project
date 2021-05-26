from PyQt5 import QtCore, QtWidgets


class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name: str) -> None:
        self.gotoSignal.emit(name)

    def initBarUI(self) -> None:
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu("Help", self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setStyleSheet("border-top: 1px solid")
        self.statusbarLabelIntro = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.statusbarLabelIntro)
        self.statusbarLabelIntro.setText("Selected Class:")
        self.statusbarLabelIntro.setStyleSheet("border-top: 0px")
        self.statusbarLabel = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.statusbarLabel)
        self.statusbarLabel.setText("none")
        self.statusbarLabel.setStyleSheet("border-top: 0px")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())
