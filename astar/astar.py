import priorityqueue as queue


class AStar:
	def __init__(self,start,goal,graph,heuristic):
		# Graph is a 2d array, -1 is blocked, 0 is unvisited, 1 is visited, 2 is done
		self.graph 	= graph
		self.h 		= heuristic
		# Nodes will be represented as x,y,cost,prev in the queue
		self.queue	= queue.PriorityQueue(lambda x,y: x[2]+self.h((x[0],x[1]),goal) < y[2]+self.h((y[0],y[1]),goal))
		self.prev = {start:None}
		self.goal = goal
		self.done = False
		self.current = *start,0,None
		x,y = start
		self.graph[x][y] = 2

	def step(self):
		if self.current[0] == self.goal[0] and self.current[1] == self.goal[1]:
			self.done = True
			return
		def neighbours(x,y):
			out = []
			for i in range(-1,2):
				if x+i >= 0 and x+i < len(self.graph):
					if self.graph[x+i][y] != -1 and self.graph[x+i][y] != 2:
						out.append((x+i,y))
				if y+i >= 0 and y+i < len(self.graph[x]):
					if self.graph[x][y+i] != -1 and self.graph[x][y+i] != 2:
						out.append((x,y+i))
			return out
		x,y,c,p = self.current
		neigh = neighbours(x,y)
		for nx,ny in neigh:
			self.graph[nx][ny] = 1
			self.queue.enqueue((nx,ny,c+1,(x,y)))
		next = self.queue.dequeue()
		while not next is None and self.graph[next[0]][next[1]] == 2:
			next = self.queue.dequeue()
		if next is None:
			raise RuntimeError('No Path Found')
		self.graph[next[0]][next[1]] = 2
		self.prev[next[0],next[1]] = next[3]
		self.current = next

	def get_path(self):
		if not self.done:
			raise RuntimeError('Not done')
		curr = self.goal
		path = [curr]
		while not self.prev[curr] is None:
			path.append(self.prev[curr])
			curr = self.prev[curr]
		return list(reversed(path))
