from PyQt5 import QtCore, QtGui, QtWidgets
from mentorePalette import mentorePaletteSetter
from pageWindow import PageWindow
from browseWindow import BrowseWindow
from mainWindow import MainWindow
from addMainWindow import AddMainWindow
from addSentenceWindow import AddSentenceWindow
from addQuestionWindow import AddQuestionWindow


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
