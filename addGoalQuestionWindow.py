from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class AddGoalQuestionWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initPageUI()

    def initPageUI(self):
        self.setWindowTitle("Add goal question")
        self.setObjectName("AddGoalQuestionWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.add_pb = QtWidgets.QPushButton("Add", self.centralwidget)
        self.add_pb.setGeometry(QtCore.QRect(630, 370, 106, 30))
        self.add_pb.setObjectName("add_pb")
        self.cancel_pb = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_pb.setGeometry(QtCore.QRect(505, 370, 106, 30))
        self.cancel_pb.setObjectName("cancel_pb")
        self.cancel_pb.clicked.connect(self.goToAddMain)
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(110, 50, 601, 31))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">"
                               "Please enter a question and its answer for the _____ topic</span></p></body></html>")
        self.questionLabel = QtWidgets.QLabel(self.centralwidget)
        self.questionLabel.setGeometry(QtCore.QRect(38, 170, 141, 21))
        self.questionLabel.setObjectName("questionLabel")
        self.questionLabel.setText(
            "<html><head/><body><p align=\"center\">Goal question:</p></body></html>")
        self.question_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.question_lineEdit.setGeometry(QtCore.QRect(50, 200, 500, 29))
        self.question_lineEdit.setObjectName("question_lineEdit")
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def goToAddMain(self):
        self.question_lineEdit.clear()
        self.goto("add")
