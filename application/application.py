import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import networkx as nx
import matplotlib
from matplotlib import cm
import plotly.graph_objs as go
import numpy as np


# ---- DEF FUNTCTIONS
def truncate_colormap(cmap_totrunc, minval, maxval, n=100):
    new_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap_totrunc.name, a=minval, b=maxval),
        cmap_totrunc(np.linspace(minval, maxval, n)))
    return new_cmap


def matplotlib_to_plotly(cmap, pl_entries, reverse_colorscale, min_colormap_val, max_colormap_val):
    cmap = truncate_colormap(cmap, minval=min_colormap_val, maxval=max_colormap_val)

    h = 1.0 / (pl_entries - 1)
    index_temp = []
    pl_colorscale_temp =[]

    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k * h)[:3]) * 255))
        index_temp.append(k * h)
        pl_colorscale_temp.append('rgb' + str((C[0], C[1], C[2])))

    if reverse_colorscale:
        pl_colorscale_temp.reverse()

    pl_colorscale = list(map(list, zip(index_temp, pl_colorscale_temp)))

    return pl_colorscale


def create_edges(G):
    edge_trace = go.Scatter(
        x=[],
        y=[],
        hoverinfo='none',
        mode='lines',
        line=dict(width=0.5, color='#E9DDE1'))
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])
    return edge_trace


def create_nodes(G, color_dimension, node_color_map):
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale=node_color_map,
            reversescale=False,
            line=dict(
                width=2,
                color='#5c595a'
            ),
            color=[],
            size=[],
            opacity=1,
            colorbar=dict(
                thickness=15,
                title='Betweenness Centrality',
                titlefont=dict(
                    color='#E9DDE1',
                    family='monospace'
                ),
                xanchor='left',
                titleside='right',
                tickfont=dict(
                    color='#E9DDE1',
                    family='monospace'
                )

            )
        ),
        textfont=dict(
            family='monospace',
            color='#E9DDE1'
        ),
        textposition='bottom center'
    )

    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    # ----- Code node points -----
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([color_dimension[list(color_dimension)[node]]])
        node_trace['marker']['size'] += tuple([len(adjacencies[1]) * 5])
        node_info = str(list(G.nodes())[node])
        # node_info2 = str(color_dimension[list(color_dimension)[node]])
        # node_info_agg = node_info + ' centrality: ' + node_info2
        node_trace['text'] += tuple([node_info])
        # node_trace['hoverinfo'] += tuple([node_info_agg])

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
    node_trace = create_nodes(G, betweeness_centrality, node_color_map=magma_cmap)     #'YlGnBu'

    return edge_trace, node_trace


def create_fig_data(G):
    edge_trace, node_trace = parse_G(G)

    try:
        most_influential = node_trace['text'][node_trace['marker']['color'].index(max(node_trace['marker']['color']))]
    except:
        most_influential = ''

    data = [edge_trace, node_trace]
    layout = go.Layout(showlegend=False,
                       hovermode='closest',
                       dragmode='pan',
                       margin=dict(b=20, l=5, r=5, t=40),
                       annotations=[dict(
                           text="Most influential: "+most_influential,
                           showarrow=False,
                           xref='paper',
                           yref='paper',
                           x=0.005,
                           y=-0.002,
                           font=dict(
                               color='#E9DDE1',
                               family='monospace'
                           )
                       )],
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       paper_bgcolor='#5c595a',
                       plot_bgcolor='#5c595a')
    return data, layout


# ---- DEF PARAMS
relationship_dict = {'school': {'label': 'school', 'color': '#ee5c5d'},
                     'work': {'label': 'work', 'color': '#ee5c5d'},
                     'roommate': {'label': 'roommate', 'color': '#ee5c5d'},
                     'mutual_friend': {'label': 'mutual friends', 'color': '#ee5c5d'},
                     'romantic': {'label': 'dating/married, current/previous', 'color': '#ee5c5d'},
                     'family': {'label': 'family (excl. spouse)', 'color': '#5c595a'},
                     'childhood': {'label': 'childhood', 'color': '#5c595a'},
                     'other': {'label': 'other', 'color': '#ee5c5d'}
                     }
dropdown_labels = [{'value': key, 'label': value['label']} for key, value in relationship_dict.items()]
magma_cmap_temp = matplotlib.cm.get_cmap('magma')
magma_cmap = matplotlib_to_plotly(magma_cmap_temp, 255, reverse_colorscale=False, min_colormap_val=0.3, max_colormap_val=1)

# Step 1. Launch the application
app = dash.Dash(__name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

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
    html.Div(children=html.Div([html.H1("Have we met?")])),
    # adding a plot
    dcc.Graph(id='plot', figure=fig),
    html.Div(dcc.Input(id='input-box', type='text', placeholder='Enter your First_name Last_name')),
    html.Div(dcc.Input(id='input-box-friend', type='text', placeholder="Enter friend's First_name Last_name")),
    html.Div(
        dcc.Dropdown(
            id='relationship',
            options=dropdown_labels,
            value=None,
            className='dropdown'
        )),
    html.Button('Submit', id='button'),
    html.Div(children=html.Label(["Python code: ", html.A('https://github.com/mallory-archer/cocktail_party/',
                                                          href='https://github.com/mallory-archer/cocktail_party/',
                                                          style={'color': '#ad1457'})],
                                 style={'color': '#E9DDE1'}))
])


# Step 5. Add callback functions
@app.callback(Output('plot', 'figure'),
              [Input('button', 'n_clicks')],
              [State('input-box', 'value'), State('input-box-friend', 'value'), State('relationship', 'value'), State('plot', 'figure')]
              )    # Output('output-container-button', 'children')  [Input('button', 'n_clicks'), ,
def update_figure(n_clicks, value, value_friend, value_relationship, fig_updated):
    if value and value_friend:
        G.add_nodes_from([value.title()])
        G.add_edge(value.title(), value_friend.title(), label=value_relationship)
        data_temp, layout_temp = create_fig_data(G)
        fig_updated = go.Figure(data=data_temp, layout=layout_temp)
    return fig_updated


# Step 6. Add the server clause
application = app.server

if __name__ == '__main__':
    # app.run_server(debug=True)
    application.run(debug=True, port=8080)  # Beanstalk expects it to be running on 8080.
