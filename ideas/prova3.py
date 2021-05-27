from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import sys

app = QApplication(sys.argv)

web_widget = QWebEngineView()  
webChannel = QWebChannel()    # ?
page = QWebEnginePage()       # ?
web_widget.setPage(page)      # ? 
my_url = QUrl("/index.html")
web_widget.load(my_url)

# now somehow replace the placeholder in the loaded html page with file contents?

file_url = QUrl("README.md")

# help 


web_widget.show()
app.exec_()