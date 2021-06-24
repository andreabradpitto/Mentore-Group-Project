from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class AddQuestionWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initPageUI()

    def initPageUI(self):
        self.setWindowTitle("Add question")
        self.setObjectName("AddQuestionWindow")

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
        self.mainLabel.setGeometry(QtCore.QRect(40, 90, 701, 31))
        self.mainLabel.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">"
                               "Please enter a new plain question</span></p></body></html>")
        self.questionLabel = QtWidgets.QLabel(self.centralwidget)
        self.questionLabel.setGeometry(QtCore.QRect(42, 140, 181, 21))
        self.questionLabel.setObjectName("questionLabel")
        self.questionLabel.setText(
            "<html><head/><body><p align=\"center\">Question:</p></body></html>")
        self.question_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.question_lineEdit.setGeometry(QtCore.QRect(50, 170, 500, 29))
        self.question_lineEdit.setObjectName("question_lineEdit")
        self.answer_present = 0
        self.plain_checkBox = QtWidgets.QCheckBox(
            "Plain question", self.centralwidget)
        self.plain_checkBox.setGeometry(QtCore.QRect(560, 170, 181, 27))
        self.plain_checkBox.setObjectName("plain_checkBox")
        self.plain_checkBox.setChecked(1)
        self.plain_checkBox.clicked.connect(self.resetGoalCont)
        self.goal_checkBox = QtWidgets.QCheckBox(
            "Goal question", self.centralwidget)
        self.goal_checkBox.setGeometry(QtCore.QRect(560, 190, 181, 27))
        self.goal_checkBox.setObjectName("goal_checkBox")
        self.goal_checkBox.clicked.connect(self.resetPlainCont)
        self.contextual_checkBox = QtWidgets.QCheckBox(
            "Contextual question", self.centralwidget)
        self.contextual_checkBox.setGeometry(QtCore.QRect(560, 210, 181, 27))
        self.contextual_checkBox.setObjectName("contextual_checkBox")
        self.contextual_checkBox.clicked.connect(self.resetPlainGoal)
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def resetGoalCont(self):
        self.goal_checkBox.setChecked(0)
        self.contextual_checkBox.setChecked(0)
        if self.answer_present == 1:
            self.answerLabel.hide()
            self.answer_lineEdit.hide()
            self.answer_present = 0
        self.mainLabel.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">"
                               "Please enter a new plain question</span></p></body></html>")

    def resetPlainCont(self):
        self.plain_checkBox.setChecked(0)
        self.contextual_checkBox.setChecked(0)
        if self.answer_present == 1:
            self.answerLabel.hide()
            self.answer_lineEdit.hide()
            self.answer_present = 0
        self.mainLabel.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">"
                               "Please enter a new goal question</span></p></body></html>")

    def resetPlainGoal(self):
        self.plain_checkBox.setChecked(0)
        self.goal_checkBox.setChecked(0)
        self.answerLabel = QtWidgets.QLabel(self.centralwidget)
        self.answerLabel.setGeometry(QtCore.QRect(42, 240, 181, 21))
        self.answerLabel.setObjectName("answerLabel")
        self.answerLabel.setText(
            "<html><head/><body><p align=\"center\">Answer:</p></body></html>")
        self.answer_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.answer_lineEdit.setGeometry(QtCore.QRect(50, 270, 500, 29))
        self.answer_lineEdit.setObjectName("answer_lineEdit")
        self.answerLabel.show()
        self.answer_lineEdit.show()
        self.answer_present = 1
        self.mainLabel.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">"
                               "Please enter a new contextual question and its answer</span></p></body></html>")

    def goToAddMain(self):
        self.question_lineEdit.clear()
        self.answer_lineEdit.clear()
        self.plain_checkBox.setChecked(1)
        self.resetGoalCont()
        self.goto("add")
