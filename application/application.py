import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import networkx as nx
# import os

import plotly.graph_objs as go



# Step 1. Launch the application
app = dash.Dash()
application = app.server

# ---- DEF FUNTCTIONS
def create_edges(G):
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

    return edge_trace


def create_nodes(G, color_dimension):
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
        node_trace['marker']['color'] += tuple([color_dimension[list(color_dimension)[node]]])
        node_trace['marker']['size'] += tuple([len(adjacencies[1]) * 10])
        node_info = str(list(G.nodes())[node])
        node_trace['text'] += tuple([node_info])

    return node_trace


def parse_G(G):
    # --- optimized position
    pos_spring = nx.spring_layout(G)
    for node in G.nodes:
        G.nodes[node]['pos'] = tuple(pos_spring[node].tolist())

    betweeness_centrality = nx.betweenness_centrality(G)

    # ----- Create edges -----
    edge_trace = create_edges(G)

    # ----- Create nodes ----
    node_trace = create_nodes(G, betweeness_centrality)

    return edge_trace, node_trace


def create_fig_data(G):
    edge_trace, node_trace = parse_G(G)
    data = [edge_trace, node_trace]
    layout = go.Layout(title='<br>Network graph made with Python',
                       titlefont=dict(size=16),
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20, l=5, r=5, t=40),
                       annotations=[dict(
                           text="Python code: <a href='https://github.com/mallory-archer/cocktail_party/'> https://github.com/mallory-archer/cocktail_party/</a>",
                           showarrow=False,
                           xref='paper', yref='paper', x=0.005, y=-0.002)],
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

    return data, layout


# Step 2. Import the dataset
# saved_graph_folder = 'network_graphs'
# saved_graph_filepath_head = os.path.join(os.getcwd(), saved_graph_folder)
# read_file_name = 'G_20190607_182226'
# G = nx.read_gpickle(os.path.join(saved_graph_filepath_head, read_file_name + '.gpickle'))
G = nx.Graph()

# G = nx.read_gpickle('C:/Users/Grace/Dropbox/cocktail_party/test_graph.gpickle')

# Step 3. Create a plotly figure
data, layout = create_fig_data(G)
fig = go.Figure(data=data, layout=layout)

# Step 4. Create a Dash layout
app.layout = html.Div([
    # a header and a paragraph
    html.Div([
        html.H1("Cocktail Party"),
    ],
        style={'padding': '5px',
               'backgroundColor': '#3aaab2'}),
    # adding a plot
    dcc.Graph(id='plot', figure=fig),
    html.Div(dcc.Input(id='input-box', type='text')),
    html.Div(dcc.Input(id='input-box-friend', type='text')),
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button-friend')
])


# Step 5. Add callback functions
@app.callback(Output('plot', 'figure'),
              [Input('button', 'n_clicks')],
              [State('input-box', 'value'), State('input-box-friend', 'value'), State('plot', 'figure')]
              )    # Output('output-container-button', 'children')  [Input('button', 'n_clicks'), ,
def update_figure(n_clicks, value, value_friend, fig_updated):
    if value and value_friend:
        G.add_nodes_from([value])
        G.add_edges_from([(value, value_friend)])
        data_temp, layout_temp = create_fig_data(G)
        fig_updated = go.Figure(data=data_temp, layout=layout_temp)
    return fig_updated


# Step 6. Add the server clause
if __name__ == '__main__':
    # app.run_server(debug=True)
    application.run(debug=True, port=8080)  # Beanstalk expects it to be running on 8080.
