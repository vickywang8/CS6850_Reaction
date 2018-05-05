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
elected_spreaders = []
entropy_parameter = 1

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
		num_votes_received = votes_with_entropy(num_votes_received, node, neighbors_dict, False)
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

### JUST INFORMATION ENTROPY (NOT VOTERANK CODE)
# nodes_votes = []
# for node in nodes_set:
# 	nodes_votes.append((get_entropy(node, neighbors_dict), node))
# nodes_votes.sort()
# nodes_votes = nodes_votes[-num_initial_spreaders:]
# print(nodes_votes)
# elected_spreaders = [node for entropy,node in nodes_votes]
# print(elected_spreaders)

condmat_elected_spreaders_without_alpha_200 = ['73647', '52658', '78667', '97632', '101425', '97788', '95372', '22987', '22757', '91392', '83259', '46269', '101355', '15439', '101191', '11063', '84209', '26075', '8536', '29380', '46016', '9991', '31762', '26750', '56672', '55210', '905', '95940', '107009', '61271', '73122', '102365', '57070', '71461', '33410', '485', '1895', '7399', '2716', '15345', '12915', '14096', '88363', '106876', '35010', '37206', '35171', '83197', '96395', '57340', '72331', '18654', '53994', '50541', '80915', '17933', '96866', '15113', '52364', '2962', '85266', '62113', '27892', '92360', '101743', '41266', '99977', '62327', '30365', '90690', '9533', '83824', '97009', '26130', '36740', '73252', '83069', '64278', '28953', '36382', '58706', '45942', '48139', '103420', '60057', '60251', '69685', '34845', '91541', '31208', '7204', '72730', '99870', '51336', '6185', '60662', '23411', '74055', '23127', '57478', '38468', '71222', '94304', '21672', '1764', '23548', '88748', '53906', '83037', '53880', '74869', '43077', '93813', '8350', '35688', '97347', '20562', '48940', '66460', '28121', '34770', '21181', '77524', '56414', '47468', '79087', '58293', '57036', '55406', '74250', '48875', '53624', '24840', '36435', '83876', '80859', '79387', '2451', '8100', '46144', '32554', '86764', '72044', '101472', '88071', '49235', '87299', '60432', '86808', '46805', '52472', '59595', '37250', '61105', '49031', '85840', '98676', '9489', '11174', '100439', '10099', '34346', '8810', '52287', '32332', '96245', '41240', '45769', '100587', '22461', '14023', '45251', '40747', '16963', '52098', '24254', '5215', '28575', '72079', '81509', '79496', '44960', '90477', '34703', '62943', '55966', '30488', '42722', '45051', '65099', '42478', '66908', '83984', '32903', '20179', '42245', '93764', '24047', '48626', '23983']
condmat_elected_spreaders_with_alpha_1_200 = ['73647', '52658', '78667', '97632', '101425', '97788', '95372', '22987', '22757', '91392', '83259', '46269', '101355', '15439', '101191', '26075', '84209', '11063', '46016', '8536', '29380', '9991', '31762', '56672', '26750', '55210', '95940', '905', '107009', '61271', '73122', '57070', '102365', '71461', '12915', '485', '33410', '2716', '1895', '7399', '15345', '83197', '14096', '88363', '35171', '35010', '106876', '37206', '96395', '72331', '57340', '18654', '53994', '17933', '80915', '50541', '96866', '15113', '52364', '85266', '27892', '2962', '90690', '62113', '101743', '92360', '41266', '99977', '83824', '36740', '62327', '30365', '9533', '64278', '26130', '97009', '83069', '73252', '38468', '28953', '91541', '6185', '103420', '34845', '36382', '23127', '60251', '48139', '58706', '69685', '60662', '74055', '7204', '51336', '31208', '45942', '23548', '72730', '23411', '60057', '99870', '53906', '88748', '1764', '35688', '57478', '71222', '53880', '94304', '21672', '74869', '83037', '8350', '43077', '97347', '48940', '93813', '21181', '34770', '79087', '20562', '57036', '56414', '66460', '28121', '2451', '77524', '24840', '47468', '48875', '58293', '55406', '74250', '46144', '101472', '80859', '86764', '83876', '53624', '79387', '36435', '88071', '8100', '32554', '52287', '72044', '87299', '5215', '85840', '49235', '9489', '60432', '37250', '49031', '33099', '86808', '11174', '59595', '98676', '61105', '28575', '52472', '46805', '8810', '32332', '41240', '100439', '34346', '45769', '14023', '89340', '10099', '96245', '22461', '52098', '24254', '40747', '25735', '30488', '16963', '100587', '81509', '45251', '55966', '34703', '72079', '42478', '62943', '44960', '79496', '90477', '66908', '85796', '93764', '83984', '46066', '48626', '32903', '20179', '42245']

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
# avg = 0
# for i in range(0,10):
# 	avg+=infection(neighbors_dict, elected_spreaders)
# print("Average # of time steps until convergence: " + str(avg/10))












