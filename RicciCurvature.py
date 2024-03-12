import networkx as nx
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# summation for FRC 
# input will be the node's name, its weight, the edge's weight, and a list of in edges, 
# the output will be the summation of the node to plun into the FRC formula
def summation(v_name, v_weight, e_weight, target, G):
    frc_sum = 0
    for (v1, v2) in G.in_edges(target):
        if v_name is not v1:
            frc_sum += v_weight / (sqrt(e_weight * G[v1][target]['weight']))
    return frc_sum
    

# FRC
# input: a netowrk x graph and a hashtable of the verticies' weights
# output: a hashtable of the edges with their Forman Ricci curvature 
def formanRicciCurvature(G, wHashmap):
    return_map = {}

    for (v1, v2) in G.edges():

        # account for the weight of edges that aren't don't have incoming edges (they're not in the hashmap)
        target_edge_weight = G[v1][v2]['weight']
        if v1 in wHashmap:
            v1_weight = wHashmap[v1]
        else:
            v1_weight = 0 

        if v2 in wHashmap:
            v2_weight = wHashmap[v2]
        else:
            v2_weight = 0             

        # this formula has been taken from Jost Juergen's research papers
        frc = target_edge_weight * ( (v1_weight/target_edge_weight) + (v2_weight/target_edge_weight) - summation(v2, v1_weight, target_edge_weight, v1, G) - summation(v1, v2_weight, target_edge_weight, v2, G))

        # since there are directed & undirected edges in this graph, and E(i,j) = E(j,i) in an undirected graph. I will check if the opposite 
        # is in the graph to add up the two directed calculations that should be an undirected calculation
        if (v2, v1) not in return_map:
            return_map[(v1,v2)] = round(frc,2)
        else:
            return_map[(v2,v1)] = round(frc,2)

    return return_map

# create the directional grpah
G = nx.DiGraph()

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

# undirected 
G.add_edge("S2C","R1K", weight=1)
G.add_edge("R1K","S2C", weight=1)
G.add_edge("S2I","R1K", weight=6)
G.add_edge("R1K","S2I", weight=6)
G.add_edge("S2I","R1M", weight=5)
G.add_edge("R1M","S2I", weight=5)


# NetworkX has diffuclty determing the weight of a node. To work arround this I will use a hashmap
# to keep the algrothm O(n). Since the graph is directed, only incomind edges will contribute to the 
# weight of the vertex. the incomind edge will  be they key and teh edges' weights will be the values.

weight_hashmap = {}
for (v1, v2) in G.edges():
    if v2 not in weight_hashmap:
        weight_hashmap[v2] = G[v1][v2]['weight']
    else:
        weight_hashmap[v2] = weight_hashmap[v2] + G[v1][v2]['weight']

frc_map = formanRicciCurvature(G, weight_hashmap)

pos = {"S3A":(1,4),"S3B":(1,3), "S3G":(1,2), "S3H":(1,1),
       "S2C":(3,4),"S2D":(3,3),"S2I":(3,1.8),
       "S1E":(5,3.5), "S1L":(5,2),
       "TC":(7,2.75),
       "R1K":(9,3.5),"R1M":(9,2),
       "R2N":(11,3.5),"R2O":(11,2),
       "R3R":(13,4),"R3S":(13,3),"R3T":(13,2),}

figure(figsize=(12,6.5))
plt.title("Forman Ricci Curvature")
nx.draw(G, pos, with_labels=True, node_size = 750, alpha = 0.75)
nx.draw_networkx_edge_labels(
    G, pos, edge_labels= frc_map,
    font_color='black', alpha=0.9)
plt.show()