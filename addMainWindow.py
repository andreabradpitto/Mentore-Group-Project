from PyQt5 import QtCore, QtWidgets
from mentorePalette import mentorePaletteSetter
from pageWindow import PageWindow


class AddMainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add menu")
        self.setObjectName("AddWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(150, 50, 351, 81))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText(
            "<html><head/><body><p align=\"center\">Something goes here...</p></body></html>")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(250, 285, 160, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.addVLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.addVLayout.setContentsMargins(0, 0, 0, 0)
        self.addVLayout.setObjectName("addVLayout")
        self.addSentence_pb = QtWidgets.QPushButton(
            "Add sentence", self.verticalLayoutWidget)
        self.addSentence_pb.setObjectName("addSentence_pb")
        self.addSentence_pb.clicked.connect(self.goToAddSentence)
        self.addVLayout.addWidget(self.addSentence_pb)
        self.addQuestion_pb = QtWidgets.QPushButton(
            "Add question", self.verticalLayoutWidget)
        self.addQuestion_pb.setObjectName("addQuestion_pb")
        self.addQuestion_pb.clicked.connect(self.goToAddQuestion)
        self.addVLayout.addWidget(self.addQuestion_pb)
        self.back_pb = QtWidgets.QPushButton("< Back", self.centralwidget)
        self.back_pb.setGeometry(QtCore.QRect(510, 380, 106, 30))
        self.back_pb.setObjectName("back_pb")
        self.back_pb.clicked.connect(self.goToMain)
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

    def goToMain(self):
        self.goto("main")

    def goToAddSentence(self):
        self.goto("addSentence")

    def goToAddQuestion(self):
        self.goto("addQuestion")
