from PyQt5 import QtCore, QtGui, QtWidgets
from mentorePalette import mentorePaletteSetter
from browseWindow import BrowseWindow
from mainWindow import MainWindow
from addMainWindow import AddMainWindow
from addConceptWindow import AddConceptWindow
from addSentenceWindow import AddSentenceWindow
from addQuestionWindow import AddQuestionWindow
from helpWindow import HelpWindow
from owlready2 import *
import ontologyInterface as ontoInt


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(800, 480)
        palette = QtGui.QPalette()
        palette = mentorePaletteSetter(palette)
        self.setPalette(palette)

        self.setWindowIcon(QtGui.QIcon('images/mentore_logo.svg'))

        self.ontologyInit("ontology/Caresses.owl", "Hour")

        self.initPagesUI()

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(MainWindow(), "main")
        self.register(AddMainWindow(), "add")
        self.register(AddConceptWindow(), "addConcept")
        self.register(AddSentenceWindow(), "addSentence")
        self.register(AddQuestionWindow(), "addQuestion")
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
        self.statusbarLabelIntro.setText("Selected subject:")
        self.statusbarLabelIntro.setStyleSheet("border-top: 0px")
        self.statusbarLabel = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.statusbarLabel)
        self.statusBarUpdater("none")
        self.currentConcept = "none"
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

    def statusBarUpdater(self, concept: str):
        statusString = "<html><head/><body><p> <b>" + concept + "</b> \
                        </p></body></html>"
        self.statusbarLabel.setText(statusString)
        self.currentConcept = concept

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if (isinstance(widget, BrowseWindow) or isinstance(widget, MainWindow)):
            widget.selectedConceptSignal.connect(self.selectedConceptName)
            widget.gotoSignal.connect(self.goto)
        elif isinstance(widget, AddConceptWindow):
            widget.conceptNameSignal.connect(self.catchConceptName)
            widget.gotoSignal.connect(self.goto)
        elif isinstance(widget, AddSentenceWindow):
            widget.sentenceSignal.connect(self.catchSentence)
            widget.gotoSignal.connect(self.goto)
        elif isinstance(widget, AddQuestionWindow):
            widget.questionSignal.connect(self.catchQuestion)
            widget.gotoSignal.connect(self.goto)
        else:  # this is the case for all the other children of PageWindow
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            self.lastPage = name
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())
            if name == "browse":
                widget.createItemList(self.subjectsList)
            elif name == "main":
                if self.currentConcept != "none":
                    widget.recentChecker(self.currentConcept)

    def goToHelp(self):
        if self.lastPage != "help":
            self.register(HelpWindow(self.lastPage), "help")
        self.goto("help")

    @QtCore.pyqtSlot(str)
    def selectedConceptName(self, name):
        self.statusBarUpdater(name)

    @QtCore.pyqtSlot(str)
    def catchConceptName(self, name):
        self.statusBarUpdater(name)
        #add the subject to the owl file itself
        #add the subject to the list to be sent to browsePage

        #call add_class_to_ontology
        #self.subjectsList.insert(0, name)
        #self.statusBarUpdater(name)
        print(name)  # to be deleted

    @QtCore.pyqtSlot(str, int)
    def catchSentence(self, sentence, type):
        #read the current subject (get string from status bar; use self.currentConcept)
        #add the sentence (care about its type!) to the owl file: call add_individual_to_ontology (?!)
        print(f"{sentence}, {type}")  # to be deleted

    @QtCore.pyqtSlot(str, str, int)
    def catchQuestion(self, sentence, answer, type):
        #read the current subject (get string from status bar; use self.currentConcept)
        #add the question and possibly the answer (care about its type!) to the owl file
        print(f"{sentence}, {answer}, {type}")  # to be deleted

    def ontologyInit(self, ontologyPath: str, startClassName: str):
        ontology = get_ontology(ontologyPath)
        ontology.load()
        self.subjectsList = ontoInt.retrieve_subclasses(ontology, startClassName)
        print(self.subjectsList)  # to be deleted


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mentoreWindow = Window()

    mentoreWindow.show()
    sys.exit(app.exec_())
