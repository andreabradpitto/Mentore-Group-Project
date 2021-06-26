from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class BrowseWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initPageUI()

    def initPageUI(self):
        self.setWindowTitle("Select topic")
        self.setObjectName("BrowseWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.cancel_pb = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_pb.setGeometry(QtCore.QRect(505, 370, 106, 30))
        self.cancel_pb.setObjectName("cancel_pb")
        self.cancel_pb.clicked.connect(self.goToMain)
        self.concept_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.concept_lineEdit.setGeometry(QtCore.QRect(200, 210, 231, 25))
        self.concept_lineEdit.setObjectName("concept_lineEdit")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(0, 0, 800, 180))
        self.mainLabel.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mainLabel.setObjectName("mainLabel")
        labelString = "<html><head/><body><p align=\"center\"><span style=\"font-size:12pt\">You are </span> \
                       <span style=\"font-size:12pt; font-weight:bold\"> selecting </span> <span style=\"font-size:12pt\"> \
                       a subject</span></p></body></html>"
        self.mainLabel.setText(labelString)
        self.ok_pb = QtWidgets.QPushButton("Ok", self.centralwidget)
        self.ok_pb.setGeometry(QtCore.QRect(630, 370, 106, 30))
        self.ok_pb.setObjectName("ok_pb")
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def goToMain(self):
        self.goto("main")
