from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import dash_table
from math import ceil

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_excel('2019-2020_NBA_player_regular.xlsx', engine='openpyxl', header=1)

team = df['TEAM'].unique()
columns = df.columns
PAGE_SIZE = ceil(len(df)/10)

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value=''
            )],
        style={'width': '48%', 'display': 'inline-block'}),

	dcc.Graph(id='graph'),

	dash_table.DataTable(
	   	id='datatable-paging',
	    columns=[
	        {'id': c, 'name': c} for c in df.columns
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
	Input('url', 'pathname')
	)
def update_graph(page_current, page_size,yaxis_column_name, pathname):

	dff=df.loc[df['TEAM']==pathname.split('/')[1]]
	players = dff['FULL NAME']

	fig = make_subplots(rows=2, cols=2, specs=[[{}, {"type": "domain"}],
			[{"colspan": 2}, None]],
			subplot_titles=("Usage rate","Full Stats", "{}".format(yaxis_column_name)))

	pie = go.Pie(labels=dff['FULL NAME'],
		values=dff['USG%Usage RateUsage rate, a.k.a., usage percentage is an estimate of the percentage of team plays used by a player while he was on the floor'])

	bar = go.Bar(x=players, y=dff['PPGPointsPoints per game.'])

	if yaxis_column_name is '':
		raise PreventUpdate
	else:
		line = go.Scatter(x=players, y=dff['{}'.format(yaxis_column_name)])
		
	fig.add_trace(bar, row=1, col=1)
	fig.add_trace(pie, row=1, col=2)
	fig.add_trace(line, row=2, col=1)
	fig.update_layout(height=1000)

	figure=fig
	return fig, dff.iloc[
	page_current*page_size:(page_current+ 1)*page_size
	].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)