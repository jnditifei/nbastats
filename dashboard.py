from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import dash_table
import plotly.express as px

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, suppress_callback_exceptions=True)

teamPlayoffs =pd.read_csv('2019-2020_NBA_team_playoffs.csv')
playoffStats = pd.read_excel('2019-2020_NBA_player_playoffs.xlsx', engine='openpyxl')
regularseason = pd.read_excel('2019-2020_NBA_player_regular.xlsx', engine='openpyxl', header=1)

team = playoffStats['TEAM'].unique()
columns = playoffStats.columns
PAGE_SIZE = 10

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

nbamap = px.scatter_mapbox(teamPlayoffs, lat="lat", lon="lon", hover_name="Team", hover_data=["Rk", "G"],
                        color="Team", zoom=3, size_max=30)
nbamap.update_layout(mapbox_style="open-street-map")
nbamap.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
nbamap.update_layout(title='NBA Playoffs 2019/2020')

index_page = html.Div([
    html.Div([dcc.Graph(figure=nbamap)
        ]),
    html.Div([dcc.Link('Full stats by team', href='/team-details')
        ])
])

page_1_layout = html.Div([
    html.Div([
        dcc.Link('Home', href='/')
        ]),
    html.Br(),
    html.Div([
        dcc.Dropdown(
                id='select-team',
                options=[{'label': i, 'value': i} for i in team],
                value='Okc',
            )],
            style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value='PPGPointsPoints per game.'
            )],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            

    dcc.Graph(id='graph'),

    dash_table.DataTable(
        id='datatable-paging',
        columns=[
            {'id': c, 'name': c} for c in playoffStats.columns
        ],
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom'
    )
    ])

@app.callback(Output('graph', 'figure'),
    Output('datatable-paging', 'data'),
    Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size"),
    Input('yaxis-column', 'value'),
    Input('select-team', 'value')
    )
def update_graph(page_current, page_size,yaxis_column_name, select_team):

    dff=playoffStats.loc[playoffStats['TEAM']==select_team]
    players = dff['FULL NAME']

    fig = make_subplots(rows=2, cols=2, specs=[[{"colspan": 2}, None],
        [{}, {"type": "domain"}]],
            subplot_titles=("Usage rate","Full Stats", "{}".format(yaxis_column_name)))

    pie = go.Pie(labels=dff['FULL NAME'],
        values=dff['USG%Usage RateUsage rate, a.k.a., usage percentage is an estimate of the percentage of team plays used by a player while he was on the floor'])

    bar = go.Bar(x=players, y=dff['PPGPointsPoints per game.'])

    if yaxis_column_name is '':
        raise PreventUpdate
    else:
        line = go.Scatter(x=players, y=dff['{}'.format(yaxis_column_name)])
        
    fig.add_trace(bar, row=2, col=1)
    fig.add_trace(pie, row=2, col=2)
    fig.add_trace(line, row=1, col=1)
    fig.update_layout(height=1000, showlegend = False)

    figure=fig
    return fig, dff.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')

# Update the index
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return index_page
    elif pathname == '/team-details':
        return page_1_layout
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)