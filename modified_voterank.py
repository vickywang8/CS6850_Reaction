"""
entropy_parameter: corresponds to the alpha parameter, only needs to be updated if we are doing testing that involves alpha
in vote_and_elect, change the True in votes_with_entropy to False if doing tests that involve alpha
in the infection function, change infected_bound and infection_rate accordingly
change num_initial_spreaders
"""

from collections import defaultdict
import random
import math

nodes_set = set()
edges_set = set()
node_neighbors_dict = {}

num_initial_spreaders = 200
elected_spreaders = set()
longest_shortest_path = 14
entropy_parameter = 100

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

def get_pj(node, target_node, neighbors_dict):
	return len(neighbors_dict[node])/sum([len(neighbors_dict[n]) for n in neighbors_dict[target_node]])

def get_entropy(target_node, neighbors_dict):
	numerator = sum([-get_pj(neighbor, target_node, neighbors_dict)*math.log(get_pj(neighbor, target_node, neighbors_dict)) for neighbor in neighbors_dict[target_node]])
	denominator = math.log(len(neighbors_dict[target_node]))
	if denominator == 0:
		return 0
	#print(target_node)
	#print(numerator/denominator)
	return numerator/denominator

def votes_with_entropy(num_votes_received, node, neighbors_dict, scale = True):
	if scale:
		return num_votes_received*get_entropy(node, neighbors_dict)
	else:
		return num_votes_received+entropy_parameter*get_entropy(node, neighbors_dict)*num_votes_received

def vote_and_elect(node_voting_info):
	node_with_max_votes = ""
	max_votes = 0
	for node, voting_info in node_voting_info.items():
		neighbors = neighbors_dict[node]
		num_votes_received = 0
		for neighbor in neighbors:
			num_votes_received += node_voting_info[neighbor][1]
		num_votes_received = votes_with_entropy(num_votes_received, node, neighbors_dict, True)
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

### JUST INFORMATION ENTROPY (NOT VOTERANK CODE)
# nodes_votes = []
# for node in nodes_set:
# 	nodes_votes.append((get_entropy(node, neighbors_dict), node))
# nodes_votes.sort()
# nodes_votes = nodes_votes[-num_initial_spreaders:]
# print(nodes_votes)
# elected_spreaders = [node for entropy,node in nodes_votes]
# print(elected_spreaders)

elected_spreaders = set(['8350', '88748', '46269', '2716', '48139', '26075', '88071', '31208', '35171', '95372', '71222', '34770', '92360', '79387', '21672', '11063', '48940', '23411', '72331', '100587', '99870', '102365', '86764', '49031', '93813', '34845', '91392', '87299', '41240', '97788', '73122', '30365', '73252', '51336', '24840', '83876', '42478', '42722', '28575', '72079', '22757', '66460', '28953', '8536', '34703', '77524', '52472', '72730', '55406', '45942', '74250', '95940', '58293', '7204', '80859', '60432', '61105', '45251', '16963', '36740', '85266', '79496', '57070', '28121', '905', '56672', '101472', '96245', '65099', '24047', '5215', '15345', '41266', '57340', '80915', '106876', '83197', '2962', '53906', '78667', '9991', '83824', '60662', '14096', '10099', '48875', '100439', '52287', '48626', '64278', '97632', '45769', '485', '45051', '66908', '62943', '8100', '83984', '32903', '62113', '97009', '32554', '20562', '23548', '9489', '57478', '74869', '99977', '60057', '56414', '103420', '21181', '26130', '1895', '15113', '57036', '98676', '2451', '81509', '71461', '101425', '85840', '93764', '97347', '53994', '6185', '44960', '101743', '90477', '17933', '74055', '55966', '83037', '37250', '32332', '29380', '30488', '86808', '90690', '84209', '22987', '24254', '42245', '23983', '38468', '101191', '107009', '73647', '52658', '52364', '36435', '46805', '35688', '83069', '91541', '37206', '69685', '53880', '7399', '94304', '33410', '47468', '53624', '49235', '101355', '9533', '22461', '36382', '50541', '18654', '15439', '8810', '27892', '52098', '60251', '58706', '43077', '12915', '72044', '83259', '31762', '20179', '55210', '61271', '59595', '62327', '96866', '1764', '11174', '46016', '46144', '79087', '14023', '26750', '35010', '34346', '40747', '88363', '23127', '96395'])

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












