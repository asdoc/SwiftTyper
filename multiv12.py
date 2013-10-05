import time
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
from PyQt4.QtCore import (QByteArray,QDataStream,QIODevice,QString)
from PyQt4 import QtSql
from PyQt4.QtNetwork import (QTcpSocket)
from paragraphs import paralist
import random


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

SIZEOF_UINT16 = 2

PORT=0
flag=0
flag2=1
userInputWord=""
positionOfCurrentWord=0
endOfCurrentWord=0
currentWordFromPara=""
paralen = 0
paragraph=""
paratextsize=8
words=0
numberOfReds=0
numberOfChars=1
totalChars=0

def stringmatch(a,b):
	i=0
	while i<len(a):
		if a[i]!=b[i]:
			return False
		i+=1
	return True

def updatecurrentWordFromPara():
	global positionOfCurrentWord
	global currentWordFromPara
	if positionOfCurrentWord>=len(paragraph):
		return "-1"
	endOfCurrentWord=positionOfCurrentWord
	while endOfCurrentWord<len(paragraph):
		if paragraph[endOfCurrentWord]==" ":
			break
		endOfCurrentWord+=1
	currentWordFromPara=paragraph[positionOfCurrentWord:endOfCurrentWord+1]
	positionOfCurrentWord=endOfCurrentWord+1

