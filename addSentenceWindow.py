from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class AddSentenceWindow(PageWindow):
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
        self.cancel_pb = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_pb.setGeometry(QtCore.QRect(505, 370, 106, 30))
        self.cancel_pb.setObjectName("cancel_pb")
        self.cancel_pb.clicked.connect(self.goToAddMain)
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(200, 90, 401, 31))
        self.mainLabel.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">"
                               "Please enter a new sentence</span></p></body></html>")
        self.sentence_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.sentence_lineEdit.setGeometry(QtCore.QRect(60, 170, 461, 29))
        self.sentence_lineEdit.setObjectName("sentence_lineEdit")
        self.positive_checkBox = QtWidgets.QCheckBox(
            "Positive sentence", self.centralwidget)
        self.positive_checkBox.setGeometry(QtCore.QRect(560, 170, 181, 27))
        self.positive_checkBox.setObjectName("positive_checkBox")
        self.positive_checkBox.setChecked(1)
        self.positive_checkBox.clicked.connect(self.resetNegWait)
        self.negative_checkBox = QtWidgets.QCheckBox(
            "Negative sentence", self.centralwidget)
        self.negative_checkBox.setGeometry(QtCore.QRect(560, 190, 181, 27))
        self.negative_checkBox.setObjectName("negative_checkBox")
        self.negative_checkBox.clicked.connect(self.resetPosWait)
        self.wait_checkBox = QtWidgets.QCheckBox(
            "Wait sentence", self.centralwidget)
        self.wait_checkBox.setGeometry(QtCore.QRect(560, 210, 181, 27))
        self.wait_checkBox.setObjectName("wait_checkBox")
        self.wait_checkBox.clicked.connect(self.resetPosNeg)
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def resetNegWait(self):
        self.negative_checkBox.setChecked(0)
        self.wait_checkBox.setChecked(0)

    def resetPosWait(self):
        self.positive_checkBox.setChecked(0)
        self.wait_checkBox.setChecked(0)

    def resetPosNeg(self):
        self.positive_checkBox.setChecked(0)
        self.negative_checkBox.setChecked(0)

    def goToAddMain(self):
        self.sentence_lineEdit.clear()
        self.positive_checkBox.setChecked(1)
        self.negative_checkBox.setChecked(0)
        self.wait_checkBox.setChecked(0)
        self.goto("add")
