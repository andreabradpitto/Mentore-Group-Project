from PyQt5 import QtCore, QtWidgets
from pageWindow import PageWindow


class HelpWindow(PageWindow):
    def __init__(self, lastPage: str):
        super().__init__()
        self.lastPage = lastPage
        self.initPageUI()

    def initPageUI(self):
        self.setWindowTitle("Help")
        self.setObjectName("HelpWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(180, 120, 381, 21))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText("<html><head/><body><p align=\"center\">Here go the instructions "
                               "for the user</p></body></html>")
        self.back_pb = QtWidgets.QPushButton("< Back", self.centralwidget)
        self.back_pb.setGeometry(QtCore.QRect(630, 370, 106, 30))
        self.back_pb.setObjectName("back_pb")
        self.back_pb.clicked.connect(self.goToPreviousPage)
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def goToPreviousPage(self):
        self.goto(self.lastPage)
