import sys
from PyQt4 import QtCore, QtGui
from PyQt4 import QtSql
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):


    def checkfor(self,text2):
	query = QtSql.QSqlQuery()
	query.exec_("SELECT name,credenzID,college FROM reg_table")
	while query.next():
		name = query.value(0).toString()
		creid = query.value(1).toString()
		coll = query.value(2).toString()
		if creid == text2:
			return 0
	return 1



	return 0





    def saveToDB(self):
#        app = QtGui.QApplication(sys.argv)
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("SwiftTyper")
        ok = db.open()
        if not ok:
            msg = QtGui.QMessageBox()
            msg.setText("Cannot connect to the database")
            msg.exec_()
            sys.exit()

	text=self.lineEdit.text()
	text2=self.lineEdit_2.text()
	text3=self.lineEdit_3.text()
	phone=self.lineEdit_4.text();
	
	if self.checkfor(text2)==0:
		msg = QtGui.QMessageBox()
		msg.setText("You have already registered")
		msg.exec_()
		sys.exit(0)

        query = QtSql.QSqlQuery()
        query.prepare("insert into reg_table(name,credenzID,college,phno) values(?,?,?,?)")
        query.addBindValue(text)
        query.addBindValue(text2)	
        query.addBindValue(text3)
	query.addBindValue(phone)
        ok=query.exec_()

        if ok:
            msg = QtGui.QMessageBox()
            msg.setText("You are now registered.")
            msg.exec_()
            sys.exit()
        else:
            msg = QtGui.QMessageBox()
            msg.setText("Error registering")
            msg.exec_()
            sys.exit()
            

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setFixedSize(522, 441)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 120, 66, 31))
        self.label.setStyleSheet(_fromUtf8("font: oblique 14pt \"Pothana2000\";"))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 170, 111, 31))
        self.label_2.setStyleSheet(_fromUtf8("font: oblique 14pt \"Pothana2000\";"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(160, 110, 261, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 166, 261, 31))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 234, 71, 31))
        self.label_3.setStyleSheet(_fromUtf8("font: oblique 14pt \"Pothana2000\";"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 230, 261, 31))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(160, 30, 204, 51))
        self.label_4.setStyleSheet(_fromUtf8("background-color: rgb(211, 207, 255);\n"
"font: 20pt \"Pothana2000\";\n"
"color: rgb(62, 62, 62);"))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 298, 101, 31))
        self.label_5.setStyleSheet(_fromUtf8("font: oblique 14pt \"Pothana2000\";"))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_4 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 290, 261, 31))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_5"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 522, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)



        self.submitButton = QtGui.QPushButton(self.centralwidget)
        self.submitButton.setObjectName(_fromUtf8("submit_button"))
        self.label_3.setStyleSheet(_fromUtf8("font: oblique 14pt \"Pothana2000\";"))
        #self.submitButton.setEnabled(True)
        self.submitButton.setGeometry(QtCore.QRect(230, 360, 61, 31))
        self.submitButton.clicked.connect(self.saveToDB)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Credenz ID"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "College", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "R E G I S T E R", None, QtGui.QApplication.UnicodeUTF8))
        self.submitButton.setText(QtGui.QApplication.translate("MainWindow", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Phone No.", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
