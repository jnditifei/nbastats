import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

from app import app
from .layouts import graph, table, content, sidebar

playoffStats = pd.read_excel('2019-2020_NBA_player_playoffs.xlsx', engine='openpyxl')
team = playoffStats['TEAM'].unique()
columns = playoffStats.columns

_graph = graph()
_table = table(columns)
_content = content()
_sidebar= sidebar(columns)

layout = html.Div([
    _sidebar,
    _content
    ])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'graph':
        return _graph
    elif tab == 'table':
        return _table

@app.callback(Output('select-team', 'options'),
    Output('select-team', 'value'),
    Input('url', 'pathname')
    )
def populatedropdown(pathname):
    return [{'label': i, 'value': i} for i in team], pathname.split('/')[1]

@app.callback(Output('graph', 'figure'),
    Input('yaxis-column', 'value'),
    Input('select-team', 'value'),
    )
def update_graph(yaxis_column_name, select_team):

    dff=playoffStats.loc[playoffStats['TEAM']==select_team]
    players = dff['FULL NAME']

    fig = make_subplots(rows=2, cols=2, specs=[[{"colspan": 2}, None],
        [{}, {"type": "domain"}]],
            subplot_titles=("{}".format(yaxis_column_name), "Full State", "Usage rate" ))

    pie = go.Pie(labels=dff['FULL NAME'],
        values=dff['USG%'])

    bar = go.Bar(x=players, y=dff['PPG'])

 
    line = go.Scatter(x=players, y=dff['{}'.format(yaxis_column_name)])
    """
       if yaxis_column_name is '':
        raise PreventUpdate
    else:
        """
        
    fig.add_trace(bar, row=2, col=1)
    fig.add_trace(pie, row=2, col=2)
    fig.add_trace(line, row=1, col=1)
    fig.update_layout(height=1000, showlegend = False)

    figure=fig
    return fig

@app.callback(
    Output('datatable-paging', 'data'),
    Input('select-team', 'value'),
    Input('datatable-paging', "page_current"),
    Input('datatable-paging', "page_size")
    )
def upgrate_table(select_team, page_current, page_size):
    dff=playoffStats.loc[playoffStats['TEAM']==select_team]
    return dff.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')