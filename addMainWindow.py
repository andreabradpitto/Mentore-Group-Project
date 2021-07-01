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
        self.mainLabel.setGeometry(QtCore.QRect(0, 0, 800, 180))
        self.mainLabel.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mainLabel.setObjectName("mainLabel")
        labelString = "<html><head/><body><p align=\"center\"> \
                       <span style=\"font-size:12pt\">Choose which element you want to add to the ontology</span></p></body></html>"
        self.mainLabel.setText(labelString)

        self.addConcept_pb = QtWidgets.QPushButton(
            "Add subject", self.centralwidget)
        self.addConcept_pb.setGeometry(QtCore.QRect(320, 150, 160, 27))
        self.addConcept_pb.setObjectName("addConcept_pb")
        self.addConcept_pb.clicked.connect(self.goToAddConcept)

        self.addSentence_pb = QtWidgets.QPushButton(
            "Add sentence", self.centralwidget)
        self.addSentence_pb.setGeometry(QtCore.QRect(320, 195, 160, 27))
        self.addSentence_pb.setObjectName("addSentence_pb")
        self.addSentence_pb.clicked.connect(self.goToAddSentence)
        self.addSentence_pb.setDisabled(1)

        self.addQuestion_pb = QtWidgets.QPushButton(
            "Add question", self.centralwidget)
        self.addQuestion_pb.setGeometry(QtCore.QRect(320, 240, 160, 27))
        self.addQuestion_pb.setObjectName("addQuestion_pb")
        self.addQuestion_pb.clicked.connect(self.goToAddQuestion)
        self.addQuestion_pb.setDisabled(1)

        self.back_pb = QtWidgets.QPushButton("< Back", self.centralwidget)
        self.back_pb.setGeometry(QtCore.QRect(630, 370, 106, 30))
        self.back_pb.setObjectName("back_pb")
        self.back_pb.clicked.connect(self.goToMain)

        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def buttonsEnabler(self):
        self.addSentence_pb.setDisabled(0)
        self.addQuestion_pb.setDisabled(0)

    def goToMain(self):
        self.goto("main")

    def goToAddConcept(self):
        self.goto("addConcept")

    def goToAddSentence(self):
        self.goto("addSentence")

    def goToAddQuestion(self):
        self.goto("addQuestion")
