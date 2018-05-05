from collections import defaultdict
import random

nodes_set = set()
edges_set = set()
node_neighbors_dict = {}

num_initial_spreaders = 1
elected_spreaders = set()
longest_shortest_path = 14

with open('ca-CondMat.txt') as inputfile:
	for line in inputfile:
		nodes = line.strip().split()
		nodes.sort()
		for node in nodes:
			nodes_set.add(node)
		edges_set.add(tuple(nodes))
num_nodes = len(nodes_set) 	#23133
num_edges = len(edges_set)	#93497

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
		node_voting_info[node] = (num_votes_received, node_voting_info[node][1])
	return node_with_max_votes

def update_voting_ability(elected_node, neighbors_dict, node_voting_info, average_degree):
	for neighbor in neighbors_dict[elected_node]:
		new_voting_ability = node_voting_info[neighbor][1] - 1/average_degree
		if new_voting_ability >= 0:
			node_voting_info[neighbor] = (node_voting_info[neighbor][0], new_voting_ability)
		else:
			node_voting_info[neighbor] = (node_voting_info[neighbor][0], 0)

# initialize the algorithm
node_voting_info = {}
for node in nodes_set:
	node_voting_info[node] = (0, 1) # (number of votes received, voting power)
while (len(elected_spreaders) < num_initial_spreaders):
	elected_node = vote_and_elect(node_voting_info)
	# print(elected_node)
	elected_spreaders.add(elected_node)
	node_voting_info[elected_node] = (0, 0)
	update_voting_ability(elected_node, neighbors_dict, node_voting_info, average_degree)
print(elected_spreaders)

###################################

def infection(neighbors_dict, elected_spreaders, infected_bound = num_nodes*0.5, infection_rate = 0.5):
	infected_set = set(elected_spreaders)
	newly_infected_set = set()
	t = 0
	while len(infected_set) < infected_bound:
		for infected_node in infected_set:
			neighbor = random.choice(list(neighbors_dict[infected_node]))
			if random.uniform(0,1) <= infection_rate:
				newly_infected_set.add(neighbor)
		t+=1
		infected_set = infected_set.union(newly_infected_set)
	return t

# run infection
avg = 0
for i in range(0,100):
	avg+=infection(neighbors_dict, elected_spreaders)
print("Average # of time steps until convergence: " + str(avg/100))