class App(QtGui.QWidget):
    
    value=0
    start=0

    def getvals(self,text):
	global text1
	global text2
	query = QtSql.QSqlQuery()
	query.exec_("SELECT name,credenzID,college FROM reg_table")
	while query.next():
		name = query.value(0).toString()
		creid = query.value(1).toString()
		coll = query.value(2).toString()
		if creid == text:
			text1=name
			text2=creid 
			return 1
	return 0


    def addToDatabase(self):
	global speed
	global tempfloat
	global text1
	global text2
	global tempatt
	global accuracy
	accuracy = int(tempfloat)
	query2=QtSql.QSqlQuery()
	query2.exec_("SELECT name,credenzID,wpm,accuracy,attempts FROM newdb")
	tempatt=0
	tempwpm=0
	tempaccuracy=0
	while query2.next():
		if query2.value(1) == text2:
			tempwpm=int(query2.value(2).toString())
			tempaccuracy=int(query2.value(3).toString())
			tempatt=int(query2.value(4).toString())
			if tempwpm > speed:
				speed=tempwpm
				accuracy=tempaccuracy
			break
	
	tempatt+=1
	query = QtSql.QSqlQuery()
	query.exec_("SELECT name,credenzID,wpm,accuracy,attempts FROM newdb")
	
	self.issueRequest(QString(str(1009) + "..." + text1 + "." + text2 + "." + str(speed) + "." + str(accuracy) + "." +  str(tempatt)))
		
    def calldialog(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Welcome', 'Enter your credenz ID')
		if ok:
			if(self.getvals(text)):
				global PORT
				query4=QtSql.QSqlQuery()
				query4.prepare("SELECT attempts FROM newdb WHERE credenzID=?")
				query4.addBindValue(text)
				query4.exec_()
				query4.next()
				tempstr=query4.value(0).toString()
				if tempstr:
					if int(tempstr)>999:
						msg = QtGui.QMessageBox()
						msg.setText("You Have completed maximum number of tries")
						msg.exec_()
						sys.exit()
				global flag
				if flag == 0:
					self.initUI()
					flag=1
				self.restart.setVisible(False)
				self.qle.setVisible(True)
				self.start=0
				portstr, ok = QtGui.QInputDialog.getText(self, 'Welcome', 'Enter port for connection')
				PORT=int(portstr)
			else:
				msg = QtGui.QMessageBox()
				msg.setText("You are not registered")
				msg.exec_()
				self.calldialog()

		else: exit(0)
    def __init__(self):
        super(App, self).__init__()
	
	global db
	db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
	db.setDatabaseName("SwiftTyper")
	ok = db.open()

        if ok:
		self.calldialog()
	
    def resizeEvent(self,event):
	#       			1366 * 768
	myh=self.mywin.height()
	myw=self.mywin.width()
	self.lbl.setGeometry(QtCore.QRect((myw*70/1366), (myh*50/768),(myw*800/1366), (myh*450/768)))	
	self.qle.setGeometry(QtCore.QRect((myw*70/1366),(myh*550/768),(myw*800/1366),(myh*100/768)))
        self.exitlbl.setGeometry(QtCore.QRect((myw*900/1366),(myh*550/768),(myw*345/1366),(myh*100/768)))
        self.lcdtimer.setGeometry(QtCore.QRect((myw*900/1366), (myh*100/768), (myw*250/1366),(myh*120/768)))
	self.lcdwpm.setGeometry(QtCore.QRect((myw*1000/1366),(myh*240/768),(myw*250/1366),(myh*120/768)))
	self.lcdaccuracy.setGeometry(QtCore.QRect((myw*1000/1366),(myh*380/768),(myw*250/1366),(myh*120/768)))
	self.wpmlbl.setGeometry(QtCore.QRect((myw*900/1366),(myh*240/768),(myw*100/1366),(myh*120/768)))
	self.accuracylbl.setGeometry(QtCore.QRect((myw*900/1366),(myh*380/768),(myw*100/1366),(myh*120/768)))
	self.restart.setGeometry(QtCore.QRect((myw*70/1366),(myh*550/768),(myw*800/1366),(myh*100/768)))
        self.progbar.setGeometry(QtCore.QRect((myw*70/1366),(myh*670/768),(myw*1200/1366),(myh*50/768)))


    def restartf(self):
	global userInputWord
	global positionOfCurrentWord
	global endOfCurrentWord
	global currentWordFromPara
	global paragraph
	global paralen
	global words
	global numberOfReds
	global numberOfChars
	global totalChars
	global paralen
	global flag2
	self.value=0
	self.value2=-2
	self.timer3.stop()
	userInputWord=""
	positionOfCurrentWord=0
	endOfCurrentWord=0
	currentWordFromPara=""
	self.calldialog()
	paralen = len(paragraph.split(" "))
	self.start=0
	flag2=1
	self.timer.start(100)
	words=0
	numberOfReds=0
	numberOfChars=1
	totalChars=len(paragraph)
	global paratextsize
	self.lbl.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255); color: #4C3327;"))
	self.lbl.setText("<font size=\""+str(paratextsize)+"\">"+paragraph+"</font>")

    def count3(self):
	self.issueRequest(QString(str(1009) + "..." + text1 + "." + text2 + "." + str(speed) + "." + str(accuracy) + "." +  str(tempatt)))
	
    def count(self):
	global tempfloat
	global speed
	global flag2
	global words
	global paralen
	global text1
	global text2
	global accuracy
	global tempatt
	if flag2 == 0:
		self.value = self.value+1
		if self.value%10==0: self.lcdtimer.display((((self.value/600)*1000)+(self.value%600))/10)
	    	self.lcdwpm.display(600*words/self.value)
		speed=600*words/self.value
		tempfloat=100*(numberOfChars-numberOfReds)/numberOfChars
		self.progbar.setValue((100*words)/paralen)
		if self.value % 10 == 0:
			self.issueRequest(QString(str(600*words/self.value)))
	elif flag2 == 2:			  # flag2==2: means para typed
		if self.value % 10 == 0:
			self.issueRequest(QString(str(1009) + "..." + text1 + "." + text2 + "." + str(speed) + "." + str(accuracy) + "." +  str(tempatt)))
	else:					  # flag2==1: send fetch_para signal to server
		if self.value % 10 == 0:
			self.issueRequest(QString(str(1000)))
		self.start=0

    def count2(self):
	self.value2+=1
	self.lcdtimer.display(self.value2)
	if self.value2 == 0:
		self.qle.setReadOnly(False)
		self.qle.setFocus()
	if self.value2 == 1:
		self.timer2.stop()
		self.timer.start(100)


    def initUI(self):      

	self.socket=QTcpSocket()
        self.connect(self.socket, SIGNAL("connected()"), self.sendRequest)
        self.connect(self.socket, SIGNAL("readyRead()"), self.readResponse)
        self.connect(self.socket, SIGNAL("disconnected()"), self.serverHasStopped)
        self.connect(self.socket, SIGNAL("error(QAbstractSocket::SocketError)"),self.serverHasError)

	self.mywin=self.window()
	self.value=0
	self.value2=-2
	self.lcdtimer = QtGui.QLCDNumber(self)
        self.lcdtimer.setGeometry(QtCore.QRect(700, 120, 250,120))
	self.lcdtimer.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255);""color: #F1ECDD;"))

	self.lcdtimer.display(self.value2)
	self.timer=QtCore.QTimer()
	self.timer2=QtCore.QTimer()
	self.timer3=QtCore.QTimer()
	self.lcdwpm=QtGui.QLCDNumber(self)
	self.lcdwpm.setGeometry(QtCore.QRect(700,260,250,120))
	self.lcdwpm.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255);""color: #F1ECDD;"))

        self.progbar = QtGui.QProgressBar(self)
        self.progbar.setGeometry(70,670,1000,100)
	self.progbar.setValue(0)

	self.lcdaccuracy=QtGui.QLCDNumber(self)
	self.lcdaccuracy.setGeometry(QtCore.QRect(700,400,250,120))
	self.lcdaccuracy.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255);""color: #F1ECDD;"))

	QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.count)
	QtCore.QObject.connect(self.timer2, QtCore.SIGNAL("timeout()"), self.count2)
	QtCore.QObject.connect(self.timer3, QtCore.SIGNAL("timeout()"), self.count3)

	self.lcdtimer.display(self.value)
	self.lbl = QtGui.QTextBrowser(self)
	self.exitlbl=QtGui.QLabel(self)
	self.exitlbl.setGeometry(QtCore.QRect(70,365,700,100))
	self.exitlbl.setVisible(False)

	self.restart=QtGui.QPushButton(self)
	self.restart.setGeometry(QtCore.QRect(100,550,724,100))
	self.restart.setText("Restart")
	self.restart.setVisible(False)
	self.restart.setStyleSheet(_fromUtf8("font: 24pt \"mry_KacstQurn\";\n""background-color: rgb(255, 255, 255);"))
        self.restart.clicked.connect(self.restartf)

        self.lbl.setGeometry(QtCore.QRect(70, 50, 724, 300))
        self.lbl.setObjectName(_fromUtf8("lbl"))
	self.lbl.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255); color: #4C3327;"))

        self.qle = QtGui.QLineEdit(self)
	self.qle.setGeometry(QtCore.QRect(70,500,724,100))
	self.qle.setStyleSheet(_fromUtf8("font: 24pt \"mry_KacstQurn\";\n""color: #25343B;"
"background-color: rgb(201, 183, 255);"))
        self.qle.textChanged[str].connect(self.onChanged)
	self.qle.setReadOnly(True)

	self.wpmlbl=QtGui.QLabel(self)
	self.wpmlbl.setGeometry(QtCore.QRect(1155,260,100,120))
	self.wpmlbl.setText("<font size=\"20\"> WPM</font>")
	self.wpmlbl.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255);""color: #F1ECDD;"))

	self.accuracylbl=QtGui.QLabel(self)
	self.accuracylbl.setGeometry(QtCore.QRect(1155,400,120,120))
	self.accuracylbl.setText("<font size=\"28\">Rank</font>")
	self.accuracylbl.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255);""color: #F1ECDD;"))

        self.setGeometry(10, 10, 1365,758)
	self.setStyleSheet(_fromUtf8("background-color: #4C3327;""background-image: url(img3.jpg);""color: #4C3327;"))
        self.setWindowTitle('SwiftTyper')
	self.show()
	self.timer.start(100)

        self.shrt_sh=QtGui.QShortcut(QtGui.QKeySequence.ZoomIn,self)
        self.connect(self.shrt_sh, QtCore.SIGNAL("activated()"), self.shrt)

        self.shrt2_sh=QtGui.QShortcut(QtGui.QKeySequence.ZoomOut,self)
        self.connect(self.shrt2_sh, QtCore.SIGNAL("activated()"), self.shrt2)

    def shrt(self):
	global paratextsize
	if paratextsize<7:
		paratextsize+=1
       	self.lbl.setText("<font size='"+str(paratextsize)+"'>"+paragraph+"</font>")

    def shrt2(self):
	global paratextsize
	if paratextsize>3:
		paratextsize-=1
       	self.lbl.setText("<font size='"+str(paratextsize)+"'>"+paragraph+"</font>")

    def onChanged(self, text): 
	global positionOfCurrentWord
	global words
	global numberOfReds
	global numberOfChars
	global endOfCurrentWord

        userInputWord=text
	if self.start==0:
		self.start=1
	if stringmatch(userInputWord,currentWordFromPara[:len(userInputWord)]):
		# green
		self.setStyleSheet(_fromUtf8("background-color: #4C3327;""background-image: url(img3.jpg);""color: #4C3327;"))
		numberOfChars+=1
	else: 
		# red
		global paratextsize
		if positionOfCurrentWord<len(paragraph):
			fill =  "<html><font color ='green' size='"+str(paratextsize)+"'>"+str(paragraph[:positionOfCurrentWord - len(currentWordFromPara)]) + "<font color ='red' size='"+str(paratextsize)+"'>"+str(currentWordFromPara)+"<font color=#4C3327 size='"+str(paratextsize)+"'><font>" + str(paragraph[positionOfCurrentWord:]) + "</html>"
		else:
			fill =  "<html><font color ='green' size='"+str(paratextsize)+"'>"+str(paragraph[:positionOfCurrentWord-1 - len(currentWordFromPara)]) + "<font color ='red' size='"+str(paratextsize)+"'>"+str(currentWordFromPara)+"<font color=#F1ECDD size='"+str(paratextsize)+"'><font>" + str(paragraph[positionOfCurrentWord:]) + "</html>"
		self.lbl.setText(fill)
		numberOfReds+=1
		self.setStyleSheet(_fromUtf8("background-color: rgb(200, 10, 10);""background-image: url(img3.jpg);""color: #4C3327;"))
		numberOfChars+=1
	if len(userInputWord)==len(currentWordFromPara):
		if stringmatch(userInputWord,currentWordFromPara):
			self.lbl.setText(QtGui.QApplication.translate("Dialog", "<html><head/><body><p><font color=\"green\" size=\""+str(paratextsize)+"\">"+str(paragraph[:positionOfCurrentWord])+"</font><font size=\""+str(paratextsize)+"\">"+str(paragraph[positionOfCurrentWord:])+"</font></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
			a=updatecurrentWordFromPara()
			words+=1
			self.qle.clear()
			if a=="-1":
				global speed
				global tempfloat
				global flag2
				
				accuracy = tempfloat
				self.timer.stop()
				self.timer3.start(1000)
				self.progbar.setValue((100*words)/paralen)
				self.exitlbl.setVisible(True)
				self.exitlbl.setText("<font size=\"15\" color=\"#F1ECDD\">   "+str(speed)+" Words per minute</font>")

				self.addToDatabase()
				self.start=0
				flag2 = 2
				self.timer.start(100)
				self.qle.setVisible(False)
				self.restart.setVisible(True)
				self.restart.setEnabled(True)


    def issueRequest(self, inpdata):
        self.request = QByteArray()
        stream = QDataStream(self.request, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream <<  inpdata
        stream.device().seek(0)
        stream.writeUInt16(self.request.size() - SIZEOF_UINT16)
        if self.socket.isOpen():
            self.socket.close()
        self.socket.connectToHost("127.0.0.1", PORT)


    def sendRequest(self):
        self.nextBlockSize = 0
        self.socket.write(self.request)
        self.request = None
        

    def readResponse(self):
	global paralen
	global words
        stream = QDataStream(self.socket)
        stream.setVersion(QDataStream.Qt_4_2)

        while True:
            if self.nextBlockSize == 0:
                if self.socket.bytesAvailable() < SIZEOF_UINT16:
                    break
                self.nextBlockSize = stream.readUInt16()
            if self.socket.bytesAvailable() < self.nextBlockSize:
                break
            inpdata = QString()

            stream >> inpdata
	    s = str(inpdata)
	    s = s.split(" ",1)
	    global flag2
	    if flag2 == 1:
			if int(s[0]) == 1000 and (s[1]) == "0" :
				self.lbl.setText("<font size='8'>Waiting for other players . . . </font>")

			else:
		    	    flag2=0  # flag2==0: para is fetched and game is not finished
			    parastr=s[1].split(" ",1)
			    n=int(str(parastr[0]))    
			    allparas=paralist()
			    global paragraph
			    global paralen
			    paragraph=parastr[1]
			    paralen = len(paragraph.split())
	       		    self.lbl.setText("<font size=\""+str(paratextsize)+"\">"+paragraph+"</font>")
			    self.lcdwpm.display(0)
			    self.lcdaccuracy.display(0)
			    self.lcdtimer.display(0)
			    self.progbar.setValue(0)
			    self.exitlbl.setVisible(False)
			    updatecurrentWordFromPara()
			    global totalChars
			    totalChars=len(paragraph)
			    self.timer.stop()
			    self.qle.setReadOnly(True)
			    self.timer2.start(1000)
	    if flag2 == 2:
			if int(s[0]) == 1009:
			    self.lbl.setText(s[1])
			    self.lbl.setStyleSheet(_fromUtf8("font: 24pt \"mry_KacstQurn\";""color:#4C3327;"))
		
	    elif flag2 == 0  and int(s[0])!=1000 and int(s[0])!=1010 and int(s[0])!=1009:
		    self.lcdaccuracy.display(int(str(inpdata)))
            self.nextBlockSize = 0

    def serverHasStopped(self):
	None

    def serverHasError(self, error):
	self.socket.close()


def main():
	app = QtGui.QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()
