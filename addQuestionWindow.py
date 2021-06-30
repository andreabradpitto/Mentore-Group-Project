from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class AddQuestionWindow(PageWindow):

    questionSignal = QtCore.pyqtSignal(str, str, int)    

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
        self.add_pb.clicked.connect(self.saveQuestion)
        self.cancel_pb = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_pb.setGeometry(QtCore.QRect(505, 370, 106, 30))
        self.cancel_pb.setObjectName("cancel_pb")
        self.cancel_pb.clicked.connect(self.goToAddMain)
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(0, 0, 800, 180))
        self.mainLabel.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabelUpdater("plain")
        self.questionLabel = QtWidgets.QLabel(self.centralwidget)
        self.questionLabel.setGeometry(QtCore.QRect(100, 145, 181, 21))
        self.questionLabel.setObjectName("questionLabel")
        self.questionLabel.setText(
            "<html><head/><body><p align=\"left\">Insert a question:</p></body></html>")
        self.question_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.question_lineEdit.setGeometry(QtCore.QRect(100, 170, 600, 30))
        self.question_lineEdit.setObjectName("question_lineEdit")
        self.answer_present = 0
        self.plain_checkBox = QtWidgets.QCheckBox(
            "Plain question", self.centralwidget)
        self.plain_checkBox.setGeometry(QtCore.QRect(80, 330, 181, 27))
        self.plain_checkBox.setObjectName("plain_checkBox")
        self.plain_checkBox.setChecked(1)
        self.plain_checkBox.clicked.connect(self.resetGoalCont)
        self.goal_checkBox = QtWidgets.QCheckBox(
            "Goal question", self.centralwidget)
        self.goal_checkBox.setGeometry(QtCore.QRect(80, 350, 181, 27))
        self.goal_checkBox.setObjectName("goal_checkBox")
        self.goal_checkBox.clicked.connect(self.resetPlainCont)
        self.contextual_checkBox = QtWidgets.QCheckBox(
            "Contextual question", self.centralwidget)
        self.contextual_checkBox.setGeometry(QtCore.QRect(80, 370, 181, 27))
        self.contextual_checkBox.setObjectName("contextual_checkBox")
        self.contextual_checkBox.clicked.connect(self.resetPlainGoal)
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def mainLabelUpdater(self, word: str):
        labelString = "<html><head/><body><p align=\"center\"><span style=\"font-size:12pt\">You are about to enter a new </span> \
                       <span style=\"font-size:12pt; font-weight:bold\">" + word + "</span> <span style=\"font-size:12pt\">\
                       question</span></p></body></html>"
        self.mainLabel.setText(labelString)

    def resetGoalCont(self):
        self.goal_checkBox.setChecked(0)
        self.contextual_checkBox.setChecked(0)
        if self.answer_present == 1:
            self.answerLabel.hide()
            self.answer_lineEdit.hide()
            self.answer_present = 0
        self.mainLabelUpdater("plain")
        self.plain_checkBox.setChecked(1)

    def resetPlainCont(self):
        self.plain_checkBox.setChecked(0)
        self.contextual_checkBox.setChecked(0)
        if self.answer_present == 1:
            self.answerLabel.hide()
            self.answer_lineEdit.hide()
            self.answer_present = 0
        self.mainLabelUpdater("goal")
        self.goal_checkBox.setChecked(1)

    def resetPlainGoal(self):
        self.plain_checkBox.setChecked(0)
        self.goal_checkBox.setChecked(0)
        self.answerLabel = QtWidgets.QLabel(self.centralwidget)
        self.answerLabel.setGeometry(QtCore.QRect(100, 230, 181, 21))
        self.answerLabel.setObjectName("answerLabel")
        self.answerLabel.setText(
            "<html><head/><body><p align=\"left\">Insert an answer:</p></body></html>")
        self.answer_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.answer_lineEdit.setGeometry(QtCore.QRect(100, 255, 600, 30))
        self.answer_lineEdit.setObjectName("answer_lineEdit")
        self.answer_lineEdit.clear()
        self.answerLabel.show()
        self.answer_lineEdit.show()
        self.answer_present = 1
        self.mainLabelUpdater("contextual")
        self.contextual_checkBox.setChecked(1)

    def saveQuestion(self):
        question = self.question_lineEdit.text()
        if self.plain_checkBox.isChecked() == 1:
            self.questionSignal.emit(question, "NULL", 0)
        elif self.goal_checkBox.isChecked() == 1:
            self.questionSignal.emit(question, "NULL", 1)
        else:
            answer = self.answer_lineEdit.text()
            self.questionSignal.emit(question, answer, 2)
        self.question_lineEdit.clear()
        self.resetGoalCont()
        self.goto("main")

    def goToAddMain(self):
        self.question_lineEdit.clear()
        self.resetGoalCont()
        self.goto("add")
