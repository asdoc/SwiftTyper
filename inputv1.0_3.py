import time
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
from PyQt4 import QtSql


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

userInputWord=""
positionOfCurrentWord=0
endOfCurrentWord=0
currentWordFromPara=""
#paragraph="small para"
paragraph="Long years ago we made a tryst with destiny, and now the time comes when we shall redeem our pledge, not wholly or in full measure, but very substantially. At the stroke of the midnight hour, when the world sleeps, India will awake to life and freedom."
words=0
numberOfReds=0
numberOfChars=1
totalChars=len(paragraph)

def stringmatch(a,b):		# A function which will match string a and b and return 1 if both are, else 0
	i=0
	while i<len(a):
		if a[i]!=b[i]:
			return False
		i+=1
	return True

def updatecurrentWordFromPara():			# A function used to store the next word into 
	global positionOfCurrentWord			# currentWordFromPara and update 
	global currentWordFromPara			# positionOfCurrentWord to next word's position
	if positionOfCurrentWord>=len(paragraph):
		return "-1"				# "-1" is returned if end of paragraph is reached
	endOfCurrentWord=positionOfCurrentWord
	while endOfCurrentWord<len(paragraph):
		if paragraph[endOfCurrentWord]==" ":
			break
		endOfCurrentWord+=1
	currentWordFromPara=paragraph[positionOfCurrentWord:endOfCurrentWord+1]
	positionOfCurrentWord=endOfCurrentWord+1

'''class mylcdtimer(QtGui.Qlcdtimer):
	value = 0.00
    
	@pyqtSlot()
	def count(self):
		self.display(self.value)
		self.value = self.value+1
'''


#add the stuff to database and display a box displaying the contents of db
def addToDatabase():
	global speed
	global tempfloat
	global text1
	global text2
	global db
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
				msg = QtGui.QMessageBox()
				msg.setText("You failed to break your record")
				msg.exec_()
			else:
				msg = QtGui.QMessageBox()
				msg.setText("New best time")
				msg.exec_()
			query3=QtSql.QSqlQuery()
			query3.prepare("DELETE  FROM newdb WHERE credenzID=?")
			query3.addBindValue(text2)
			query3.exec_()
			break
		
	tempatt+=1

	#query3=QtSql.QSqlQuery()
	#query3.exec_("DELETE (name,credenzID,wpm,accuracy,attempts) FROM newdb WHERE credenzID=\""+text2+"\"")
#	while query2.next():
#		if query2.value(0).toString() == text2:
#			print query2.value(0).toString()
	query = QtSql.QSqlQuery()
	query.prepare("insert into newdb(name,credenzID,wpm,accuracy,attempts) values(?,?,?,?,?)")
	query.addBindValue(text1)
	query.addBindValue(text2)	
	query.addBindValue(speed)
	query.addBindValue(accuracy)
	query.addBindValue(tempatt)
	query.exec_()
	query.exec_("SELECT name,credenzID,wpm,accuracy,attempts FROM newdb")
			
	result = "Name\tEmail\t\tWPM\tAccuracy\n"
	while query.next():
		name = query.value(0).toString()
		email = query.value(1).toString()
		wpm = query.value(2).toString()
		accuracy = query.value(3).toString()
		attempts=query.value(4).toString()
		result += ("\n" + name + "\t" + email + "\t" + wpm + "\t" + accuracy + "\t" + attempts)
	msg1 = QtGui.QMessageBox()
	msg1.setText(result)
	
	msg1.exec_()


