from dash import Dash, html, dcc
from map import configure_callbacks_map, create_map_timeline
from concert import configure_callbacks
from top_artists import configure_callbacks_display_results, configure_callbacks_update_results, artists_info
from song import configure_callbacks_songs
# Font icons and CSS
external_stylesheets = ['./assets/app.css', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css']

# We create the app
app = Dash('Eventful', external_stylesheets=external_stylesheets, suppress_callback_exceptions = True)


app.layout = html.Div(
    [
        html.Div(['EVENTFUL', 
                  html.Img(src=app.get_asset_url('logo.svg'), 
                           alt='Logo', 
                           style={'width': 'auto', 'height': '125px'})], id='titulo'),  # Page title

        # Navigation bar
        html.Div(
            children =
            [
                html.Div([html.A("GO TO ARTISTS", href="#artists-title", className='Scroll', style={'margin-right': '10px'}),
                        html.A("GO TO CONCERTS", href="#concert-info", className='Scroll')])
            ], 
            className='Intro'
        ), # Navigation bar

    html.Div([dcc.Graph(id='map',style={'width': '100%', 'height': '90vh'})]),

    create_map_timeline(),

        html.Div(id='concert-info'),
        artists_info,
        html.Div(id='song-info')
    ],

    style =
    {
        'backgroundColor': '#19323C',
        'margin': '7%',
        'fontFamily': 'Jomhuria-Regular'
    }
)

configure_callbacks(app)
configure_callbacks_map(app)
configure_callbacks_update_results(app)
configure_callbacks_display_results(app)
configure_callbacks_songs(app)
if __name__ == '__main__':
    app.run(debug=True)
