from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Demo(QTextEdit):
    def __init__(self):
        super().__init__()
        md = self.get_markdown()
        self.setMarkdown(md)

    def get_markdown(self):
        file = open('README.md', encoding="utf8").read()
        return file

app = QApplication([])
demo = Demo()
demo.show()
app.exec()