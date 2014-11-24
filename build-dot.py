import sys

nodes = set()
links = ""

sys.stdout.write("graph G {\n")
for line in sys.stdin:
    if line[0] == "G":
        X = line.strip().split(" ")[2] 
        b = line.strip().split(" ")[3].split(",")[0]
        e = line.strip().split(" ")[3].split(",")[1]
        
        u = "({" + X +"}, [" + b + ";" + e + "])"
        out = ""
        adds = 0
    elif line[0] == "A":
        X = line.strip().split(" ")[1] 
        b = line.strip().split(" ")[2].split(",")[0]
        e = line.strip().split(" ")[2].split(",")[1]
        v = "({" + X +"}, [" + b + ";" + e + "])"
        
        nodes.add(u)
        nodes.add(v)
	if line.strip().split(" ")[6]=='(time':
        	out =  "\"" + u + "\" -- \"" + v +"\" [color=green];\n"
	elif line.strip().split(" ")[6]=='(left':
        	out =  "\"" + u + "\" -- \"" + v +"\" [color=red];\n"
	else:
		out =  "\"" + u + "\" -- \"" + v +"\" [color=blue];\n"


        adds = 1
    if adds:
        links += out

for node in nodes:
    sys.stdout.write("\"" + node + "\" [shape=ellipse];\n")

sys.stdout.write(links)

sys.stdout.write("}\n")
