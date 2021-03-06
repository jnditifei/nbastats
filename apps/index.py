import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app import app

teamPlayoffs =pd.read_csv('2019-2020_NBA_team_playoffs.csv')

maps= go.Figure()

access = ("pk.eyJ1Ijoiam5kaXRpZmVpIiwiYSI6ImNrbHVwN2o4NDA5NmgybnBsNzI3Z3c1dWYifQ.971IMEJSB-BBVl575_HH3w")

maps.add_trace(go.Scattermapbox(
        lat=teamPlayoffs['lat'],
        lon=teamPlayoffs['lon'],
        mode='markers',
        hovertext=teamPlayoffs['short'],
        hoverinfo="text",
        marker=go.scattermapbox.Marker(
            size=20,
            color='rgb(138, 11, 11)',
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
    mapbox_style="dark"
)

maps.update_layout()

layout = html.Div([
    html.Div([dcc.Graph(id='map',figure=maps)
        ]),
])
