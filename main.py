import plotly
# import plotly.plotly as py
import plotly.graph_objs as go

import networkx as nx
import random


def take_input():
    node_list = list()
    edge_list = list()
    take_input_control = True
    while take_input_control:
        print("type 'q' to quit")

        name = input("Enter your name: ")
        if name == 'q':
            break
        node_list.append(name)
        # print('Your name is: ' + name)

        while take_input_control:
            connection = input("Enter a friend's name: ")
            if connection == 'q':
                take_input_control = False
                break
            edge_list.append((name, connection))
            node_list.append(connection)
            # print("Your friend's name is: " + connections)
    return node_list, edge_list


def main(G):
    # ----- Get node positions -----
    # ---- randomly generate
    # G = nx.random_geometric_graph(200, 0.125)

    # ---- specify nodes
    # G = nx.Graph()
    # G.add_nodes_from(["Grace", "Dan", "Liz"])
    # G.add_edges_from([("Grace", "Dan"), ("Grace", "Liz")])

    # ---- generate from input
    node_list, edge_list = take_input()
    G.add_nodes_from(node_list)
    # G.add_nodes_from([connections])
    G.add_edges_from(edge_list)

    # p = {i: (random.gauss(0, 2), random.gauss(0, 2)) for i in range(len(G.nodes))}
    for node in G.nodes:
        # G.nodes[node]['pos'] = p[node]
        G.nodes[node]['pos'] = (random.gauss(0, 2), random.gauss(0, 2))
    pos = nx.get_node_attributes(G, 'pos')

    dmin = 1
    ncenter = list(G.nodes)[0]
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d

    p = nx.single_source_shortest_path_length(G, ncenter)

    # ----- Create edges -----
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    # ----- Code node points -----
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([len(adjacencies[1])])
        node_info = '# of connections: ' + str(len(adjacencies[1]))
        node_trace['text'] += tuple([node_info])

    # ----- Create network graph -----
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Network graph made with Python',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                            showarrow=False,
                            xref='paper', yref='paper', x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    # py.iplot(fig, filename='networkx')
    plotly.offline.plot(fig)
    return G


G = nx.Graph()
for i in range(3):
    G = main(G)

