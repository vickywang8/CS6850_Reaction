from collections import defaultdict
import random

nodes_set = set()
edges_set = set()
node_neighbors_dict = {}

num_initial_spreaders = 200
elected_spreaders = []
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
	if elected_node not in elected_spreaders:
		elected_spreaders.append(elected_node)
	node_voting_info[elected_node] = (0, 0)
	update_voting_ability(elected_node, neighbors_dict, node_voting_info, average_degree)
print(elected_spreaders)

cond_mat_elected_spreaders_200 = ['73647', '52658', '78667', '97632', '101425', '97788', '95372', '22987', '22757', '91392', '83259', '46269', '101355', '15439', '101191', '26075', '84209', '46016', '11063', '29380', '8536', '9991', '31762', '56672', '26750', '55210', '95940', '905', '107009', '73122', '61271', '102365', '57070', '71461', '12915', '485', '33410', '2716', '15345', '1895', '83197', '88363', '72331', '14096', '96395', '35010', '37206', '106876', '35171', '7399', '17933', '15113', '96866', '80915', '57340', '52364', '53994', '90690', '18654', '50541', '85266', '27892', '2962', '99977', '41266', '26130', '101743', '36740', '62113', '92360', '64278', '62327', '9533', '30365', '83824', '38468', '97009', '83069', '73252', '91541', '60662', '34845', '74055', '6185', '103420', '23127', '28953', '36382', '60251', '69685', '58706', '48139', '23548', '53906', '7204', '47468', '51336', '88748', '35688', '72730', '31208', '57036', '60057', '53880', '99870', '1764', '21672', '45942', '57478', '34770', '94304', '71222', '8350', '23411', '83037', '79087', '48940', '101472', '97347', '21181', '2451', '24840', '56414', '86764', '46144', '20562', '74869', '30488', '48875', '93813', '28121', '74250', '43077', '55406', '77524', '58293', '66460', '80859', '5215', '83876', '32554', '87299', '52287', '53624', '8100', '36435', '85840', '9489', '28575', '79387', '72044', '49235', '11174', '37250', '49031', '60432', '45769', '46805', '66908', '59595', '86808', '14023', '41240', '98676', '61105', '89340', '88071', '10099', '34346', '8810', '100439', '32332', '52098', '52472', '22461', '96245', '93764', '42478', '85796', '24254', '55966', '1034', '25735', '40747', '81509', '34703', '26002', '16963', '46066', '62943', '98553', '44960', '100587', '72079', '45251', '79496', '83984', '48626', '90477', '45051']
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
for i in range(0,10):
	avg+=infection(neighbors_dict, elected_spreaders)
print("Average # of time steps until convergence: " + str(avg/10))












