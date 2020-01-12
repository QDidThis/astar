from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush
import sys


class GraphView(QWidget):
	def __init__(self,graph):
		super().__init__()
		self.graph = graph
		self.initUI()
		self.empty = QColor(255,255,255)
		self.blocked = QColor(156, 94, 8)
		self.visited = QColor(237, 33, 33)
		self.done = QColor(64, 136, 219)

	def initUI(self):
		self.setGeometry(300,300,20+20*len(self.graph),20+20*len(self.graph[0]))
		self.setWindowTitle('Grid')
		self.show()
	
	def paintEvent(self,e):
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
#				qp.setBrush(QColor(i*10,j*10,abs(j-i)*10))
				qp.drawRect(10+i*20,10+j*20,20,20)
		



if __name__=='__main__':
	app = QApplication([])
	ex = GraphView([[0,-1,0,0,0,0,0,0,0,0],
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
