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
        self.negative_checkBox = QtWidgets.QCheckBox(
            "Negative sentence", self.centralwidget)
        self.negative_checkBox.setGeometry(QtCore.QRect(550, 170, 181, 27))
        self.negative_checkBox.setObjectName("negative_checkBox")
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def goToAddMain(self):
        self.sentence_lineEdit.clear()
        self.negative_checkBox.setCheckState(0)
        self.goto("add")
