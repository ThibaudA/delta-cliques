from CliqueMaster import CliqueMaster,minNone
from Clique import Clique
from CliqueCritique import CliqueCritique
import sys
import bisect

Cm = CliqueMaster()
times = dict()
nodes = dict()
delta = int(sys.argv[1]) 
nb_lines = 0
stock=[]
for line in sys.stdin:
	contents = line.split(" ")
	t = int(contents[0])
	u = int(contents[1])
	v = int(contents[2])

	link = frozenset([u,v])
	time = (t,t)
	
        #if t==2:
	stock.append(CliqueCritique((link,(t,t),0,delta,t,t)))
	# Populate data structures
	if not times.has_key(link):
		times[link] = []
	times[link].append(t)

        if not u in nodes:
		nodes[u] = set()

	if not v in nodes:
		nodes[v] = set()

	nodes[u].add(v)
        nodes[v].add(u)
	nb_lines = nb_lines + 1

for c in stock:
	index=times[c._X].index(c._tlimite)
	lenght=len(times[c._X])
	if not (index==0 and  index==lenght-1):
		c._deltamax=abs(c._tlimite-minNone(times[c._X][index+1] if index != lenght-1 else delta,times[c._X][index-1] if index!=0 else delta))
	
	c_add=Clique((c._X,(c._tlimite,c._tlimite),(c._tlimite,c._tlimite)))
	c_add._deltamax=c._deltamax
	Cm.addClique(c_add)
	Cm._R.add(c)
	
Cm._times = times
Cm._nodes = nodes
sys.stderr.write("Processed " + str(nb_lines) + "from stdin\n")
R = Cm.getTree(delta)
Cm.printCliques()	


