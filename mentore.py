from PyQt5 import QtCore, QtGui, QtWidgets
from mentorePalette import mentorePaletteSetter


class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)


class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Mentore")
        self.setObjectName("MainWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(150, 50, 351, 81))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText("<html><head/><body><p align=\"center\">Select the class/subject to edit</p></body></html>")
        self.recentLabel = QtWidgets.QLabel(self.centralwidget)
        self.recentLabel.setGeometry(QtCore.QRect(60, 180, 141, 51))
        self.recentLabel.setObjectName("recentLabel")
        self.recentLabel.setText("<html><head/><body><p align=\"center\">Recently used</p></body></html>")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 250, 160, 106))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.recentVLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.recentVLayout.setContentsMargins(0, 0, 0, 0)
        self.recentVLayout.setObjectName("recentVLayout")
        self.recent1_pb = QtWidgets.QPushButton("recent 1", self.verticalLayoutWidget)
        self.recent1_pb.setObjectName("recent1_pb")
        self.recentVLayout.addWidget(self.recent1_pb)
        self.recent2_pb = QtWidgets.QPushButton("recent 2", self.verticalLayoutWidget)
        self.recent2_pb.setObjectName("recent2_pb")
        self.recentVLayout.addWidget(self.recent2_pb)
        self.recent3_pb = QtWidgets.QPushButton("recent 3", self.verticalLayoutWidget)
        self.recent3_pb.setObjectName("recent3_pb")
        self.recentVLayout.addWidget(self.recent3_pb)
        self.browse_pb = QtWidgets.QPushButton("Browse", self.centralwidget)
        self.browse_pb.setGeometry(QtCore.QRect(630, 270, 106, 30))
        self.browse_pb.setObjectName("browse_pb")
        self.browse_pb.clicked.connect(self.make_handleButton("browse_pb"))
        self.add_pb = QtWidgets.QPushButton("Add", self.centralwidget)
        self.add_pb.setGeometry(QtCore.QRect(630, 320, 106, 30))
        self.add_pb.setObjectName("add_pb")
        self.add_pb.clicked.connect(self.make_handleButton("add_pb"))
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu("Help", self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())

        QtCore.QMetaObject.connectSlotsByName(self)

    def make_handleButton(self, button):
        def handleButton():
            if button == "add_pb":
                self.goto("add")
            elif button == "browse_pb":
                self.goto("browse")
        return handleButton


class AddMainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add menu")
        self.setObjectName("AddWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(150, 50, 351, 81))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText("<html><head/><body><p align=\"center\">Something goes here...</p></body></html>")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(250, 285, 160, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.addVLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.addVLayout.setContentsMargins(0, 0, 0, 0)
        self.addVLayout.setObjectName("addVLayout")
        self.addSentence_pb = QtWidgets.QPushButton("Add sentence", self.verticalLayoutWidget)
        self.addSentence_pb.setObjectName("addSentence_pb")
        self.addSentence_pb.clicked.connect(self.goToAddSentence)
        self.addVLayout.addWidget(self.addSentence_pb)
        self.addQuestion_pb = QtWidgets.QPushButton("Add question", self.verticalLayoutWidget)
        self.addQuestion_pb.setObjectName("addQuestion_pb")
        self.addQuestion_pb.clicked.connect(self.goToAddQuestion)
        self.addVLayout.addWidget(self.addQuestion_pb)
        self.back_pb = QtWidgets.QPushButton("< Back", self.centralwidget)
        self.back_pb.setGeometry(QtCore.QRect(510, 380, 106, 30))
        self.back_pb.setObjectName("back_pb")
        self.back_pb.clicked.connect(self.goToMain)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu("Help", self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())
    
        QtCore.QMetaObject.connectSlotsByName(self)

    def goToMain(self):
        self.goto("main")

    def goToAddSentence(self):
        self.goto("addSentence")

    def goToAddQuestion(self):
        self.goto("addQuestion")


class AddSentenceWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add sentence")
        self.setObjectName("AddSentenceWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.add_pb = QtWidgets.QPushButton("Add", self.centralwidget)
        self.add_pb.setGeometry(QtCore.QRect(650, 340, 106, 30))
        self.add_pb.setObjectName("add_pb")
        self.cancel_pb = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_pb.setGeometry(QtCore.QRect(520, 340, 106, 30))
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
        self.negative_checkBox = QtWidgets.QCheckBox("Negative sentence", self.centralwidget)
        self.negative_checkBox.setGeometry(QtCore.QRect(550, 170, 181, 27))
        self.negative_checkBox.setObjectName("negative_checkBox")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu("Help", self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())
    
        QtCore.QMetaObject.connectSlotsByName(self)

    def goToAddMain(self):
        self.sentence_lineEdit.clear()
        self.negative_checkBox.setCheckState(0)
        self.goto("add")


class AddQuestionWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add Question")
        self.setObjectName("AddWQuestionWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.add_pb = QtWidgets.QPushButton("Add", self.centralwidget)
        self.add_pb.setGeometry(QtCore.QRect(650, 340, 106, 30))
        self.add_pb.setObjectName("add_pb")
        self.cancel_pb = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_pb.setGeometry(QtCore.QRect(520, 340, 106, 30))
        self.cancel_pb.setObjectName("cancel_pb")
        self.cancel_pb.clicked.connect(self.goToAddMain)
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(110, 50, 601, 31))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">"
                               "Please enter a question and its answer for the _____ class</span></p></body></html>")
        self.questionLabel = QtWidgets.QLabel(self.centralwidget)
        self.questionLabel.setGeometry(QtCore.QRect(30, 130, 141, 21))
        self.questionLabel.setObjectName("questionLabel")
        self.questionLabel.setText("<html><head/><body><p align=\"center\">Question:</p></body></html>")
        self.answerLabel = QtWidgets.QLabel(self.centralwidget)
        self.answerLabel.setGeometry(QtCore.QRect(30, 230, 141, 21))
        self.answerLabel.setObjectName("answerLabel")
        self.answerLabel.setText("<html><head/><body><p align=\"center\">Answer:</p></body></html>")
        self.question_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.question_lineEdit.setGeometry(QtCore.QRect(50, 170, 451, 29))
        self.question_lineEdit.setObjectName("question_lineEdit")
        self.answer_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.answer_lineEdit.setGeometry(QtCore.QRect(50, 270, 451, 29))
        self.answer_lineEdit.setObjectName("answer_lineEdit")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu("Help", self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())
    
        QtCore.QMetaObject.connectSlotsByName(self)

    def goToAddMain(self):
        self.question_lineEdit.clear()
        self.answer_lineEdit.clear()
        self.goto("add")


class BrowseWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Select Class")
        self.setObjectName("BrowseWindow")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.cancel_pb = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_pb.setGeometry(QtCore.QRect(560, 370, 89, 25))
        self.cancel_pb.setObjectName("cancel_pb")
        self.cancel_pb.clicked.connect(self.goToMain)
        self.concept_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.concept_lineEdit.setGeometry(QtCore.QRect(200, 210, 231, 25))
        self.concept_lineEdit.setObjectName("concept_lineEdit")
        self.mainLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainLabel.setGeometry(QtCore.QRect(180, 120, 381, 21))
        self.mainLabel.setObjectName("mainLabel")
        self.mainLabel.setText("<html><head/><body><p align=\"center\">Enter the Class / "
                               "Subject you want to add</p></body></html>")
        self.ok_pb = QtWidgets.QPushButton("Ok", self.centralwidget)
        self.ok_pb.setGeometry(QtCore.QRect(660, 370, 89, 25))
        self.ok_pb.setObjectName("ok_pb")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu("Help", self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())
    
        QtCore.QMetaObject.connectSlotsByName(self)

    def goToMain(self):
        self.goto("main")


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(800, 480)
        palette = QtGui.QPalette()
        palette = mentorePaletteSetter(palette)
        self.setPalette(palette)

        self.setWindowIcon(QtGui.QIcon('images/mentore_logo.svg'))

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(MainWindow(), "main")
        self.register(AddMainWindow(), "add")
        self.register(AddSentenceWindow(), "addSentence")
        self.register(AddQuestionWindow(), "addQuestion")
        self.register(BrowseWindow(), "browse")

        self.goto("main")

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mentoreWindow = Window()

    mentoreWindow.show()
    sys.exit(app.exec_())
    