import time


""" This program is intended to arrange random numbers in BTree form of any order for efficient search

Authors: Mohit Kolluri
		Siddarth Mitra
		Aseem Pathak




"""


#For printing the BTree, taken from a reference code

def printer(prefix ,isTail,n):				
	print ( prefix + ("└── " if isTail else "├── ") + str(n.keys) )
	for i in range(len(n.children)-1 , 0 , -1):
		if n.children[i]!=None:
			printer(prefix +  ("    " if isTail else  "│   " ), False , n.children[i])
	
	if (len(n.children) > 0) and n.children[0] != None:
		printer(prefix + ("    " if isTail else "│   "), True , n.children[0])
	
		
def printTree(tree):
	printer("" , True , tree.root)


class BTreeNode(object):

	def __init__(self,leaf=False):

		self.keys=[] #List for keys
		self.children=[] #List for children
		self.leaf=leaf #Boolean for if leaf node or not
	
	#returns number of keys in the node
	def length(self):
		return len(self.keys)
		
		


	
class BTree(object):
	
		
	def __init__(self,order=5):
		
		self.order=order  #defines the order, Default=5
		self.root= BTreeNode(True)  #initializing the root node
		self.traverse= []	#list of indexes to keep track of traversals to reach the right leaf node
		
	
		
    #Insertion function for inserting the elements   
	def insert(self,val):
		self.iterate(val);
		s=self.root
		#Loop for reaching the parent node 
		for i in self.traverse:
			if(s.leaf):
				continue
			else:
				s=s.children[i]
		#check if splitting of nodes required or not	
		if len(s.keys)>=(self.order-1):
			self.split(s)
			self.insert_not_full(val)
		else:
			self.insert_not_full(val)
		# need to clear the traverse array
		self.traverse[:]=[]
		
	#recursive function for splitting the nodes till insertion possible	
	def split(self,s):
		k=self.root
		z=BTreeNode(leaf=s.leaf) #creating a new child node
		median=(len(s.keys)/2) #determing the median index
		
		#adding the required keys and children to the node
		z.keys= s.keys[int(median+1):(self.order)]
		z.children= s.children[int(median+1):(self.order)+1]
		y=s.keys[int(median)]
		if (median-1)==0:
			h=s.keys[0]
			s.keys[:]=[]
			s.keys.append(h)
		else:
			s.keys=s.keys[0:int(median)]
			s.children= s.children[0:int(median+1)]
		#splitting different for root node and other nodes
		if(s==self.root):
			new=BTreeNode(leaf=False) #creating a new root
			new.keys.append(y)
			new.children.append(s)
			new.children.append(z)
			self.root=new
				
		else:
		    #traversing till index of insertion of the median element
			for i in self.traverse[0:-2]:
				k=k.children[i]
			self.traverse.pop()
			index=self.traverse[-1]
			k.children.insert(index+1,z)
			k.keys.insert(index,y)
			#if parent node results in being max split further
			if len(k.keys)>=self.order:
				self.split(k)
		
			
	#Insert element when not full
	def insert_not_full(self,val):
		
		s=self.root
		self.traverse[:]=[]
		self.iterate(val)
		
		if len(self.traverse)>0:
			for i in self.traverse:
				if s.leaf:
					break
					
				else:
					s=s.children[i]
		f=0		
		if len(s.keys)>0:
			for i in s.keys:
				if i<val:
					f=f+1
		
		s.keys.insert(f,val)
		s.children.insert(f,None)
		
		
		
	
	
	#For traversing the path of insertion till the leaf node
	def iterate(self,val):
		s=self.root
		cond=False
		while cond==False:
			j=0
			cond=s.leaf
			
			if len(s.keys)>0:
				for i in s.keys:
					if i<val:
						j=j+1
				self.traverse.append(j)
			if(len(s.children)>j):
				s=s.children[j]
				
			
t=BTree();

start_time = time.time()
for i in range(100):
	t.insert(i)
printTree(t) #Printing the BTree
print("--- %s seconds ---" % (time.time() - start_time)) #Determining the efficiency of the code

		
		
			