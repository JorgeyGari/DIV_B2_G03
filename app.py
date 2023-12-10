from dash import Dash, html, dcc
from map import configure_callbacks_map, create_map_timeline
from concert import configure_callbacks

app = Dash(__name__, suppress_callback_exceptions = True)

app.layout = html.Div([
    html.H1  # Page title
    (
        'EVENTFUL'
    ),
    
    html.Div  # Navigation bar
    ( 
        children =
        [
            html.Div([html.A("Artists", href="#artists")]),
            html.Div([html.A("Concerts", href="#concerts")])
        ]
    ),

    html.Div([dcc.Graph(id='map')]),

    create_map_timeline(),

    # create_dropdown(),

    html.Div(id='concert-info')

])

configure_callbacks(app)
configure_callbacks_map(app)

if __name__ == '__main__':
    app.run(debug=True)