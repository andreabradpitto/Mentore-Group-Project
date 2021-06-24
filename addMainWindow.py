from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class AddMainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initPageUI()

    def initPageUI(self):
        self.setWindowTitle("Add menu")
        self.setObjectName("AddWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(150, 50, 351, 81))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText(
            "<html><head/><body><p align=\"center\">Something goes here...</p></body></html>")
        self.addSentence_pb = QtWidgets.QPushButton(
            "Add sentence", self.centralwidget)
        self.addSentence_pb.setGeometry(QtCore.QRect(320, 190, 160, 27))
        self.addSentence_pb.setObjectName("addSentence_pb")
        self.addSentence_pb.clicked.connect(self.goToAddSentence)
        self.addQuestion_pb = QtWidgets.QPushButton(
            "Add question", self.centralwidget)
        self.addQuestion_pb.setGeometry(QtCore.QRect(320, 235, 160, 27))
        self.addQuestion_pb.setObjectName("addQuestion_pb")
        self.addQuestion_pb.clicked.connect(self.goToAddQuestion)
        self.back_pb = QtWidgets.QPushButton("< Back", self.centralwidget)
        self.back_pb.setGeometry(QtCore.QRect(630, 370, 106, 30))
        self.back_pb.setObjectName("back_pb")
        self.back_pb.clicked.connect(self.goToMain)
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def goToMain(self):
        self.goto("main")

    def goToAddSentence(self):
        self.goto("addSentence")

    def goToAddQuestion(self):
        self.goto("addQuestion")
