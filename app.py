from dash import Dash, html
from map import configure_callbacks, create_map_timeline
from concert import configure_callbacks, create_dropdown

app = Dash('Eventful')

app.layout = html.Div(
    [
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

    html.Div(id = 'map'),

    create_map_timeline(),

        create_dropdown(),

        html.Div(id='concert-info')

    ],

    style =
    {
        'backgroundColor': '#F0F0F0',
        'margin': '10%',
        'fontFamily': 'Jomhuria-Regular'
    }
)

configure_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
