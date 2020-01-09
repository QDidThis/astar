class PriorityQueue:
	def __init__(self,comp):
		import binomialheap as heap
		self.heap = heap.BinomialHeap(comp)
	
	def enqueue(self,value):
		self.heap = self.heap.insert(value)
	
	def dequeue(self):
		if self.peek() is None:
			return None
		value,self.heap = self.heap.removeMin()
		return value

	def peek(self):
		return self.heap.peek()
