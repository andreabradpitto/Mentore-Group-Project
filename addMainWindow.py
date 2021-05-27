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
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(320, 205, 160, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.addVLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.addVLayout.setContentsMargins(0, 0, 0, 0)
        self.addVLayout.setObjectName("addVLayout")
        self.addSentence_pb = QtWidgets.QPushButton(
            "Add sentence", self.verticalLayoutWidget)
        self.addSentence_pb.setObjectName("addSentence_pb")
        self.addSentence_pb.clicked.connect(self.goToAddSentence)
        self.addVLayout.addWidget(self.addSentence_pb)
        self.addContQuestion_pb = QtWidgets.QPushButton(
            "Add cont. question", self.verticalLayoutWidget)
        self.addContQuestion_pb.setObjectName("addContQuestion_pb")
        self.addContQuestion_pb.clicked.connect(self.goToAddContQuestion)
        self.addQuestion_pb = QtWidgets.QPushButton(
            "Add question", self.centralwidget)
        self.addQuestion_pb.setGeometry(QtCore.QRect(150, 245, 160, 27))
        self.addQuestion_pb.setObjectName("addQuestion_pb")
        self.addQuestion_pb.clicked.connect(self.goToAddQuestion)
        self.addGoalQuestion_pb = QtWidgets.QPushButton(
            "Add goal question", self.centralwidget)
        self.addGoalQuestion_pb.setGeometry(QtCore.QRect(490, 245, 160, 27))
        self.addGoalQuestion_pb.setObjectName("addGoalQuestion_pb")
        self.addGoalQuestion_pb.clicked.connect(self.goToAddGoalQuestion)
        self.addVLayout.addWidget(self.addContQuestion_pb)
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

    def goToAddContQuestion(self):
        self.goto("addContQuestion")

    def goToAddGoalQuestion(self):
        self.goto("addGoalQuestion")
