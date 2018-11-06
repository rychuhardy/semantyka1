import networkx as nx
import pylab
import matplotlib.pyplot as plt
import pandas as pd

edge_file = 'out.txt'


G = nx.read_weighted_edgelist(edge_file, delimiter=';', encoding='utf-8')

color_map = {1:'#f09494', 2:'#eebcbc', 3:'#72bbd0', 4:'#91f0a1', 5:'#629fff', 6:'#bcc2f2',
             7:'#eebcbc', 8:'#f1f0c0', 9:'#d2ffe7', 10:'#caf3a6', 11:'#ffdf55', 12:'#ef77aa',
             13:'#d6dcff', 14:'#d2f5f0'}
plt.figure(figsize=(25,25))
options = {
    'edge_color': '#FFDEA2',
    'width': 1,
    'with_labels': True,
    'font_weight': 'regular',
}

#colors = [color_map[G.node[node]['group']] for node in G]
sizes = [sum(c[2]['weight'] for c in G.edges(node, data=True)) for node in G]



pos = nx.spring_layout(G, k=0.25, iterations=50)
nx.draw(G, pos=pos, node_size=sizes, **options)
ax = plt.gca()
ax.collections[0].set_edgecolor("#555555")
plt.show()
# pylab.figure(1)
# nx.draw(G, pos)
# nx.draw_networkx_edge_labels(G, pos)
#
# pylab.show()
