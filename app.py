from dash import Dash
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.MINTY]
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server