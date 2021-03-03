import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

teamPlayoffs =pd.read_csv('2019-2020_NBA_team_playoffs.csv')

nbamap = px.scatter_mapbox(teamPlayoffs, lat="lat", lon="lon", hover_name="Team", hover_data=["Rk", "G"],
                        color="Team", zoom=3, size_max=30)
nbamap.update_layout(mapbox_style="open-street-map")
nbamap.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
nbamap.update_layout(title='NBA Playoffs 2019/2020')

layout = html.Div([
    html.Div([dcc.Graph(figure=nbamap)
        ]),
])