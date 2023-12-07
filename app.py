from dash import Dash, html
from map import map_timeline
from concert import configure_callbacks, create_dropdown

app = Dash(__name__)

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

    map_timeline,

    create_dropdown(),

    html.Div(id='concert-info')

])

configure_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)