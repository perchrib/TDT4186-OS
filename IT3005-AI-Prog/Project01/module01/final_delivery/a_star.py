from search_queue import SearchQueue
from math import sqrt
#import itertools


class A_star():
	def __init__(self, board, gui, searchMethod,speed):
		self.speed = speed
		self.gui = gui
		self.cost = 1
		self.board = board
		self.openStore = SearchQueue(searchMethod)
		self.closedStore = SearchQueue(searchMethod)

		self.board.startNode.f = self.board.startNode.g + self.board.startNode.h
		#print "finishNode", board.finishNode.state , "is Finish: ", board.finishNode.isFinish
		self.openStore.add(board.startNode)
		self.path = []
		
	def mainLoop(self):
		while self.openStore:
			if not self.openStore:
				print "Fail"
				break
			
			
			currentNode = self.openStore.pop()
			currentNode.status = 'CLOSED'
			self.closedStore.add(currentNode)			
			
			#print "Current Node State: ",currentNode.state,"   Current Node Heuristic: ", currentNode.h

			
			if currentNode.isFinish:
				print "Solution found"
				if self.gui:
					self.drawPath(currentNode,False)
					self.gui.after(self.speed,self.gui.update())

				print "closedStore: ", len(self.closedStore)
				print "openStore: " ,len(self.openStore)				
				break

			currentNode.generateNeighbours()
			for node in currentNode.neighbours:
				#if not node in self.openStore:
					#if not node in self.openStore or not node in self.closedStore :
					#	node.status = 'OPEN'
					#	self.openStore.add(node)
				currentNode.kids.append(node)
				if not node.status == 'OPEN' and not node.status == 'CLOSED':					
					if not node.isFinish:
						if self.gui:
							self.gui.canvas.itemconfig(node.ID, fill="chocolate3")
	
					self.attachAndEval(node,currentNode)
					node.status = 'OPEN'
					self.openStore.add(node)

				elif currentNode.g + self.arc_cost(currentNode,node) < node.g:
					self.attachAndEval(node,currentNode)
					print"DENNE"
					if node == 'CLOSED':
						improve_path(node)
			
			if self.gui:
				if not currentNode.isStart and not currentNode.isFinish:
					self.gui.canvas.itemconfig(currentNode.ID, fill="sandy brown")
				


				
				self.drawPath(currentNode,False)
				self.gui.after(self.speed,self.gui.update())
				self.drawPath(currentNode,True)
				
	
	def arc_cost(self,currentNode,neighbour):
		return sqrt(((currentNode.state[0]-neighbour.state[0])**2) + ((currentNode.state[1]-neighbour.state[1])**2)) * self.cost


	def attachAndEval(self,node,currentNode):
		node.parent = currentNode
		node.g = currentNode.g + self.arc_cost(currentNode,node)
		node.f = node.g + node.h

	def improve_path(currentNode):
		for kid in currentNode.kids:
			kid.parent = currentNode
			kid.g = currentNode.g + self.arc_cost(currentNode,kid)
			kid.f = kid.c + kid.h

	def findPath(self, node):
		route = []
		temp_node = node
		while not temp_node is None:
			route.append(temp_node)
			temp_node = temp_node.parent

		route.reverse()
		return route

	def drawPath(self,node,rase):

		path = self.findPath(node)
		self.path = path 
		for n in path:
			if not (n.isStart or n.isFinish):
				if rase:
					self.gui.canvas.itemconfig(n.ID, fill="sandy brown")
				else:
					self.gui.canvas.itemconfig(n.ID, fill="light blue")








					
					




