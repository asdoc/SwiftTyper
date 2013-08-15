import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
from PyQt4 import QtSql


def main():
	app = QtGui.QApplication(sys.argv)
	db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
	
	db.setDatabaseName("SwiftTyper")
	
	

	ok = db.open()
	if not ok:
		msg = QtGui.QMessageBox()
		msg.setText("Cannot connect to the database..!")
		msg.exec_()
		sys.exit()

	query = QtSql.QSqlQuery()
	ok = query.exec_("CREATE TABLE reg_table(name varchar(20), credenzID varchar(20), college varchar(25),phno int)")
	if ok:
		msg = QtGui.QMessageBox()
		msg.setText("You are now registered.")
		msg.exec_()
	else:
		msg = QtGui.QMessageBox()
		msg.setText("Error creating table")
		msg.exec_()

	sys.exit()

if __name__ == '__main__':
    main()

