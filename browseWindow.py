from PyQt5 import QtCore, QtWidgets, QtGui
from pageWindow import PageWindow


class BrowseWindow(PageWindow):

    selectedConceptSignal = QtCore.pyqtSignal(str)

    browseSubjectsList = []

    def __init__(self):
        super().__init__()
        self.initPageUI()

    def initPageUI(self):
        self.setWindowTitle("Select subject")
        self.setObjectName("BrowseWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.cancel_pb = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_pb.setGeometry(QtCore.QRect(505, 370, 106, 30))
        self.cancel_pb.setObjectName("cancel_pb")
        self.cancel_pb.clicked.connect(self.goToMain)
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(0, 0, 800, 180))
        self.mainLabel.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mainLabel.setObjectName("mainLabel")
        labelString = "<html><head/><body><p align=\"center\"><span style=\"font-size:12pt\">You are </span> \
                       <span style=\"font-size:12pt; font-weight:bold\"> selecting </span> <span style=\"font-size:12pt\">\
                       a subject</span></p></body></html>"
        self.mainLabel.setText(labelString)

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(260, 135, 280, 145))
        self.listWidget.setObjectName("listWidget")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        self.createItemList(self.browseSubjectsList)

        self.ok_pb = QtWidgets.QPushButton("Ok", self.centralwidget)
        self.ok_pb.setGeometry(QtCore.QRect(630, 370, 106, 30))
        self.ok_pb.setObjectName("ok_pb")
        self.ok_pb.clicked.connect(self.selectConcept)
        self.setCentralWidget(self.centralwidget)

        self.ok_pb.setDisabled(1)
        self.listWidget.itemSelectionChanged.connect(self.disableButton)

        QtCore.QMetaObject.connectSlotsByName(self)

    def createItemList(self, subjectsList: list):
        for elem in subjectsList:
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(elem)

    def disableButton(self):
        if len(self.listWidget.selectedItems()) != 0:
            self.ok_pb.setDisabled(0)
        else:
            self.ok_pb.setDisabled(1)

    def clearSelection(self):
        for idx in range(self.listWidget.count()):
            item = self.listWidget.item(idx)
            item.setSelected(False)

    def selectConcept(self):
        concept = self.listWidget.currentItem()
        conceptName = concept.text()
        self.selectedConceptSignal.emit(conceptName)
        #self.clearSelection()
        self.listWidget.clear()
        self.goto("main")

    def goToMain(self):
        #self.clearSelection()
        self.listWidget.clear()
        self.goto("main")
