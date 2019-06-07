import plotly
import plotly.graph_objs as go
import networkx as nx
import os
from datetime import datetime


def take_input():
    node_list = list()
    edge_list = list()
    take_input_control = True
    while take_input_control:
        print("Type 'q' to move on")

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


def parse_G(G):
    # --- random position
    # for node in G.nodes:
    #     G.nodes[node]['pos'] = (random.gauss(0, 2), random.gauss(0, 2))
    # pos = nx.get_node_attributes(G, 'pos')

    # --- optimized position
    pos_spring = nx.spring_layout(G)
    for node in G.nodes:
        G.nodes[node]['pos'] = tuple(pos_spring[node].tolist())

    # # ---- shortest path calc ----
    # dmin = 1
    # ncenter = list(G.nodes)[0]
    # for n in pos:
    #     x, y = pos[n]
    #     d = (x - 0.5) ** 2 + (y - 0.5) ** 2
    #     if d < dmin:
    #         ncenter = n
    #         dmin = d
    # p = nx.single_source_shortest_path_length(G, ncenter)
    betweeness_centrality = nx.betweenness_centrality(G)

    # ----- Create edges -----
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=[],
            colorbar=dict(
                thickness=15,
                title='Betweenness Centrality',
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
        # node_trace['marker']['color'] += tuple([len(adjacencies[1])])
        node_trace['marker']['color'] += tuple([betweeness_centrality[list(betweeness_centrality)[node]]])
        node_trace['marker']['size'] += tuple([len(adjacencies[1]) * 10])
        # node_info = 'Name: ' + str(list(G.nodes())[node]) + ', # of connections: ' + str(len(adjacencies[1]))
        node_info = str(list(G.nodes())[node])
        node_trace['text'] += tuple([node_info])

    return edge_trace, node_trace


def main(G, add_new_input):
    # ---- generate from input
    if add_new_input:
        node_list, edge_list = take_input()
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

    # ----- FUNCTION REPLACE -----
    edge_trace, node_trace = parse_G(G)

    # ----- Create network graph -----
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Network graph made with Python',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Python code: <a href='https://github.com/mallory-archer/cocktail_party/'> https://github.com/mallory-archer/cocktail_party/</a>",
                            showarrow=False,
                            xref='paper', yref='paper', x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    plotly.offline.plot(fig)

    return G


# ----- Set control params -----
add_new_input = False
save_graph = True
saved_graph_folder = 'network_graphs'

# Pre-calcs
saved_graph_filepath_head = os.path.join(os.getcwd(), saved_graph_folder)

# ----- INITIALIZE GRAPH -----
# ----- Start with blank graph -----
# G = nx.Graph()

# ---- specify nodes from list -----
# G = nx.Graph()
# G.add_nodes_from(["Grace", "Dan", "Liz"])
# G.add_edges_from([("Grace", "Dan"), ("Grace", "Liz")])

# ---- read in graph ----
read_file_name = 'G_20190607_182226'
G = nx.read_gpickle(os.path.join(saved_graph_filepath_head, read_file_name + '.gpickle'))

if __name__ == '__main__':
    CLI_active = True
    while CLI_active:
        G = main(G, add_new_input)
        print('Continue inputing data? [y/n]: ')
        CLI_active = input()
        if CLI_active == 'n':
            CLI_active = False
            print('Would end input')
            break
    if save_graph:
        saved_graph_filename = 'G_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.gpickle'
        nx.write_gpickle(G, os.path.join(saved_graph_filepath_head, saved_graph_filename))