class Example(QtGui.QWidget):
    
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

    def calldialog(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Welcome', 'Enter your credenz ID')
		if ok:
			if(self.getvals(text)):
				query4=QtSql.QSqlQuery()
				query4.prepare("SELECT attempts FROM newdb WHERE credenzID=?")
				query4.addBindValue(text)
				query4.exec_()
				query4.next()
				tempstr=query4.value(0).toString()    # tempstr = attemps from newdb 
				if tempstr:
					if int(tempstr)>2:
						msg = QtGui.QMessageBox()
						msg.setText("You Have completed maximum number of tries")
						msg.exec_()
						sys.exit()
				self.initUI()
			else:
				msg = QtGui.QMessageBox()
				msg.setText("You are not registered")
				msg.exec_()
				self.calldialog()

	
    def __init__(self):
        super(Example, self).__init__()
	
	global db
	db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
	db.setDatabaseName("SwiftTyper")
	ok = db.open()
#	if not ok:
#		msg = QtGui.QMessageBox()
#		msg.setText("Cannot connect to the database..!")
#		msg.exec_()
#		sys.exit()
#	else:
#		msg = QtGui.QMessageBox()
#		msg.setText("Connected to database..!")
#		msg.exec_()
		

        if ok:
		self.calldialog()
	
    def resizeEvent(self,event):
	#       			1366 * 768
	myh=self.mywin.height()
	myw=self.mywin.width()
	self.lbl.setGeometry(QtCore.QRect((myw*70/1366), (myh*50/768),(myw*800/1366), (myh*450/768)))	
	self.qle.setGeometry(QtCore.QRect((myw*70/1366),(myh*550/768),(myw*800/1366),(myh*100/768)))
        self.exitlbl.setGeometry(QtCore.QRect((myw*900/1366),(myh*550/768),(myw*500/1366),(myh*100/768)))
        self.lcdtimer.setGeometry(QtCore.QRect((myw*900/1366), (myh*100/768), (myw*250/1366),(myh*120/768)))
	self.lcdwpm.setGeometry(QtCore.QRect((myw*900/1366),(myh*240/768),(myw*250/1366),(myh*120/768)))
	self.lcdaccuracy.setGeometry(QtCore.QRect((myw*900/1366),(myh*380/768),(myw*250/1366),(myh*120/768)))
	self.wpmlbl.setGeometry(QtCore.QRect((myw*1155/1366),(myh*240/768),(myw*100/1366),(myh*120/768)))
	self.accuracylbl.setGeometry(QtCore.QRect((myw*1155/1366),(myh*380/768),(myw*50/1366),(myh*120/768)))
	self.startlbl.setGeometry(QtCore.QRect((myw*700/1366),(myh*650/768),(myw*524/1366),(myh*20/768)))

    def count(self):

	global tempfloat
	global speed
	self.value = self.value+1
	if self.value%10==0: self.lcdtimer.display((((self.value/600)*1000)+(self.value%600))/10)
    	self.lcdwpm.display(600*words/self.value)
#	print "lcd"+str(self.value)
	speed=600*words/self.value
	tempfloat=100*(numberOfChars-numberOfReds)/numberOfChars
	self.lcdaccuracy.display(int(tempfloat))

    def initUI(self):      
	self.mywin=self.window()
	self.value=0
	self.lcdtimer = QtGui.QLCDNumber(self)
        self.lcdtimer.setGeometry(QtCore.QRect(700, 120, 250,120))
	self.lcdtimer.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255);"))
	self.timer=QtCore.QTimer()
	self.lcdwpm=QtGui.QLCDNumber(self)
	self.lcdwpm.setGeometry(QtCore.QRect(700,260,250,120))
	self.lcdwpm.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255);"))
	self.lcdaccuracy=QtGui.QLCDNumber(self)
	self.lcdaccuracy.setGeometry(QtCore.QRect(700,400,250,120))
	self.lcdaccuracy.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255);"))
	QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.count)
	#self.timer.start(100)
	self.lcdtimer.display(self.value)
	#sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
	#timer.valueChanged.connect(self.lcdtimer.display)
	self.lbl = QtGui.QTextBrowser(self)
	self.exitlbl=QtGui.QLabel(self)
	self.exitlbl.setGeometry(QtCore.QRect(70,365,700,100))
        self.lbl.setGeometry(QtCore.QRect(70, 50, 724, 300))
        self.lbl.setObjectName(_fromUtf8("lbl"))
	self.lbl.setText("<font size=\"20\">"+paragraph+"</font>")
	self.lbl.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255); color: black;"))
