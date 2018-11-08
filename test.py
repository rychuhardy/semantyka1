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
for edge in G.edges():
    weights += [str(G.get_edge_data(edge[0], edge[1])['weight'])]
    Xed += [pos[edge[0]][0], pos[edge[1]][0], None]
    Yed += [pos[edge[0]][1], pos[edge[1]][1], None]

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

data1 = [trace3, trace4]
fig1 = Figure(data=data1, layout=layout)
fig1['layout']['annotations'][0]['text'] = annot
py.iplot(fig1, filename='semantyka1')