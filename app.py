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
                        html.A("GO TO CONCERTS", href="#map-title", className='Scroll')])
            ], 
            className='Intro'
        ), # Navigation bar

        html.Div([html.P('Eventful is an interactive webpage which allows you to look for concerts by your favorite artists! Select a concert in the map to visualize it, and obtain additional information about the artist and his/her songs. Click on "Go to concerts" to move to the map. Click on "Go to artists" to move to the visualization of the most popular artists of the moment.', 
                     style={'display': 'inline-block', 'padding-left': '20px'}, id='main-explanation')]),

        html.Div([html.H2("CONCERT MAP", id='map-title', style={'display': 'inline-block'}), 
                html.P('Click on a concert in the map to display its information. You can filter the available concerts by date using the timeline. To see all concerts in a single venue, please zoom in on its location; otherwise you will only see one of the concerts', 
                        style={'display': 'inline-block', 'padding-left': '20px'}, id='map-explanation'),
                dcc.Graph(id='map',style={'width': '100%', 'height': '90vh'})]),

        create_map_timeline(),

            html.Div(id='concert-info'),
            html.Div(id='song-info'),
            artists_info,
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
