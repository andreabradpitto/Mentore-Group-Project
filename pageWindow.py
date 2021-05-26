from PyQt5 import QtCore, QtGui, QtWidgets


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
        self.statusbarLabelOutro = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.statusbarLabelOutro)
        self.statusbarLabelOutro.setText(" ")
        self.statusbarLabelOutro.setStyleSheet("border-top: 0px")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())
        logoLabel = QtWidgets.QLabel(self)
        logoLabel.setGeometry(350, 330, 0, 0)
        logoPixmap = QtGui.QPixmap('images/mentore_logo.svg')
        logoPixmap = logoPixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        logoLabel.setPixmap(logoPixmap)
        logoLabel.resize(logoPixmap.width(), logoPixmap.height())
