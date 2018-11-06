import networkx as nx
import pylab

edge_file = 'out.txt'

G = nx.read_weighted_edgelist(edge_file, delimiter=';', encoding='utf-8')

pos = nx.spring_layout(G)
pylab.figure(1)
nx.draw(G, pos)
nx.draw_networkx_edge_labels(G, pos)

pylab.show()

print("Ok")
