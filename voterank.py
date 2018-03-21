from collections import defaultdict

nodes_set = set()
edges_set = set()
node_neighbors_dict = {}

num_initial_spreaders = 20
elected_spreaders = []

with open('ca-CondMat.txt') as inputfile:
	for line in inputfile:
		nodes = line.strip().split()
		nodes.sort()
		int_nodes = []
		for node in nodes:
			nodes_set.add(int(node))
			int_nodes.append(int(node))
		edges_set.add(tuple(int_nodes))
num_nodes = len(nodes_set) 	#23133
num_edges = len(edges_set)	#93497

nodes_list = list(nodes_set)
nodes_list.sort()

neighbors_dict = defaultdict(set)
for (node_0, node_1) in edges_set:
	neighbors_dict[node_0].add(node_1)
	neighbors_dict[node_1].add(node_0)

# average degree of network
average_degree = 0
for node, neighbors in neighbors_dict.items():
	average_degree += len(neighbors)
average_degree /= num_nodes
print("average degree of the graph is :" + str(average_degree))

def vote_and_elect(node_voting_info):
	node_with_max_votes = ""
	max_votes = 0
	for node, voting_info in node_voting_info.items():
		neighbors = neighbors_dict[node]
		num_votes_received = 0
		for neighbor in neighbors:
			num_votes_received += node_voting_info[neighbor][1]
		if num_votes_received > max_votes:
			max_votes = num_votes_received
			node_with_max_votes = node
		node_voting_info[node] = num_votes_received
	return node_with_max_votes

def update_voting_ability(elected_node, neighbors_dict, node_voting_info, average_degree):
	for neighbor in neighbors_dict[elected_node]:
		new_voting_ability = node_voting_info[neighbor][1] - 1/average_degree
		node_voting_info[neighbor][1] = new_voting_ability if new_voting_ability >= 0 else 0

# initialize the algorithm
node_voting_info = {}
for node in nodes_list:
	node_voting_info[node] = (0, 1) # (number of votes received, voting power)
# print(node_voting_info)
while (len(elected_spreaders) < num_initial_spreaders):
	elected_node = vote_and_elect(node_voting_info)
	print(elected_node)
	elected_spreaders.append(elected_node)
	update_voting_ability(elected_node, neighbors_dict, node_voting_info, average_degree)
print(elected_spreaders)
