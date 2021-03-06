import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from app import server
from apps import index, playoffs

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.

app.layout = html.Div([
    html.Nav(className = "nav nav-pills", children=[
        html.A('Home', className="nav-item nav-link btn", href='/'),
        html.A('Player Stats', className="nav-item nav-link active btn", href='/playoffs')
        ]),
    dcc.Location(id='url', refresh=False),
    html.Br(),
    html.Div(id='page-content')
])

@app.callback(
    Output('url', 'pathname'),
    [Input('map', 'clickData')]
)
def change_url(clickData):
    if clickData:
        return '/' + str(clickData['points'][0]['hovertext'])

# Update the index
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == pathname:
        return playoffs.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)