#       self.lbl = QtGui.QLabel(paragraph,self)
        self.qle = QtGui.QLineEdit(self)
	self.qle.setGeometry(QtCore.QRect(70,500,724,100))
	self.qle.setStyleSheet(_fromUtf8("font: 24pt \"mry_KacstQurn\";\n""color: #25343B;"
"background-color: rgb(201, 183, 255);"))
        self.qle.textChanged[str].connect(self.onChanged)
	self.qle.setFocus() 
	self.startlbl = QtGui.QLabel(self)
	self.startlbl.setGeometry(QtCore.QRect(700,650,524,20))
	self.startlbl.setStyleSheet(_fromUtf8("background-color: #25343B; color: red;"))
	self.startlbl.setText("Start typing to begin!")
	self.wpmlbl=QtGui.QLabel(self)
	self.wpmlbl.setGeometry(QtCore.QRect(1155,260,100,120))
	self.wpmlbl.setText("<font size=\"20\">wpm</font>")
	self.wpmlbl.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255);"))
	self.accuracylbl=QtGui.QLabel(self)
	self.accuracylbl.setGeometry(QtCore.QRect(1155,400,50,120))
	self.accuracylbl.setText("<font size=\"28\">%</font>")
	self.accuracylbl.setStyleSheet(_fromUtf8("background-color: rgb(201, 183, 255);"))
        self.setGeometry(10, 10, 1365,758)
	self.setStyleSheet(_fromUtf8("background-color: #25343B;")) #25343B
        self.setWindowTitle('SwiftTyper')
        self.show()
        
    def onChanged(self, text): 
	global positionOfCurrentWord
	global words
	global numberOfReds
	global numberOfChars
	global endOfCurrentWord
        userInputWord=text
	if self.start==0:
		self.timeVariable=time.time()
		self.timer.start(100)
		self.start=1
		self.startlbl.setVisible(False)
	if stringmatch(userInputWord,currentWordFromPara[:len(userInputWord)]):
		#print "green"
		self.setStyleSheet(_fromUtf8("background-color: #25343B;"))
		numberOfChars+=1
	else: 
		#print "red"
		if positionOfCurrentWord<len(paragraph): fill =  "<html><font color ='green' size=\"20\">"+str(paragraph[:positionOfCurrentWord - len(currentWordFromPara)]) + "<font color ='red' size=\"20\">"+str(currentWordFromPara)+"<font color ='black'size=\"20\"><font>" + str(paragraph[positionOfCurrentWord:]) + "</html>"
		else:  fill =  "<html><font color ='green' size=\"20\">"+str(paragraph[:positionOfCurrentWord-1 - len(currentWordFromPara)]) + "<font color ='red' size=\"20\">"+str(currentWordFromPara)+"<font color ='black'size=\"20\"><font>" + str(paragraph[positionOfCurrentWord:]) + "</html>"
		self.lbl.setText(fill)
		numberOfReds+=1
		self.setStyleSheet(_fromUtf8("background-color: rgb(200, 10, 10);"))
		numberOfChars+=1
	if len(userInputWord)==len(currentWordFromPara):
		if stringmatch(userInputWord,currentWordFromPara):
#			self.lbl.setText(paragraph[positionOfCurrentWord:])
#			self.lbl.setTextFormat(Qt.RichText)
#			self.lbl.setText("<html> <font color =''>"+str(paragraph[:endOfCurrentWord])+"<
#			font>"+str(paragraph[endOfCurrentWord:])+"</html>")
			self.lbl.setText(QtGui.QApplication.translate("Dialog", "<html><head/><body><p><font color=\"green\" size=\"20\">"+str(paragraph[:positionOfCurrentWord])+"</font><font size=\"20\">"+str(paragraph[positionOfCurrentWord:])+"</font></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
			a=updatecurrentWordFromPara()
			words+=1
			self.qle.clear()
			if a=="-1":
				global speed
				global tempfloat
				
				self.timeVariable=time.time()-self.timeVariable
				wpm = int(60*words/self.timeVariable)
				print "Your speed is " + str(wpm) +" words per minute"
				accuracy = tempfloat
				print "Accuracy="+ str(tempfloat) + "%"
				self.timer.stop()
				self.exitlbl.setText("<font size=\"15\" color=\"white\">"+str(speed)+" Words per minute</font>")
				self.qle.setReadOnly(True)
				
				addToDatabase()
				
				
#				print str(self.timeVariable)
#				exit()

def main():
	#global myTimer
	#myTimer.start(100)
	updatecurrentWordFromPara()
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	#ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()
