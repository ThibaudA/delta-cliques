#-*-coding:utf8*-

import sys
import operator
from collections import deque
from Clique import Clique
from CliqueCritique import CliqueCritique

class CliqueMaster:
	
	def __init__(self):
		self._S = deque()
		self._S_set = set()
		self._R = set()
		self._times = dict()
		self._nodes = dict()

	def addClique(self, c):
		""" Adds a clique to S, checking beforehand that this clique is not already present in S. """
		if not c in self._S_set:
			#self._S.appendleft(c)
                        self._S.append(c)
			self._S_set.add(c)


	def halfMemory(self):
		length=len(self._S_set)
		while len(self._S_set) > length/2:
			trash=self._S_set.pop()
	


	def getClique(self):
		c = self._S.pop()
		#sys.stderr.write("Getting clique " + str(c) + "\n")
		return c

	def getTree(self, delta):
		""" Returns a set of maximal cliques. """
		token=0
		while len(self._S) != 0:
                        token+=1
			if token==10000:
				if len(self._S_set)>500000:  
					#Limite de Cliques dans le set _S_Set (economise la mémoire)
					self.halfMemory()
					sys.stderr.write("Cleaning _S_set \n")
				sys.stderr.write("S:"+ str(len(self._S)) + "\n")
				token=0
			c = self.getClique()
			is_max = True

			# Grow time on the right side
			td = c.getTd(self._times, delta)
			if c._te != td + delta:
				new_t,sameclique = c.getFirstTInInterval(self._times, self._nodes, td, delta)
				if new_t is not None:
                                        if sameclique:
				            c_add = Clique((c._X, (c._tb, new_t),(c._tlimitb,new_t)))
                                            if new_t-td>c._deltamin: 
						    c_add._deltamin=new_t-td
                                            else: c_add._deltamin=c._deltamin
					    
					    td=c_add.getTd(self._times,delta)
					    tp=c_add.getTp(self._times,delta)
					    c_add._deltamax=minNone(c_add.getDeltamaxLeft(self._times,tp,delta),c_add.getDeltamaxRight(self._times,td,delta))
					    
					    if c_add._deltamax is not delta:
					    	if c_add._deltamin<c_add._deltamax:
					    		self._R.add(CliqueCritique((c_add._X,(c_add._tlimitb,c_add._tlimite),c_add._deltamin,c_add._deltamax,td,tp)))
                                            else:
					    	self._R.add(CliqueCritique((c_add._X,(c_add._tlimitb,c_add._tlimite),c_add._deltamin,c_add._deltamax,td,tp)))
					else:
 				            c_add = Clique((c._X, (c._tb, new_t),(c._tlimitb,c._tlimite)))
                                            c_add._deltamin=c._deltamin
                                            c_add._deltamax=c._deltamax
                                        #sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")
					self.addClique(c_add)
				else:
					c_add = Clique((c._X, (c._tb, td + delta),(c._tlimitb,c._tlimite)))
					c_add._deltamin=c._deltamin
                                        c_add._deltamax=c._deltamax
					self.addClique(c_add)
					#sys.stderr.write("Adding " + str(c_add) + " (time delta extension)\n")
				is_max = False
			#else:
				#sys.stderr.write(str(c) + " cannot grow on the right side\n")

			# Grow time on the left side 
			tp = c.getTp(self._times, delta)
			if c._tb != tp - delta:
				new_t,sameclique = c.getLastTInInterval(self._times, self._nodes, tp, delta)

				if new_t is not None:
                                        if sameclique:
				        	c_add = Clique((c._X, (new_t , c._te),(new_t,c._tlimite)))
                                                if tp-new_t>c._deltamin: c_add._deltamin=tp-new_t
                                                else: c_add._deltamin=c._deltamin
					    	td=c_add.getTd(self._times,delta)
					    	tp=c_add.getTp(self._times,delta)
					    	c_add._deltamax=minNone(c_add.getDeltamaxRight(self._times,td,delta),c_add.getDeltamaxLeft(self._times,tp,delta))
					    	
						if c_add._deltamax is not delta:
					    		if c_add._deltamin<c_add._deltamax:
					    			self._R.add(CliqueCritique((c_add._X,(c_add._tlimitb,c_add._tlimite),c_add._deltamin,c_add._deltamax,td,tp)))
                                            	else:
					    		self._R.add(CliqueCritique((c_add._X,(c_add._tlimitb,c_add._tlimite),c_add._deltamin,c_add._deltamax,td,tp)))
					else:	
                                                c_add = Clique((c._X, (new_t , c._te),(c._tlimitb,c._tlimite)))       
						c_add._deltamin=c._deltamin
                                        	c_add._deltamax=c._deltamax
                                        self.addClique(c_add)
					#sys.stderr.write("Adding " + str(c_add) + " (left time extension)\n")
				else:
					c_add = Clique((c._X, (tp - delta, c._te),(c._tlimitb,c._tlimite)))
					c_add._deltamin=c._deltamin
                                        c_add._deltamax=c._deltamax
					self.addClique(c_add)
					#sys.stderr.write("Adding " + str(c_add) + " (left time delta extension)\n")
				is_max = False
			#else:
				#sys.stderr.write(str(c) + " cannot grow on the left side\n")

			# Grow node set
			candidates = c.getAdjacentNodes(self._times, self._nodes, delta)
			#sys.stderr.write("    Candidates : %s.\n" % (str(candidates)))

			for node in candidates:
                                isclique,first,last,maxinterval=c.isClique(self._times,node,delta)
				if isclique:
					Xnew = set(c._X).union([node])
					c_add = Clique((frozenset(Xnew), (c._tb, c._te),(min(c._tlimitb,min(first)),max(c._tlimite,max(last)))))
                                        c_add._deltamin=max(c._deltamin,maxinterval,c_add._tlimite-min(last),max(first)-c_add._tlimitb)
					tp,td=c_add.getTp(self._times,delta),c_add.getTd(self._times,delta)
				  	c_add._deltamax=minNone(c_add.getDeltamaxRight(self._times,td,delta),c_add.getDeltamaxLeft(self._times,tp,delta))

					if c_add._deltamin<c_add._deltamax:
						self._R.add(CliqueCritique((c_add._X,(c_add._tlimitb,c_add._tlimite),c_add._deltamin,c_add._deltamax,td,tp)))
					self.addClique(c_add)
					#sys.stderr.write("Adding " + str(c_add) + " (node extension)\n")
					is_max = False

			#if is_max:
				#sys.stderr.write(str(c) + " is maximal\n")
		return self._R



	def getDeltaCliques(self, delta):
		""" Returns a set of maximal cliques. """

		while len(self._S) != 0:
                        sys.stderr.write("S:"+ str(len(self._S)) + "\n")
			c = self.getClique()
			is_max = True

			# Grow time on the right side
			td = c.getTd(self._times, delta)
			if c._te != td + delta:
				new_t = c.getFirstTInInterval(self._times, self._nodes, td, delta)
				if new_t is not None:
					c_add = Clique((c._X, (c._tb, new_t)))
					sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")
					self.addClique(c_add)
				else:
					c_add = Clique((c._X, (c._tb, td + delta)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (time delta extension)\n")
				is_max = False
			#else:
				#sys.stderr.write(str(c) + " cannot grow on the right side\n")

			# Grow time on the left side 
			tp = c.getTp(self._times, delta)
			if c._tb != tp - delta:
				new_t = c.getLastTInInterval(self._times, self._nodes, tp, delta)
				if new_t is not None:
					c_add = Clique((c._X, (new_t , c._te)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + "(left time extension)\n")
				else:
					c_add = Clique((c._X, (tp - delta, c._te)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (left time delta extension)\n")
				is_max = False
			#else:
				#sys.stderr.write(str(c) + " cannot grow on the left side\n")

			# Grow node set
			candidates = c.getAdjacentNodes(self._times, self._nodes, delta)
			#sys.stderr.write("    Candidates : %s.\n" % (str(candidates)))

			for node in candidates:
				if c.isClique(self._times, node, delta):
					Xnew = set(c._X).union([node])
					c_add = Clique((frozenset(Xnew), (c._tb, c._te)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (node extension)\n")
					is_max = False

			if is_max:
				#sys.stderr.write(str(c) + " is maximal\n")
				self._R.add(c)
		return self._R
	



	def printCliques(self):
		out=sorted(list(self._R),key=operator.attrgetter('_deltamin'))
		for c in out:
			sys.stdout.write(str(c) + " \n")

	def __str__(self):
		msg = ""
		for c in self._R:
			msg += str(c) + "\n"
		return msg



def minNone(tlimitb,first):
	if tlimitb!=None:
		if first!=None:
			return min(tlimitb,first)
		else:
			return tlimitb
	elif first!=None:
		return first 
	else:
		return None
