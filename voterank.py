nodes_set = set()
edges_set = set()
node_neighbors_dict = {}
with open('ca-CondMat.txt') as inputfile:
	for line in inputfile:
		nodes = line.strip().split()
		nodes.sort()
		for node in nodes:
			nodes_set.add(node)
		edges_set.add(tuple(nodes))
print(len(nodes_set)) 	#23133
print(len(edges_set))	#93497