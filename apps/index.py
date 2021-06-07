import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app import app
from apps.utils import create_card

teamsStats =pd.read_csv('2019-2020_NBA_team_playoffs.csv')
playersStats = pd.read_excel('2019-2020_NBA_player_playoffs.xlsx', engine='openpyxl')

short = teamsStats['short'].unique()

years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2018,2019,2020]


maps= go.Figure()

access = ("pk.eyJ1Ijoiam5kaXRpZmVpIiwiYSI6ImNrbHVwN2o4NDA5NmgybnBsNzI3Z3c1dWYifQ.971IMEJSB-BBVl575_HH3w")

maps.add_trace(go.Scattermapbox(
        lat=teamsStats['lat'],
        lon=teamsStats['lon'],
        mode='markers',
        hovertext=teamsStats['short'],
        hoverinfo="text",
        marker=go.scattermapbox.Marker(
            size=20,
            color='#e83e8c',
            opacity=0.7
        )
    ))

maps.update_layout(
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=access,
        bearing=0,
        center=dict(
            lat=38,
            lon=-94
        ),
        pitch=0,
        zoom=3,
        style='light'
    ),
    mapbox_style="light", margin = dict(l = 0, r = 0, t = 0, b = 0,)
    )

first_row = dbc.Row([
    dbc.Col([
        html.Div(dcc.Dropdown(style={'width': '48%'}),
            className='w-35 p-3 h-25'
            ),
        html.Div(
            dcc.RadioItems(options=[{'value':'regular', 'label': 'Regular'}, {'value':'playoffs', 'label':'Playoffs'}],
                className='w-35 p-3 h-25'
                )
            ),
        html.Div(
                dcc.Slider(
                    id='slider-season',
                    min=years[0],
                    max=years[-1],
                    value=years[-1],
                    marks={str(year): str(year) for year in years},
                    #marks = {"2010":"2010/2011", "2011":"2011/2012", "2012":"2012/2013", "2013":"2013/2014", "2014":"2014/2015", "2015":"2015/2016", "2016":"2016/2017","2017":"2017/2018", "2018":"2018/2019", "2019":"2019/2020"},
                    step=None
                    ),
                className='w-35 p-3 h-25'
    )],
    align='center',
    className='shadow p-3 mb-5 bg-white rounded',
    width=4),

    dbc.Col(
        dbc.CardDeck([
            create_card("League Champion", "Los Angeles Lakers"),
            create_card("Finals MVP", "Lebron James"), 
            create_card("Playoffs Leader PTS", "Anthony Davis (582)"),
            create_card("Playoffs Leader TRB", "Lebron James (184)"),
            create_card("Playoffs Leader WS", "Anthony Davis (4.5)"),
                     ],
                     className='w-100',
                     style={'margin-left':'2px'}),
        width=8,
        )],
    style={"margin-bottom":"5px", "margin-top":"5px"})

second_row = dbc.Row(
    dbc.Col(
    dbc.CardDeck([
        dbc.Card(
                dcc.Graph(id='map',figure=maps, hoverData={'points': [{'hovertext': 'Lal'}]}
                    ), className="shadow p-3 mb-5 bg-white rounded",
            ),
        dbc.Card(
            dash_table.DataTable(
            id='DataTable-result',
            data=teamsStats.round(decimals=3).to_dict('records'),
            columns=[
            {'id': c, 'name': c} for c in teamsStats.columns[:24]
            ],
            style_as_list_view=True,
            style_table={'overflowX': 'auto'},
            ), className="shadow p-3 mb-5 bg-white rounded"
            )
        
    ])
    ),
    align="center",
    justify="center")
third_row = dbc.Row([
    dbc.Col(width=4),
    dbc.Col(
            dbc.Card(dcc.Graph(id="players-graph", figure=go.Figure(
                go.Scatter(y=playersStats["MPG"], x=playersStats["GP"], 
                    mode='markers',
                    marker_size=playersStats["PPG"],
                    text=playersStats["FULL NAME"],
                    marker_color=playersStats['FULL NAME'].index.tolist(),
                    hovertemplate = "%{text}: <br>Game Played: %{x} </br>Minute Per Game: %{y} </br>Point Per Game: %{marker.size}"
                    )
                )
                ), className="shadow p-3 mb-5 bg-white rounded"),
            width=8
            )]
    )

layout = dbc.Container([
    first_row,
    second_row,
    third_row],
    fluid=True
)


    
