from dash import Dash, html, dcc
from map import configure_callbacks_map, create_map_timeline
from concert import configure_callbacks
from top_artists import configure_callbacks_display_results, configure_callbacks_update_results, artists_info

# Font icons and CSS
external_stylesheets = ['./assets/app.css', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css']

# We create the app
app = Dash('Eventful', external_stylesheets=external_stylesheets, suppress_callback_exceptions = True)


app.layout = html.Div(
    [
        html.H1('EVENTFUL', id='titulo'), #Page title

        # Navigation bar
        html.Div( className='Intro',
            children =
            [
                html.Div([html.A("Artists", href="artists-title")], style={'scroll-behaviour': 'smooth'}),
                html.Div([html.A("Concerts", href="#concerts")])
            ]
        ), # Navigation bar

    html.Div([dcc.Graph(id='map')]),

    create_map_timeline(),

        html.Div(id='concert-info'),
        artists_info
    ],

    style =
    {
        'backgroundColor': '#F0F0F0',
        'margin': '10%',
        'fontFamily': 'Jomhuria-Regular'
    }
)

configure_callbacks(app)
configure_callbacks_map(app)
configure_callbacks_update_results(app)
configure_callbacks_display_results(app)

if __name__ == '__main__':
    app.run(debug=True)
