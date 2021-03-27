import dash_html_components as html
import dash_bootstrap_components as dbc

def create_card(title, content):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, className="card-title"),
                html.Br(),
                html.Br(),
                html.H2(content, className="card-subtitle"),
                html.Br(),
                html.Br(),
                ]
        ),
        className='shadow p-3 mb-5 bg-white rounded',
        style={"text-align": "center"}
    )
    return(card)