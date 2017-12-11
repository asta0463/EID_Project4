# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'P3.ui'
#
# Created: Sun Dec 10 09:14:40 2017
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(777, 556)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../Project1-EID/pi.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.request_button = QtGui.QPushButton(self.centralwidget)
        self.request_button.setGeometry(QtCore.QRect(10, 10, 101, 41))
        self.request_button.setObjectName(_fromUtf8("request_button"))
        self.text_window = QtGui.QTextEdit(self.centralwidget)
        self.text_window.setGeometry(QtCore.QRect(120, 10, 631, 101))
        self.text_window.setObjectName(_fromUtf8("text_window"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 160, 751, 231))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.Humgraph_button = QtGui.QPushButton(self.centralwidget)
        self.Humgraph_button.setGeometry(QtCore.QRect(120, 120, 121, 31))
        self.Humgraph_button.setObjectName(_fromUtf8("Humgraph_button"))
        self.Tempgraph_button = QtGui.QPushButton(self.centralwidget)
        self.Tempgraph_button.setGeometry(QtCore.QRect(250, 120, 151, 31))
        self.Tempgraph_button.setObjectName(_fromUtf8("Tempgraph_button"))
        self.CtoF_button = QtGui.QPushButton(self.centralwidget)
        self.CtoF_button.setGeometry(QtCore.QRect(10, 120, 101, 31))
        self.CtoF_button.setObjectName(_fromUtf8("CtoF_button"))
        self.MQTT_button = QtGui.QPushButton(self.centralwidget)
        self.MQTT_button.setGeometry(QtCore.QRect(410, 120, 81, 31))
        self.MQTT_button.setObjectName(_fromUtf8("MQTT_button"))
        self.websockets_button = QtGui.QPushButton(self.centralwidget)
        self.websockets_button.setGeometry(QtCore.QRect(500, 120, 101, 31))
        self.websockets_button.setObjectName(_fromUtf8("websockets_button"))
        self.COAP_button = QtGui.QPushButton(self.centralwidget)
        self.COAP_button.setGeometry(QtCore.QRect(610, 120, 71, 31))
        self.COAP_button.setObjectName(_fromUtf8("COAP_button"))
        self.compare_button = QtGui.QPushButton(self.centralwidget)
        self.compare_button.setGeometry(QtCore.QRect(10, 60, 101, 31))
        self.compare_button.setObjectName(_fromUtf8("compare_button"))
        self.AMQP_button = QtGui.QPushButton(self.centralwidget)
        self.AMQP_button.setGeometry(QtCore.QRect(690, 120, 81, 31))
        self.AMQP_button.setObjectName(_fromUtf8("AMQP_button"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Project1", None))
        self.request_button.setText(_translate("MainWindow", "Request Data", None))
        self.Humgraph_button.setText(_translate("MainWindow", "Humidity Graph", None))
        self.Tempgraph_button.setText(_translate("MainWindow", "Temperature Graph", None))
        self.CtoF_button.setText(_translate("MainWindow", "C <-> F", None))
        self.MQTT_button.setText(_translate("MainWindow", "MQTT", None))
        self.websockets_button.setText(_translate("MainWindow", "WebSockets", None))
        self.COAP_button.setText(_translate("MainWindow", "COAP", None))
        self.compare_button.setText(_translate("MainWindow", "Compare", None))
        self.AMQP_button.setText(_translate("MainWindow", "AMQP", None))

