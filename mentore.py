from PyQt5 import QtCore, QtGui, QtWidgets
#from mentorePalette import mentorePaletteSetter
from pageWindow import PageWindow
from browseWindow import BrowseWindow
from mainWindow import MainWindow
from addMainWindow import AddMainWindow
from addSentenceWindow import AddSentenceWindow
from addQuestionWindow import AddQuestionWindow
from addContQuestionWindow import AddContQuestionWindow
from addGoalQuestionWindow import AddGoalQuestionWindow
from helpWindow import HelpWindow


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(800, 480)
        #palette = QtGui.QPalette()
        #palette = mentorePaletteSetter(palette)
        #self.setPalette(palette)

        self.setWindowIcon(QtGui.QIcon('images/mentore_logo.svg'))

        self.initPagesUI()

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(MainWindow(), "main")
        self.register(AddMainWindow(), "add")
        self.register(AddSentenceWindow(), "addSentence")
        self.register(AddQuestionWindow(), "addQuestion")
        self.register(AddContQuestionWindow(), "addContQuestion")
        self.register(AddGoalQuestionWindow(), "addGoalQuestion")
        self.register(BrowseWindow(), "browse")

        self.goto("main")

    def initPagesUI(self) -> None:
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu("Help", self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.menubar.addAction("Help", self.goToHelp)

        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setStyleSheet("border-top: 1px solid")
        self.statusbarLabelIntro = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.statusbarLabelIntro)
        self.statusbarLabelIntro.setText("Selected Topic:")
        self.statusbarLabelIntro.setStyleSheet("border-top: 0px")
        self.statusbarLabel = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.statusbarLabel)
        self.statusbarLabel.setText("none")
        self.statusbarLabel.setStyleSheet("border-top: 0px")
        self.statusbarLabelOutro = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.statusbarLabelOutro)
        self.statusbarLabelOutro.setText(" ")
        self.statusbarLabelOutro.setStyleSheet("border-top: 0px")
        self.setStatusBar(self.statusbar)

        logoLabel = QtWidgets.QLabel(self)
        logoLabel.setGeometry(350, 330, 0, 0)
        logoPixmap = QtGui.QPixmap('images/mentore_logo.svg')
        logoPixmap = logoPixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        logoLabel.setPixmap(logoPixmap)
        logoLabel.resize(logoPixmap.width(), logoPixmap.height())

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            self.lastPage = name
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())

    def goToHelp(self):
        if self.lastPage != "help":
            self.register(HelpWindow(self.lastPage), "help")
        self.goto("help")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mentoreWindow = Window()

    mentoreWindow.show()
    sys.exit(app.exec_())
