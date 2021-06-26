from PyQt5 import QtCore, QtWidgets, QtGui
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
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(0, 0, 800, 180))
        self.mainLabel.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mainLabel.setObjectName("mainLabel")
        labelString = "<html><head/><body><p align=\"center\"><span style=\"font-size:12pt\">You are </span> \
                       <span style=\"font-size:12pt; font-weight:bold\"> selecting </span> <span style=\"font-size:12pt\"> \
                       a subject</span></p></body></html>"
        self.mainLabel.setText(labelString)

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(260, 135, 280, 145))
        self.listWidget.setObjectName("listWidget")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        #item = self.listWidget.item(0)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("mate")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        #item = self.listWidget.item(1)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("fisi")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        #item = self.listWidget.item(2)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("scienze")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        #item = self.listWidget.item(3)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("italiano")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        #item = self.listWidget.item(4)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("geo")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        #item = self.listWidget.item(5)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("gatti")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        #item = self.listWidget.item(6)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("magia")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        #item = self.listWidget.item(7)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setText("inglese")

        self.ok_pb = QtWidgets.QPushButton("Ok", self.centralwidget)
        self.ok_pb.setGeometry(QtCore.QRect(630, 370, 106, 30))
        self.ok_pb.setObjectName("ok_pb")
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def clearSelection(self):
        for idx in range(self.listWidget.count()):
            item = self.listWidget.item(idx)
            item.setSelected(False)

    def goToMain(self):
        self.clearSelection()
        self.goto("main")
