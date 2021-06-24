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
        self.addConcept_pb = QtWidgets.QPushButton(
            "Add concept", self.centralwidget)
        self.addConcept_pb.setGeometry(QtCore.QRect(320, 145, 160, 27))
        self.addConcept_pb.setObjectName("addConcept_pb")
        self.addConcept_pb.clicked.connect(self.goToAddConcept)
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

    def goToAddConcept(self):
        self.goto("addConcept")

    def goToAddSentence(self):
        self.goto("addSentence")

    def goToAddQuestion(self):
        self.goto("addQuestion")
