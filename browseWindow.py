from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class BrowseWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Select Class")
        self.setObjectName("BrowseWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.cancel_pb = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_pb.setGeometry(QtCore.QRect(560, 370, 89, 25))
        self.cancel_pb.setObjectName("cancel_pb")
        self.cancel_pb.clicked.connect(self.goToMain)
        self.concept_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.concept_lineEdit.setGeometry(QtCore.QRect(200, 210, 231, 25))
        self.concept_lineEdit.setObjectName("concept_lineEdit")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(180, 120, 381, 21))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText("<html><head/><body><p align=\"center\">Enter the Class / "
                               "Subject you want to add</p></body></html>")
        self.ok_pb = QtWidgets.QPushButton("Ok", self.centralwidget)
        self.ok_pb.setGeometry(QtCore.QRect(660, 370, 89, 25))
        self.ok_pb.setObjectName("ok_pb")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu("Help", self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())

        QtCore.QMetaObject.connectSlotsByName(self)

    def goToMain(self):
        self.goto("main")
