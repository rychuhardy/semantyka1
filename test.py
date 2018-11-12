import networkx as nx
import plotly.plotly as py
from plotly.graph_objs import *



edge_file = 'out.txt'


G = nx.read_weighted_edgelist(edge_file, delimiter=';', encoding='utf-8')
# remove weak nodes
toRemove = [node for node, degree in G.degree().items() if degree < 2]
G.remove_nodes_from(toRemove)


N = len(G.nodes())

pos=nx.fruchterman_reingold_layout(G)

Xv = [pos[k][0] for k in G.nodes()]
Yv = [pos[k][1] for k in G.nodes()]
Xed = []
Yed = []
weights = []
weights_extra = []
X_hidden = []
Y_hidden = []

for edge in G.edges():
    weights += [str(G.get_edge_data(edge[0], edge[1])['weight'])]
    weights_extra += [weights[-1] + ' ' + edge[0] + ' ' + edge[1]]
    Xed += [pos[edge[0]][0], pos[edge[1]][0], None]
    Yed += [pos[edge[0]][1], pos[edge[1]][1], None]
    X_hidden += [(pos[edge[0]][0] + pos[edge[1]][0])/2]
    Y_hidden += [(pos[edge[0]][1] + pos[edge[1]][1])/2]

max_weight = max(list(map(float, weights)))
inverted_weights = [(max_weight+1)]*len(weights)
inverted_weights = [i - float(j) for i, j in zip(inverted_weights, weights)]
idx = 0
for edge in G.edges():
    G.get_edge_data(edge[0], edge[1])['weight'] = inverted_weights[idx]
    idx += 1

trace3 = Scatter(x=Xed,
                 y=Yed,
                 mode='lines+text',
                 name='edges',
                 line=dict(color='rgb(210,210,210)', width=1),
                 text=weights,
                 hoverinfo='text',
                 hovertext=weights,
                 textposition='top center'
                 )
trace4 = Scatter(x=Xv,
                 y=Yv,
                 mode='markers+text',
                 name='nodes',
                 marker=dict(symbol='circle-dot',
                             size=5,
                             color='#6959CD',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
                 text=G.nodes(),

                 hoverinfo='text'
                 )

trace5 = Scatter(
    x = X_hidden,
    y = Y_hidden,
    mode='text',
    marker=dict(symbol='circle-dot',
                size=5,
                color='#6959CD',
                line=dict(color='rgb(50,50,50)', width=0.5)
                ),
    text=weights,
    hovertext=weights_extra,
    hoverinfo='text',
    hoveron='points+fills'
)

annot = "Graf skojarzeń dla słów: chłopiec, dziecko, mały, dziewczyna"


axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )
width=1200
height=1200
layout=Layout(title= "Graf skojarzeń dla słów: chłopiec, dziecko, mały, dziewczyna",
    font= dict(size=12),
    showlegend=False,
    autosize=False,
    width=width,
    height=height,
    xaxis=layout.XAxis(axis),
    yaxis=layout.YAxis(axis),
    margin=layout.Margin(
        l=40,
        r=40,
        b=85,
        t=100,
    ),
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            text='This igraph.Graph has the Kamada-Kawai layout',
            xref='paper',
            yref='paper',
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ]
    )

data1 = [trace3, trace4, trace5]
fig1 = Figure(data=data1, layout=layout)
fig1['layout']['annotations'][0]['text'] = annot
py.iplot(fig1, filename='semantyka1')

all_paths = nx.shortest_path_length(G, weight='weight')
paths2 = nx.all_pairs_dijkstra_path(G)

with open('weights2.txt', 'a', encoding='utf-8') as report:
    for src, target in all_paths.items():
        for second, value in target.items():
            if value > 0:
                report.write(f'{src} -> {second} (Distance: {value}, Nodes: {paths2[src][second]})\n')