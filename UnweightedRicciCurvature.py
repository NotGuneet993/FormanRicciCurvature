import networkx as nx
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# summation for FRC 
# input will be the node's name, its weight, the edge's weight, and a list of in edges, 
# the output will be the summation of the node to plun into the FRC formula
def summation(exclude_node, focus_node, edge_weight, foucs_node_weight, G):
    sum = 0
    for (v1,v2) in G.edges(focus_node):
        if v2 is not exclude_node:
            sum += foucs_node_weight /(sqrt(edge_weight*G[v1][v2]['weight']))
    return sum
    

# FRC
# input: a netowrk x graph and a hashtable of the verticies' weights
# output: a hashtable of the edges with their Forman Ricci curvature 
def formanRicciCurvature(G, wHashmap):
    return_map = {}

    for (v1, v2) in G.edges():
        target_edge_weight = G[v1][v2]['weight']
        v1_weight = wHashmap[v1]
        v2_weight = wHashmap[v2]
          
        # this formula has been taken from Jost Juergen's research papers
        frc = target_edge_weight * ( (v1_weight/target_edge_weight) + (v2_weight/target_edge_weight) - summation(v2, v1, target_edge_weight, v1_weight, G) - summation(v1, v2, target_edge_weight, v2_weight, G))

        return_map[(v1,v2)] = round(frc,2)
    return return_map

G = nx.Graph()

# Green
G.add_edge("S3A","S2C", weight=1)
G.add_edge("S2C","S1E", weight=2)
G.add_edge("S3B","S2D", weight=3)
G.add_edge("S2D","S1E", weight=2)
G.add_edge("S3G","S2I", weight=1)
G.add_edge("S3H","S2I", weight=2)
G.add_edge("S2I","S1L", weight=4)

# Yellow
G.add_edge("S1E","TC", weight=3)
G.add_edge("S1L","TC", weight=6)
G.add_edge("TC","R1K", weight=4)
G.add_edge("TC","R1M", weight=3)

# red
G.add_edge("R1K","R2N", weight=4)
G.add_edge("R1M","R2O", weight=2)
G.add_edge("R2N","R3R", weight=1)
G.add_edge("R2N","R3S", weight=5)
G.add_edge("R2O","R3T", weight=4)
G.add_edge("R3S","R3T", weight=2)

# across green & red
G.add_edge("S2C","R1K", weight=1)
G.add_edge("S2I","R1K", weight=6)
G.add_edge("S2I","R1M", weight=5)


# NetworkX has diffuclty determing the weight of a node. To work arround this I will use a hashmap
# to keep the algrothm O(n). Since the graph is directed, only incomind edges will contribute to the 
# weight of the vertex. the incomind edge will  be they key and teh edges' weights will be the values.

weight_hashmap = {}
for node in list(G.nodes()):
    weight_hashmap[node] = sum([G[v1][v2]['weight'] for (v1,v2) in G.edges(node)])

frc_map = formanRicciCurvature(G, weight_hashmap)

# coordinates to shape the graph. 
pos = {"S3A":(1,4),"S3B":(1,3), "S3G":(1,2), "S3H":(1,1),
       "S2C":(3,4),"S2D":(3,3),"S2I":(3,1.8),
       "S1E":(5,3.5), "S1L":(5,2),
       "TC":(7,2.75),
       "R1K":(9,3.5),"R1M":(9,2),
       "R2N":(11,3.5),"R2O":(11,2),
       "R3R":(13,4),"R3S":(13,3),"R3T":(13,2),}

colors = ['green','green','green','green','green','green','green','green','green',
          'yellow',
          'red','red','red','red','red','red','red']

figure(figsize=(12,6.5))
plt.title("Forman Ricci Curvature (Undirected graph)")
nx.draw(G, pos, with_labels=True, node_size = 750, alpha = 0.75, node_color=colors)
nx.draw_networkx_edge_labels(
    G, pos, edge_labels= frc_map,
    font_color='black', alpha=0.9)
plt.show()