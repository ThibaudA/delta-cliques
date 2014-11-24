from CliqueMaster import CliqueMaster
from Clique import Clique
from CliqueCritique import CliqueCritique
import sys

Cm = CliqueMaster()
times = dict()
nodes = dict()
delta = int(sys.argv[1]) 
nb_lines = 0

for line in sys.stdin:
	contents = line.split(" ")
	t = int(contents[0])
	u = int(contents[1])
	v = int(contents[2])

	link = frozenset([u,v])
	time = (t,t)
	
      #if t==2:
#	Cm.addClique(Clique((link, time, time)))
#	Cm.addCliqueCritique(CliqueCritique((link,(t,t),0)))
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

cliquescritiques=[]
filenode=open(sys.argv[2], 'r')
for line in filenode:
	content=line.split(" ")
	cliquescritiques.append(CliqueCritique((frozenset(map(int,list(content[0].split(',')))),map(int,tuple(content[1].split(','))),int(content[2]))))


print map(str,sorted(cliquescritiques,Key=CliqueCritique._deltacritique))



Cm._times = times
Cm._nodes = nodes
sys.stderr.write("Processed " + str(nb_lines) + "from stdin\n")
R = Cm.ExtendCliqueCritique(delta)
#Cm.printCliques()	
