from collections import defaultdict
import random

nodes_set = set()
edges_set = set()
node_neighbors_dict = {}

num_initial_spreaders = 200
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
# node_voting_info = {}
# for node in nodes_set:
# 	node_voting_info[node] = (0, 1) # (number of votes received, voting power)
# while (len(elected_spreaders) < num_initial_spreaders):
# 	elected_node = vote_and_elect(node_voting_info)
# 	# print(elected_node)
# 	elected_spreaders.add(elected_node)
# 	node_voting_info[elected_node] = (0, 0)
# 	update_voting_ability(elected_node, neighbors_dict, node_voting_info, average_degree)
# print(elected_spreaders)

elected_spreaders = set(['10099', '83069', '37206', '101743', '1895', '35010', '26075', '25735', '60662', '36740', '8536', '87299', '30365', '106876', '27892', '61105', '89340', '905', '61271', '77524', '22461', '66908', '31762', '85266', '83037', '72044', '57070', '23548', '47468', '95372', '97347', '83259', '57478', '93764', '101425', '53880', '69685', '103420', '101472', '46805', '74869', '96866', '36435', '57340', '2451', '71461', '46066', '55210', '28575', '83824', '45942', '46144', '101355', '78667', '8810', '14023', '23411', '99977', '96245', '66460', '57036', '79387', '58293', '83876', '72331', '35688', '41240', '9533', '74250', '84209', '72730', '22987', '24840', '99870', '49031', '21181', '102365', '98676', '53994', '16963', '32554', '45769', '48139', '37250', '5215', '97632', '60251', '98553', '15345', '64278', '60432', '23127', '79496', '34703', '80859', '60057', '46016', '7399', '94304', '43077', '62113', '81509', '21672', '15113', '40747', '88748', '11063', '91392', '17933', '24254', '86764', '55966', '52658', '79087', '59595', '9489', '42478', '97009', '8350', '73122', '36382', '58706', '34346', '62327', '83197', '15439', '52364', '28121', '18654', '88363', '1034', '92360', '91541', '74055', '80915', '85796', '71222', '62943', '485', '101191', '52287', '34845', '56672', '29380', '72079', '97788', '90690', '31208', '96395', '95940', '28953', '1764', '53624', '35171', '45051', '26002', '51336', '32332', '12915', '34770', '9991', '30488', '48875', '107009', '52098', '46269', '56414', '86808', '49235', '52472', '45251', '48940', '100439', '83984', '38468', '48626', '2716', '100587', '88071', '8100', '53906', '41266', '14096', '11174', '6185', '90477', '2962', '7204', '73647', '85840', '33410', '26130', '22757', '73252', '20562', '55406', '44960', '26750', '93813', '50541'])
###################################

def infection(neighbors_dict, elected_spreaders, infected_bound = num_nodes*0.5, infection_rate = 0.8):
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
for i in range(0,10):
	avg+=infection(neighbors_dict, elected_spreaders)
print("Average # of time steps until convergence: " + str(avg/10))












