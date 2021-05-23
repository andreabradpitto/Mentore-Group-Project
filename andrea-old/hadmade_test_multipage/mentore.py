# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mentore.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


def mainLayout(mWindow):
    mWindow.centralwidget = QtWidgets.QWidget()
    mWindow.centralwidget.setObjectName("centralwidget")
    mWindow.mainLabel = QtWidgets.QLabel(mWindow.centralwidget)
    mWindow.mainLabel.setGeometry(QtCore.QRect(150, 50, 351, 81))
    mWindow.mainLabel.setObjectName("mainLabel")
    mWindow.recentLabel = QtWidgets.QLabel(mWindow.centralwidget)
    mWindow.recentLabel.setGeometry(QtCore.QRect(60, 180, 141, 51))
    mWindow.recentLabel.setObjectName("recentLabel")
    mWindow.verticalLayoutWidget = QtWidgets.QWidget(mWindow.centralwidget)
    mWindow.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 250, 160, 106))
    mWindow.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
    mWindow.recentVLayout = QtWidgets.QVBoxLayout(mWindow.verticalLayoutWidget)
    mWindow.recentVLayout.setContentsMargins(0, 0, 0, 0)
    mWindow.recentVLayout.setObjectName("recentVLayout")
    mWindow.recent1_pb = QtWidgets.QPushButton(mWindow.verticalLayoutWidget)
    mWindow.recent1_pb.setObjectName("recent1_pb")
    mWindow.recentVLayout.addWidget(mWindow.recent1_pb)
    mWindow.recent2_pb = QtWidgets.QPushButton(mWindow.verticalLayoutWidget)
    mWindow.recent2_pb.setObjectName("recent2_pb")
    mWindow.recentVLayout.addWidget(mWindow.recent2_pb)
    mWindow.recent3_pb = QtWidgets.QPushButton(mWindow.verticalLayoutWidget)
    mWindow.recent3_pb.setObjectName("recent3_pb")
    mWindow.recentVLayout.addWidget(mWindow.recent3_pb)
    mWindow.browse_pb = QtWidgets.QPushButton(mWindow.centralwidget)
    mWindow.browse_pb.setGeometry(QtCore.QRect(460, 240, 106, 30))
    mWindow.browse_pb.setObjectName("browse_pb")
    mWindow.add_pb = QtWidgets.QPushButton(mWindow.centralwidget)
    mWindow.add_pb.setGeometry(QtCore.QRect(460, 290, 106, 30))
    mWindow.add_pb.setObjectName("add_pb")
    mWindow.setCentralWidget(mWindow.centralwidget)
    mWindow.menubar = QtWidgets.QMenuBar()
    mWindow.menubar.setGeometry(QtCore.QRect(0, 0, 640, 26))
    mWindow.menubar.setObjectName("menubar")
    mWindow.menuHelp = QtWidgets.QMenu(mWindow.menubar)
    mWindow.menuHelp.setObjectName("menuHelp")
    mWindow.setMenuBar(mWindow.menubar)
    mWindow.statusbar = QtWidgets.QStatusBar()
    mWindow.statusbar.setObjectName("statusbar")
    mWindow.setStatusBar(mWindow.statusbar)
    mWindow.menubar.addAction(mWindow.menuHelp.menuAction())

    #mWindow.retranslateUi()
    QtCore.QMetaObject.connectSlotsByName(mWindow)

#def retranslateUi(mWindow):
    _translate = QtCore.QCoreApplication.translate
    mWindow.setWindowTitle(_translate("MainWindow", "Mentore"))
    mWindow.mainLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Select the class/subject to edit</p></body></html>"))
    mWindow.recentLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Recently used</p></body></html>"))
    mWindow.recent1_pb.setText(_translate("MainWindow", "recent 1"))
    mWindow.recent2_pb.setText(_translate("MainWindow", "recent 2"))
    mWindow.recent3_pb.setText(_translate("MainWindow", "recent 3"))
    mWindow.browse_pb.setText(_translate("MainWindow", "Browse"))
    mWindow.add_pb.setText(_translate("MainWindow", "Add"))
    mWindow.menuHelp.setTitle(_translate("MainWindow", "Help"))

    return mWindow
