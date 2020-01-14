from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QSize
import sys


class GraphView(QWidget):
	def __init__(self,graph, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.graph = graph
		self.initUI()
		self.empty = QColor(255,255,255)
		self.blocked = QColor(156, 94, 8)
		self.visited = QColor(237, 33, 33)
		self.start = QColor(0,0,0)
		self.path = QColor(123,244,12)
		self.done = QColor(64, 136, 219)

	def initUI(self):
		self.setWindowTitle('Grid')
		self.show()
	
	def sizeHint(self):
		return QSize(len(self.graph)*20+20,len(self.graph[0])*20+20)

	def paintEvent(self,e):
		self.resize(20+20*len(self.graph),20+20*len(self.graph[0]))
		qp = QPainter()
		qp.begin(self)
		self.drawRectangles(qp)
		qp.end()

	def drawRectangles(self,qp):
		col = QColor(0,0,0)
		qp.setPen(col)
		for i,row in enumerate(self.graph):
			for j,cell in enumerate(row):
				if cell == 0:
					qp.setBrush(self.empty)
				elif cell == -1:
					qp.setBrush(self.blocked)
				elif cell == 1:
					qp.setBrush(self.visited)
				elif cell == 2:
					qp.setBrush(self.done)
				elif cell == 3:
					qp.setBrush(self.path)
				elif cell == 4:
					qp.setBrush(self.start)
#				qp.setBrush(QColor(i*10,j*10,abs(j-i)*10))
				qp.drawRect(10+i*20,10+j*20,20,20)
		

class GraphController(GraphView):
	def __init__(self, graph, *args, **kwargs):
		super().__init__(graph, *args, **kwargs)
		self.enabled = True
		self.changeTo = -1

	
	def mousePressEvent(self,QMouseEvent):
		if not self.enabled:
			return
		# 10 rand 20 20 20 20 ...
		# (pos - 10)//20
		x = (QMouseEvent.x() - 10) // 20
		y = (QMouseEvent.y() - 10) // 20
		if x >= 0 and x < len(self.graph) and y >= 0 and y < len(self.graph[0]):
			if self.graph[x][y] == 0:
				self.graph[x][y] = -1
				self.changeTo = -1
			elif self.graph[x][y] == -1:
				self.graph[x][y] = 0
				self.changeTo = 0
		self.update()
		#print(QMouseEvent.pos())
		#print((QMouseEvent.x() - 10)//20,(QMouseEvent.y() - 10)//20)
	
	def mouseMoveEvent(self,QMouseEvent):
		if not self.enabled:
			return
		x = (QMouseEvent.x() - 10) // 20
		y = (QMouseEvent.y() - 10) // 20
		if x >= 0 and x < len(self.graph) and y >= 0 and y < len(self.graph[0]):
			self.graph[x][y] = self.changeTo
		self.update()

	def setEnabled(self,bool):
		self.enabled = bool

if __name__=='__main__':
	app = QApplication([])
	ex = GraphController([[0,-1,0,0,0,0,0,0,0,0],
		[1,0,0,0,0,0,0,0,0,0],
		[2,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0]])
	sys.exit(app.exec_())
