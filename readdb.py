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
            msg.setText("Cannot connect to the database")
            msg.exec_()
            sys.exit()

	query = QtSql.QSqlQuery()
        query.exec_("SELECT name,credenzID,college FROM reg_table")
			
	result = "Name\tCredenz ID\t\tcollege"
	while query.next():
		name = query.value(0).toString()
		email = query.value(1).toString()
		wpm = query.value(2).toString()
		accuracy = query.value(3).toString()
		result += ("\n" + name + "\t" + email + "\t" + wpm + "\t" + accuracy)
	msg = QtGui.QMessageBox()
	msg.setText(result)
	
	msg.exec_()


if __name__ == "__main__":
    main()
