class BinomialTree:
	def __init__(self, value, comp):
		self.children 	= []
		self.value		= value
		self.comp		= comp

	def __lt__(self, tree):
		return self.comp(self.value, tree.value)

	def __len__(self):
		return len(self.children)
	
	def __str__(self):
		out = str(self.value) 
		for child in self.children:
			out += f'\n {child}'
		return out
	
	def __repr__(self):
		return f'BinomialTree Order {len(self)}'
	
	def add_child(self, tree):
		self.children.append(tree)
		
	def merge(self, tree):
		if len(self) != len(tree):
			raise RuntimeError(f'Lengths of BinomialTrees are not equal {len(self)}, {len(tree)}')
		if self < tree:
			self.add_child(tree)
			return self
		else:
			tree.add_child(self)
			return tree

class BinomialHeap:
	'''
	comp: comparator function on the elements contained in the Heap
	'''
	def __init__(self, comp, trees=[]):
		self.trees 	= trees
		self.min 	= None
		self.comp	= comp
	
	def __len__(self):
		return len(self.trees)
	
	def __str__(self):
		return f'BinomialHeap {list(map(repr,self.trees))}'

	def __repr__(self):
		return str(self)

	def merge(self, heap):
		if len(self) < len(heap):
			return heap.merge(self)
		trees = []
		carry = None
		for tree1,tree2 in zip(self.trees,heap.trees):
			if tree1 is None and tree2 is None and carry is None:
				trees.append(None)
			elif tree1 is None and carry is None:
				trees.append(tree2)
			elif tree2 is None and carry is None:
				trees.append(tree1)
			elif tree1 is None and tree2 is None:
				trees.append(carry)
				carry = None
			elif carry is None:
				carry = tree1.merge(tree2)
				trees.append(None)
			elif tree1 is None:
				carry = carry.merge(tree2)
				trees.append(None)
			elif tree2 is None:
				carry = carry.merge(tree1)
				trees.append(None)
			else:
				trees.append(carry)
				carry = tree1.merge(tree2)
		for tree in self.trees[len(heap):]:
			if carry is None:
				trees.append(tree)
			elif tree is None:
				trees.append(carry)
				carry = None
			else:
				trees.append(None)
				carry = tree.merge(carry)
		if not carry is None:
			trees.append(carry)
		
		for tree in reversed(trees):
			if tree is None:
				trees.pop()
			else:
				break
		self.trees = trees
		return self

	def insert(self, value):
		return self.merge(BinomialHeap(self.comp,[BinomialTree(value,self.comp)]))
	
	def peek(self):
		if len(self.trees) == 0:
			return None
		min = None
		for tree in self.trees:
			if min is None and tree is None:
				continue
			elif min is None:
				min = tree
			elif tree is None:
				continue
			elif tree < min:
				min = tree
		if min is None:
			return min
		return min.value

	def removeMin(self):
		if len(self.trees) == 0:
			return None
		min = None
		min_index = 0
		for i,tree in enumerate(self.trees):
			if min is None and tree is None:
				continue
			elif min is None:
				min = tree
				min_index = i
			elif tree is None:
				continue
			elif tree < min:
				min = tree
				min_index = i
		if min is None:
			self.trees = []
			return min,self
		self.trees[min_index] = None
		return min.value,self.merge(BinomialHeap(self.comp,min.children))
