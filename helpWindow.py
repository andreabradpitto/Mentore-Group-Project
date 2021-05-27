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
        self.back_pb = QtWidgets.QPushButton("< Back", self.centralwidget)
        self.back_pb.setGeometry(QtCore.QRect(630, 370, 106, 30))
        self.back_pb.setObjectName("back_pb")
        self.back_pb.clicked.connect(self.goToPreviousPage)
        self.mdText = QtWidgets.QTextBrowser(self.centralwidget)
        self.mdText.setMarkdown(open('help.md', encoding="utf8").read())
        self.mdText.setGeometry(QtCore.QRect(0, 0, 800, 290))
        self.mdText.setObjectName("mdText")
        #self.htmlText = QtWidgets.QTextBrowser(self.centralwidget)
        #self.htmlText.setHtml(open('help.html', encoding="utf8").read()) # encoding needed?
        #self.htmlText.setGeometry(QtCore.QRect(0, 0, 800, 290))
        #self.htmlText.setObjectName("htmlText")

        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def goToPreviousPage(self):
        self.goto(self.lastPage)
