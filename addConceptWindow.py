from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class AddConceptWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initPageUI()

    def initPageUI(self):
        self.setWindowTitle("Add Concept")
        self.setObjectName("AddConceptWindow")

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
        self.mainLabel.setGeometry(QtCore.QRect(0, 0, 800, 180))
        self.mainLabel.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mainLabel.setObjectName("mainLabel")
        labelString = "<html><head/><body><p align=\"center\"><span style=\"font-size:12pt\">You are about to enter a new </span> \
                       <span style=\"font-size:12pt; font-weight:bold\"> concept </span> <span style=\"font-size:12pt\"> \
                       name</span></p></body></html>"
        self.mainLabel.setText(labelString)
        self.conceptLabel = QtWidgets.QLabel(self.centralwidget)
        self.conceptLabel.setGeometry(QtCore.QRect(240, 145, 181, 21))
        self.conceptLabel.setObjectName("conceptLabel")
        self.conceptLabel.setText(
            "<html><head/><body><p align=\"left\">Insert a new concept:</p></body></html>")
        self.concept_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.concept_lineEdit.setGeometry(QtCore.QRect(240, 170, 320, 30))
        self.concept_lineEdit.setObjectName("concept_lineEdit")
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def goToAddMain(self):
        self.concept_lineEdit.clear()
        self.goto("add")
