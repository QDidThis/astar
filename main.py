from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import gui.graphView as graphView
import astar.astar as astar
import time

def makeGraph(x, y, old=None):
	if old is None:
		old = []
		for i in range(x):
			old.append([])
			for j in range(y):
				old[i].append(0)
	else:
		h = len(old)
		w = len(old[0])
		if h <= x and w <= y:
			for i in range(h):
				for j in range(w,y):
					old[i].append(0)
			for i in range(h,x):
				old.append([])
				for j in range(y):
					old[i].append(0)
		elif h <= x and w > y:
			for i in range(h):
				for j in range(w-y):
					old[i].pop()
			for i in range(h,x):
				for j in range(y):
					old[i].append(0)	
		elif w <= y and h > x:
			for i in range(h-x):
				old.pop()
			for i in range(x):
				for j in range(w,y):
					old[i].append(0)
		else:
			for i in range(h-x):
				old.pop()
			for i in range(x):
				for j in range(w-y):
					old[i].pop()
	return old

class Window(QWidget):

	def __init__(self):
		super().__init__()
		self.astarThread = None
		self.initUI()
	
	def initUI(self):
		self.graph = makeGraph(30,30)
		self.graphV = graphView.GraphController(self.graph)
		self.startbtn = QPushButton('Start')
		self.startbtn.resize(self.startbtn.sizeHint())
		self.startbtn.clicked.connect(self.startpressed)
		
		self.stopbtn = QPushButton('Stop')
		self.stopbtn.resize(self.stopbtn.sizeHint())
		self.stopbtn.clicked.connect(self.stoppressed)
		self.stopbtn.setEnabled(False)
	
		self.resetbtn = QPushButton('Reset')
		self.resetbtn.resize(self.resetbtn.sizeHint())
		self.resetbtn.clicked.connect(self.resetpressed)
		
		self.showbtn = QPushButton('Show')
		self.showbtn.resize(self.showbtn.sizeHint())
		self.showbtn.clicked.connect(self.showpressed)

		hbox1 = QHBoxLayout()
		hbox1.addWidget(self.startbtn)
		hbox1.addWidget(self.showbtn)
		hbox1.addWidget(self.stopbtn)
		hbox1.addWidget(self.resetbtn)
	
		vbox = QVBoxLayout()
		vbox.addWidget(self.graphV)
		vbox.addStretch()
		vbox.addLayout(hbox1)

		self.win = QLineEdit()
		self.win.setValidator(QIntValidator())
		self.win.setMaxLength(3)
		self.win.setAlignment(Qt.AlignRight)
		self.win.setText(str(len(self.graph[0])))
		self.win.editingFinished.connect(self.widthchanged)
		lw = QLabel('width')

		self.hin = QLineEdit()
		self.hin.setValidator(QIntValidator())
		self.hin.setMaxLength(3)
		self.hin.setAlignment(Qt.AlignRight)
		self.hin.setText(str(len(self.graph)))
		self.hin.editingFinished.connect(self.heightchanged)
		lh = QLabel('height')
		
		self.yin = QLineEdit()
		self.yin.setValidator(QIntValidator())
		self.yin.setMaxLength(3)
		self.yin.setAlignment(Qt.AlignRight)
		self.yin.setText(str(len(self.graph[0])-1))
		self.yin.editingFinished.connect(self.ychanged)
		ly = QLabel('Goal y')
	
		self.xin = QLineEdit()
		self.xin.setValidator(QIntValidator())
		self.xin.setMaxLength(3)
		self.xin.setAlignment(Qt.AlignRight)
		self.xin.setText(str(len(self.graph)-1))
		self.xin.editingFinished.connect(self.xchanged)
		lx = QLabel('Goal x')
		
		fbox = QFormLayout()
		fbox.addRow(lw,self.win)
		fbox.addRow(lh,self.hin)	
		fbox.addRow(lx,self.xin)
		fbox.addRow(ly,self.yin)
			
		hbox = QHBoxLayout()
		hbox.addLayout(vbox)
		hbox.addStretch()
		hbox.addLayout(fbox)
			
		self.setWindowTitle('Window')
		self.setLayout(hbox)
		self.show()

	def heightchanged(self):
		height = self.hin.text()
		if height is None:
			return
		makeGraph(int(height),len(self.graph[0]),self.graph)
		if int(self.xin.text()) >= int(height):
			self.xin.setText(str(len(self.graph)-1))
		self.update()

	def widthchanged(self):
		width = self.win.text()
		if width is None:
			return
		makeGraph(len(self.graph),int(width),self.graph)
		if int(self.yin.text()) >= int(width):
			self.yin.setText(str(len(self.graph[0])-1))
		self.update()
	
	def startpressed(self):
		self.astarThread = AStarThread(self.graph,(int(self.xin.text()),int(self.yin.text())))
		self.astarThread.stepDone.connect(self.step)
		self.astarThread.done.connect(self.done)
		self.win.setReadOnly(True)
		self.hin.setReadOnly(True)	
		self.xin.setReadOnly(True)
		self.yin.setReadOnly(True)	
		self.astarThread.start()
		self.startbtn.setEnabled(False)
		self.resetbtn.setEnabled(False)
		self.stopbtn.setEnabled(True)
		self.graphV.setEnabled(False)
	
	def stoppressed(self):
		self.astarThread.stop()
		self.update()
	#	self.startbtn.setEnabled(True)
		self.resetbtn.setEnabled(True)
		self.stopbtn.setEnabled(False)
	
	def resetpressed(self):
		makeGraph(1,1,self.graph)
		self.graph[0][0] = 0
		makeGraph(30,30,self.graph)
		self.update()
		self.startbtn.setEnabled(True)
		self.win.setReadOnly(False)
		self.win.setText(str(len(self.graph)))
		self.hin.setReadOnly(False)
		self.hin.setText(str(len(self.graph[0])))
		self.xin.setReadOnly(False)
		self.xin.setText(str(len(self.graph)-1))
		self.yin.setReadOnly(False)	
		self.yin.setText(str(len(self.graph[0])-1))
		self.graphV.setEnabled(True)

	def showpressed(self):
		if (not self.astarThread is None) and self.astarThread.isRunning:
			self.astarThread.show()
		else:	
			self.astarThread = AStarThread(self.graph,(int(self.xin.text()),int(self.yin.text())),display=False)
			self.astarThread.stepDone.connect(self.step)
			self.astarThread.done.connect(self.done)
			self.win.setReadOnly(True)
			self.hin.setReadOnly(True)	
			self.xin.setReadOnly(True)
			self.yin.setReadOnly(True)	
			self.astarThread.start()
			self.startbtn.setEnabled(False)
			self.graphV.setEnabled(False)
	


	def step(self):
		self.update()

	def done(self):
		self.update()
		self.resetbtn.setEnabled(True)
		self.stopbtn.setEnabled(False)
		self.win.setReadOnly(False)
		self.hin.setReadOnly(False)
		self.xin.setReadOnly(False)
		self.yin.setReadOnly(False)	
	
		
	
	def xchanged(self):
		x = int(self.xin.text())
		if x < 0 or x >= len(self.graph):
			self.xin.setText(str(len(self.graph)-1))

	
	def ychanged(self):
		y = int(self.yin.text())
		if y < 0 or y >= len(self.graph[0]):
			self.yin.setText(str(len(self.graph[0])-1))


class AStarThread(QThread):
	stepDone = pyqtSignal()
	done = pyqtSignal()

	def __init__(self,graph,end,display=True,parent=None):
		QThread.__init__(self,parent)
		import math
		l = lambda x,y:math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)
		l2 = lambda x,y: 0
		l3 = lambda x,y: abs(x[0]-y[0])+abs(x[1]-y[1])
		self.graph = graph
		self.astar = astar.AStar((0,0),end,self.graph,l3)
		self.isRunning = False	
		self.display = display

	def run(self):
		if not self.isRunning:
			self.isRunning = True
		while not self.astar.done and self.isRunning:
			self.astar.step()
			if self.display:
				self.stepDone.emit()
				time.sleep(.1)
		if self.astar.done:
			path = self.astar.get_path()
			self.isRunning = False
			self.done.emit()
	
	def stop(self):
		self.isRunning = False

	def show(self):
		self.display = False
		
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	win = Window()
	sys.exit(app.exec_())
	
