import dash_core_components as dcc
import dash_html_components as html
import dash_table

def graph():
    graph = html.Div([
        dcc.Graph(id='graph')
        ])
    return graph

def table(columns):
    PAGE_SIZE = 10
    table = html.Div([
        dash_table.DataTable(
            id='datatable-paging',
            columns=[
                {'id': c, 'name': c} for c in columns
            ],
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom'
        )
        ])
    return table

def content():
    CONTENT_STYLE = {
    'margin-left': '20%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
    }

    content = html.Div([
    dcc.Tabs(id="tabs", value='graph', children=[
        dcc.Tab(label='Graph', value='graph'),
        dcc.Tab(label='Table', value='table'),
    ]),
    html.Div(id='tabs-content')
    ],
    style=CONTENT_STYLE
    )
    return content

def sidebar(team, columns):
    SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
    }

    TEXT_STYLE = {
        'textAlign': 'center',
        'color': '#191970'
    }
    sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        html.P("Select Team"),
        html.Div([dcc.Dropdown(
                id='select-team',
                options=[{'label': i, 'value': i} for i in team],
                value='Okc',
            )],
        style={'width': '90%', 'display': 'inline-block'}),
        html.P("X-axis Line"),
        html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in columns],
                    value='PPGPointsPoints per game.'
                )],
                style={'width': '90%', 'display': 'inline-block'}),
    ],
    style=SIDEBAR_STYLE,
    )

    return sidebar
