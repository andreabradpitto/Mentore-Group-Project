from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class MainWindow(PageWindow):

    selectedConceptSignal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initPageUI()

    def initPageUI(self):
        self.setWindowTitle("Mentore")
        self.setObjectName("MainWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(0, 0, 800, 240))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText(
            "<html><head/><body><p align=\"center\"><span style=\"font-size:12pt\">Welcome to Mentore!<br>\
             To begin, </span><span style=\"font-size:12pt; font-weight:bold\">Browse</span> \
             <span style=\"font-size:12pt\"> for an existing subject or </span> \
             <span style=\"font-size:12pt; font-weight:bold\">Add</span><span style=\"font-size:12pt\"> something<br>\
             Press the </span><span style=\"font-size:12pt; font-weight:bold\">Help</span> \
             <span style=\"font-size:12pt\"> button at any time if you need assistance</span></p></body></html>")
        self.recentLabel = QtWidgets.QLabel(self.centralwidget)
        self.recentLabel.setGeometry(QtCore.QRect(54, 260, 180, 51))
        self.recentLabel.setObjectName("recentLabel")
        self.recentLabel.setText(
            "<html><head/><body><p align=\"center\">Recently used subjects</p></body></html>")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(64, 300, 160, 106))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.recentVLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.recentVLayout.setContentsMargins(0, 0, 0, 0)
        self.recentVLayout.setObjectName("recentVLayout")

        self.recent1_pb = QtWidgets.QPushButton(
            "recent 1", self.verticalLayoutWidget)
        self.recent1_pb.setObjectName("recent1_pb")
        self.recent1_pb.setDisabled(1)
        self.recent1_pb.clicked.connect(self.selectRecent1)
        self.recentVLayout.addWidget(self.recent1_pb)

        self.recent2_pb = QtWidgets.QPushButton(
            "recent 2", self.verticalLayoutWidget)
        self.recent2_pb.setObjectName("recent2_pb")
        self.recent2_pb.setDisabled(1)
        self.recent2_pb.clicked.connect(self.selectRecent2)
        self.recentVLayout.addWidget(self.recent2_pb)

        self.recent3_pb = QtWidgets.QPushButton(
            "recent 3", self.verticalLayoutWidget)
        self.recent3_pb.setObjectName("recent3_pb")
        self.recent3_pb.setDisabled(1)
        self.recent3_pb.clicked.connect(self.selectRecent3)
        self.recentVLayout.addWidget(self.recent3_pb)

        self.browse_pb = QtWidgets.QPushButton("Browse", self.centralwidget)
        self.browse_pb.setGeometry(QtCore.QRect(630, 325, 106, 30))
        self.browse_pb.setObjectName("browse_pb")
        self.browse_pb.clicked.connect(self.make_handleButton("browse_pb"))
        self.add_pb = QtWidgets.QPushButton("Add", self.centralwidget)
        self.add_pb.setGeometry(QtCore.QRect(630, 370, 106, 30))
        self.add_pb.setObjectName("add_pb")
        self.add_pb.clicked.connect(self.make_handleButton("add_pb"))
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def recentChecker(self, concept: str):
        if concept != self.recent1_pb.text() and concept != self.recent2_pb.text() \
                                             and concept != self.recent3_pb.text():
            if self.recent1_pb.text() == "recent 1":
                self.recent1_pb.setText(concept)
                self.recent1_pb.setDisabled(0)
            elif self.recent2_pb.text() == "recent 2":
                self.recent2_pb.setText(concept)
                self.recent2_pb.setDisabled(0)
            elif self.recent3_pb.text() == "recent 3":
                self.recent3_pb.setText(concept)
                self.recent3_pb.setDisabled(0)
            else:
                self.recent3_pb.setText(self.recent2_pb.text())
                self.recent2_pb.setText(self.recent1_pb.text())
                self.recent1_pb.setText(concept)

    def selectRecent1(self):
        conceptName = self.recent1_pb.text()
        self.selectedConceptSignal.emit(conceptName)

    def selectRecent2(self):
        conceptName = self.recent2_pb.text()
        self.selectedConceptSignal.emit(conceptName)

    def selectRecent3(self):
        conceptName = self.recent3_pb.text()
        self.selectedConceptSignal.emit(conceptName)

    def make_handleButton(self, button):
        def handleButton():
            if button == "add_pb":
                self.goto("add")
            elif button == "browse_pb":
                self.goto("browse")
        return handleButton
