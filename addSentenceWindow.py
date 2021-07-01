from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class AddSentenceWindow(PageWindow):

    sentenceSignal = QtCore.pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.initPageUI()

    def initPageUI(self):
        self.setWindowTitle("Add sentence")
        self.setObjectName("AddSentenceWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.add_pb = QtWidgets.QPushButton("Add", self.centralwidget)
        self.add_pb.setGeometry(QtCore.QRect(630, 370, 106, 30))
        self.add_pb.setObjectName("add_pb")
        self.add_pb.clicked.connect(self.saveSentence)
        self.add_pb.setDisabled(1)

        self.cancel_pb = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_pb.setGeometry(QtCore.QRect(505, 370, 106, 30))
        self.cancel_pb.setObjectName("cancel_pb")
        self.cancel_pb.clicked.connect(self.goToAddMain)

        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(0, 0, 800, 180))
        self.mainLabel.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabelUpdater("positive")

        self.sentenceLabel = QtWidgets.QLabel(self.centralwidget)
        self.sentenceLabel.setGeometry(QtCore.QRect(100, 145, 181, 21))
        self.sentenceLabel.setObjectName("sentenceLabel")
        self.sentenceLabel.setText(
            "<html><head/><body><p align=\"left\">Insert a sentence:</p></body></html>")

        self.sentence_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.sentence_lineEdit.setGeometry(QtCore.QRect(100, 170, 600, 30))
        self.sentence_lineEdit.setObjectName("sentence_lineEdit")
        self.sentence_lineEdit.textChanged.connect(self.disableButton)

        self.positive_checkBox = QtWidgets.QCheckBox(
            "Positive sentence", self.centralwidget)
        self.positive_checkBox.setGeometry(QtCore.QRect(80, 330, 181, 27))
        self.positive_checkBox.setObjectName("positive_checkBox")
        self.positive_checkBox.setChecked(1)
        self.positive_checkBox.clicked.connect(self.resetNegWait)

        self.negative_checkBox = QtWidgets.QCheckBox(
            "Negative sentence", self.centralwidget)
        self.negative_checkBox.setGeometry(QtCore.QRect(80, 350, 181, 27))
        self.negative_checkBox.setObjectName("negative_checkBox")
        self.negative_checkBox.clicked.connect(self.resetPosWait)

        self.wait_checkBox = QtWidgets.QCheckBox(
            "Wait sentence", self.centralwidget)
        self.wait_checkBox.setGeometry(QtCore.QRect(80, 370, 181, 27))
        self.wait_checkBox.setObjectName("wait_checkBox")
        self.wait_checkBox.clicked.connect(self.resetPosNeg)

        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def mainLabelUpdater(self, word: str):
        labelString = "<html><head/><body><p align=\"center\"><span style=\"font-size:12pt\">You are about to enter a new </span> \
                       <span style=\"font-size:12pt; font-weight:bold\">" + word + "</span> <span style=\"font-size:12pt\">\
                       sentence</span></p></body></html>"
        self.mainLabel.setText(labelString)

    def disableButton(self):
        if len(self.sentence_lineEdit.text()) > 0:
            self.add_pb.setDisabled(0)
        else:
            self.add_pb.setDisabled(1)

    def resetNegWait(self):
        self.negative_checkBox.setChecked(0)
        self.wait_checkBox.setChecked(0)
        self.mainLabelUpdater("positive")
        self.positive_checkBox.setChecked(1)

    def resetPosWait(self):
        self.positive_checkBox.setChecked(0)
        self.wait_checkBox.setChecked(0)
        self.mainLabelUpdater("negative")
        self.negative_checkBox.setChecked(1)

    def resetPosNeg(self):
        self.positive_checkBox.setChecked(0)
        self.negative_checkBox.setChecked(0)
        self.mainLabelUpdater("wait")
        self.wait_checkBox.setChecked(1)

    def saveSentence(self):
        sentence = self.sentence_lineEdit.text()
        if self.positive_checkBox.isChecked() == 1:
            self.sentenceSignal.emit(sentence, 0)
        elif self.negative_checkBox.isChecked() == 1:
            self.sentenceSignal.emit(sentence, 1)
        else:
            self.sentenceSignal.emit(sentence, 2)
        self.sentence_lineEdit.clear()
        self.resetNegWait()
        self.goto("main")

    def goToAddMain(self):
        self.sentence_lineEdit.clear()
        self.resetNegWait()
        self.goto("add")
