from __future__ import division
from __future__ import unicode_literals
from future_builtins import *
from PyQt4 import QtGui, QtCore
from PyQt4 import QtSql


import bisect
import collections
import sys
from PyQt4.QtCore import (QByteArray, QDataStream, QDate, QIODevice,
        QReadWriteLock, QString, QThread, Qt, SIGNAL, SLOT)
from PyQt4.QtGui import (QApplication, QMessageBox, QPushButton)
from PyQt4.QtCore import (QByteArray,QDataStream,QIODevice,QString)
from PyQt4.QtNetwork import (QAbstractSocket, QHostAddress, QTcpServer,
        QTcpSocket)
import random
from paragraphs import paralist
k=3
n=0
flag2=0
PORT={}
rankstring="1009 Rankings:-\n"
prevrankstring=""
compplayers=0
for x in range(9001,9011):
	PORT[x]=[0,0,0,0,str,0,0]

SIZEOF_UINT16 = 2
MAX_BOOKINGS_PER_DAY = 5

class Thread(QThread):


    def __init__(self, socketId, parent, myPort):
        super(Thread, self).__init__(parent)
	self.myPort=myPort
        self.socketId = socketId

    def ready(self):
	global PORT
	global k
	for x in range(9001,9001+k):
		if PORT[x][2] == 0 or PORT[x][2] == 2:
			return 0
	return 1

    def ended(self):
	global PORT
	global k
	for x in range(9001,9001+k):
		if PORT[x][2] == 0 or PORT[x][2] == 1:
			return 0
	return 1
        
    def addtodatabase(self,val1,val2,val3,val4,val5):

	query2=QtSql.QSqlQuery()
	query2.prepare("DELETE  FROM newdb WHERE credenzID=?")
	query2.addBindValue(val2)
	query2.exec_()
	query = QtSql.QSqlQuery()
	query.prepare("insert into newdb(name,credenzID,wpm,accuracy,attempts) values(?,?,?,?,?)")
	query.addBindValue(val1)
	query.addBindValue(val2)	
	query.addBindValue(val3)
	query.addBindValue(val4)
	query.addBindValue(val5)
	query.exec_()
	
    def run(self):
    	global flag2
    	global PORT
    	global prevrankstring
        socket = QTcpSocket()
        if not socket.setSocketDescriptor(self.socketId):
            self.emit(SIGNAL("error(int)"), socket.error())
            return
        while socket.state() == QAbstractSocket.ConnectedState:
            nextBlockSize = 0
            stream = QDataStream(socket)
            stream.setVersion(QDataStream.Qt_4_2)
            if (socket.waitForReadyRead() and
                socket.bytesAvailable() >= SIZEOF_UINT16):
                nextBlockSize = stream.readUInt16()
            else:
                return
            if socket.bytesAvailable() < nextBlockSize:
                if (not socket.waitForReadyRead(100000) or
                    socket.bytesAvailable() < nextBlockSize):
                    return
            room = QString()
	    toSend = QString()
            stream >> room

	    s = str(room)
	    s = s.split("...")

	    global n
	    if int(str(s[0])) == 1000:
		    PORT[self.myPort][2]=1
		    if self.ready():
			toSend=QString(str(1000)+" "+str(1)+" "+allparas.para[n])
			flag2=1
		    else:
			toSend=QString(str(1000)+" 0")

	    elif int(str(s[0])) == 1009 and flag2!=0:
	    	    s2=s[1].split(".")
		    global rankstring
		    global compplayers
		    if len(s2) == 5 and PORT[self.myPort][2] != 2:
			compplayers+=1
			rankstring += (str(compplayers) + ". " + s2[0] + "\n")
		        PORT[self.myPort][2]=2
		        PORT[self.myPort][6]=1
			self.addtodatabase(s2[0],s2[1],s2[2],s2[3],s2[4])
		    toSend = QString(rankstring)
		    prevrankstring=rankstring


	    elif int(str(s[0])) == 1009:
	    	    toSend = QString(prevrankstring)
	    else:
		    PORT[self.myPort][1]=int(str(room))
		    self.rank=1
		    for x in range(9001,9001+k):
			if PORT[x][1] > PORT[self.myPort][1]:
				self.rank+=1	
		    PORT[self.myPort][5] = self.rank
		    toSend=QString(str(self.rank))					
	    self.sendError(socket, toSend)


    def sendError(self, socket, msg):
	global port1data
	global port2data
        reply = QByteArray()
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream << QString(msg)
	
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        socket.write(reply)




class TcpServer(QTcpServer):

    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)
        
    def setPort(self,port):
	self.port=port

    def incomingConnection(self, socketId):
        thread = Thread(socketId, self, self.port)
        thread.start()
        

class BuildingServicesDlg(QPushButton):

    def lose(self):
    	global flag2
	global n
        global rankstring
        global compplayers
        global PORT
	for x in range(9001,9011):
		PORT[x][2]=0
	rankstring="1009 Rankings:-\n"
	compplayers=0
	flag2=0
	n=random.randrange(0,len(allparas.para))
	global k
    	for i in range(9001,9001+k):
    		PORT[i][6] = 0
	text, ok = QtGui.QInputDialog.getText(self, 'Server', 'Enter number of players and press OK to create server')
	if ok:
		k = int(text)
	else:
		sys.exit()



    def lose2(self):
    	global flag2
	global n
        global rankstring
        global compplayers
        global PORT
	for x in range(9001,9011):
		PORT[x][2]=0
	rankstring="1009 Rankings:-\n"
	compplayers=0
	flag2=0
	n=random.randrange(0,len(allparas.para))
	global k
    	for i in range(9001,9001+k):
    		PORT[i][6] = 0

    def checkrestart(self):
    	global k
    	for i in range(9001,9001+k):
    		if PORT[i][6] == 0:
    			return 0
    	return 1

    def count(self):
	if self.checkrestart():
		self.lose2()    	
    	
    	
    	
    def __init__(self, parent=None):
	global k        
	global db
	db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("SwiftTyper")
        ok = db.open()
	self.timer=QtCore.QTimer()
	self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.count)
	super(BuildingServicesDlg, self).__init__("&Restart Server", parent)
	text, ok = QtGui.QInputDialog.getText(self, 'Server', 'Enter number of players and press OK to create server')
	if ok:
		k = int(text)
	else:
		sys.exit()
        self.tcpServer=[TcpServer(self),TcpServer(self),TcpServer(self),TcpServer(self),TcpServer(self),TcpServer(self),TcpServer(self),TcpServer(self),TcpServer(self),TcpServer(self)]

	for x in range(9001,9011):
	        self.tcpServer[x-9001] = TcpServer(self)		
		self.tcpServer[x-9001].setPort(x)
		if not self.tcpServer[x-9001].listen(QHostAddress("0.0.0.0"), x):
		    QMessageBox.critical(self, "Building Services Server",
		            QString("Failed to start server: %1").arg(self.tcpServer[x-9001].errorString()))
		    self.close()
		    return


        self.connect(self, SIGNAL("clicked()"), self.lose2)
        font = self.font()
        font.setPointSize(24)
        self.setFont(font)
        self.setWindowTitle(str(k) + " Player(s) server")
	self.timer.start(2000)

	

	
allparas=paralist()
n=random.randrange(0,len(allparas.para))
app = QApplication(sys.argv)
form = BuildingServicesDlg()
form.show()
form.move(0, 0)
app.exec_()
