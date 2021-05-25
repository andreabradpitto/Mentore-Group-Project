from PyQt5 import QtCore, QtWidgets
from mentorePalette import mentorePaletteSetter
from pageWindow import PageWindow


class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Mentore")
        self.setObjectName("MainWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(150, 50, 351, 81))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText(
            "<html><head/><body><p align=\"center\">Select the class/subject to edit</p></body></html>")
        self.recentLabel = QtWidgets.QLabel(self.centralwidget)
        self.recentLabel.setGeometry(QtCore.QRect(60, 180, 141, 51))
        self.recentLabel.setObjectName("recentLabel")
        self.recentLabel.setText(
            "<html><head/><body><p align=\"center\">Recently used</p></body></html>")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 250, 160, 106))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.recentVLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.recentVLayout.setContentsMargins(0, 0, 0, 0)
        self.recentVLayout.setObjectName("recentVLayout")
        self.recent1_pb = QtWidgets.QPushButton(
            "recent 1", self.verticalLayoutWidget)
        self.recent1_pb.setObjectName("recent1_pb")
        self.recentVLayout.addWidget(self.recent1_pb)
        self.recent2_pb = QtWidgets.QPushButton(
            "recent 2", self.verticalLayoutWidget)
        self.recent2_pb.setObjectName("recent2_pb")
        self.recentVLayout.addWidget(self.recent2_pb)
        self.recent3_pb = QtWidgets.QPushButton(
            "recent 3", self.verticalLayoutWidget)
        self.recent3_pb.setObjectName("recent3_pb")
        self.recentVLayout.addWidget(self.recent3_pb)
        self.browse_pb = QtWidgets.QPushButton("Browse", self.centralwidget)
        self.browse_pb.setGeometry(QtCore.QRect(630, 270, 106, 30))
        self.browse_pb.setObjectName("browse_pb")
        self.browse_pb.clicked.connect(self.make_handleButton("browse_pb"))
        self.add_pb = QtWidgets.QPushButton("Add", self.centralwidget)
        self.add_pb.setGeometry(QtCore.QRect(630, 320, 106, 30))
        self.add_pb.setObjectName("add_pb")
        self.add_pb.clicked.connect(self.make_handleButton("add_pb"))
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu("Help", self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())

        QtCore.QMetaObject.connectSlotsByName(self)

    def make_handleButton(self, button):
        def handleButton():
            if button == "add_pb":
                self.goto("add")
            elif button == "browse_pb":
                self.goto("browse")
        return handleButton
