from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import dash
from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objects as go
import plotly
import plotly.graph_objs as go
import random

# Read the data json
df = pd.read_json('data.json')

def wordCloud(song, clickData):
    """Create a wordcloud based on the input song"""
    df = pd.read_json('data.json')
    if not clickData:
       # Check if user has clicked an artist
       return error_figure()
    else:
        artist = clickData["points"][0]["text"]
        if song == 'Nothing' or song == None: # Check if a user has selected song
            # If not, default to their first song
            song = songs_of_artist(artist)[0]
    # Extract the most sang words for the wordcloud
    song_words = df.loc["Spotify tracks", str(artist)][song]["words"]
    if len(song_words) == 0:
        return error_figure()  # Return error figure in case of no data

    # Sort words dscending order
    sorted_words = sorted(song_words.items(), key = lambda x:x[1], reverse = True)
    # Grab the top 10 songs
    top_10 = dict(sorted_words[:10])
    # Multiply by 10 to increase the word size
    top_10 = {k: v * 10 for k, v in top_10.items()}
    # Create random colors for th words
    colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]
    # Create the wordcloud as a scatter plot
    data = go.Scatter(x=[random.random() for i in range(10)],
                 y=[random.random() for i in range(10)],
                 mode='text',
                 text=list(top_10.keys()),
                 marker={'opacity': 0.3},
                 textfont={'size': list(top_10.values()),
                           'color': colors}
                )
    return data

def error_figure():
    # Error figure in case there is no word data
    error_figure = go.Scatter(x=[5],
                 y=[5],
                 mode='text',
                 text=['No data available for selected song'],
                 marker={'opacity': 0.3},
                 textfont={'size': 60}
                )

    return error_figure

def songs_of_artist(name):
    """Function to return all songs of an artist in the dataset"""
    if name == None:
        name = 'Taylor Swift'    
    # Locate the tracks    
    tracks = df.loc["Spotify tracks", name]
    song_list = []
    # Create a list with all the tracks
    for song in tracks:
        song_list.append(song)
    return song_list

# Different callbacks for different parts of the app
@dash.callback(
    [dash.dependencies.Output('wordcloud-div', 'children'), # To reflect changes in the song selected for the word cloud
     dash.dependencies.Output('album-name', 'children'), # To change the current album name of the selected song
     dash.dependencies.Output('album-photo', 'src'), # To change the album picture of the current song
     dash.dependencies.Output('song-link', 'href'), # To add the proper spotify link of the song
     dash.dependencies.Output('setlist-div', 'children')], # To add the proper graph for most played songs
    [dash.dependencies.Input('song_dropdown', 'value'), # The input is the dropdown menu AND
     Input(component_id='map', component_property='clickData')] # Also the selected concert in the map
)
def updatecallback(value, clickData):
    """Function to update the web depending of the inputs described above"""
    return update_wordcloud(value, clickData), showalbumname(value, clickData), showalbumcover(value, clickData),\
    createlink(value, clickData), setlistGraph(value, clickData)

def update_wordcloud(song, clickData):  
    """Function to update the wordcloud based on a specific song"""
    wordcloud_figure = wordCloud(song, clickData)
    # The layout is of no use
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                    'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
    # Create the figure and return it
    fig = go.Figure(data=[wordcloud_figure], layout=layout)
    return dcc.Graph(figure=fig)

def showalbumname(song, clickData):
    """Function to obtain the name of an album from the dataset"""
    if not clickData:
        return None
    artist = clickData["points"][0]["text"]
    # Error handling
    if song == 'Nothing' or song == None:
        song = songs_of_artist(artist)[0]
    # Locate and return
    album = df.loc["Spotify tracks", artist][song]["album_name"]
    return album

def showalbumcover(song, clickData):
    """Function to obtain the cover of an album from the dataset"""
    if not clickData:
        return None
    artist = clickData["points"][0]["text"]
    # Error handling
    if song == 'Nothing' or song == None:
        song = songs_of_artist(artist)[0]
    # Locate and return
    cover = df.loc["Spotify tracks", artist][song]["album_photo"]
    return cover

def createlink(song, clickData):
    """Function to obtain the url of a song from the dataset"""
    if not clickData:
        return None
    artist = clickData["points"][0]["text"]
    # Error handling
    if song == 'Nothing' or song == None:
        song = songs_of_artist(artist)[0]
    # Locate and return
    url = df.loc["Spotify tracks", artist][song]["url"]
    return url

def setlistGraph(song,clickData):
    if not clickData:
        return None
    artist = clickData["points"][0]["text"]
    # Error handling
    if song == 'Nothing' or song == None:
        song = songs_of_artist(artist)[0]
    # Locate most played tracks
    setlist_tracks = df.loc["Setlist tracks", artist]
    # Obtain the songs and times played
    songs = setlist_tracks.keys()
    values = setlist_tracks.values()
    # If the selected song is in the most played songs, highlight it in green
    colors = ['green' if s == song else 'blue' for s in songs]
    # Create the bar graph
    fig = go.Figure(data=[go.Bar(x=list(range(1, len(setlist_tracks)+1)), y=list(values), 
                                 hovertext=list(songs), marker=dict(color=colors))])
    # When hovering show the name of the song
    fig.update_layout(hovermode="x",
    xaxis_title='Song',
    yaxis_title='Times Played')
    
    return dcc.Graph(figure=fig)

def configure_callbacks_songs(app: Dash) -> None:
    """
    Configures the callbacks for the app.
    This is a workaround for circular imports.
    :param app: The Dash app.
    """
    # This function recieves the concert selected on the map as an input
    app.callback(
        Output(component_id='song-info', component_property='children'),
        Input(component_id='map', component_property='clickData')
    )(update_song_info)

    return

def checkOptions(clickData):
    """Function to show the available songs in the dropdown"""
    if not clickData:
        return [{'label': 'no data', 'value': 'no data'}]
    else:
        return [{'label': song, 'value': song} for song in songs_of_artist(clickData["points"][0]["text"])]

def checkValue(clickData):
    """Function to show the selected song in the dropdown"""
    if not clickData:
        return "Nothing"
    else:
        songs_of_artist(clickData["points"][0]["text"])[0]

def update_song_info(clickData):
    return html.Div(
    [
        html.H2(children='Songs', style={'textAlign':'left'}),
        dcc.Dropdown(
            id='song_dropdown',
            options=checkOptions(clickData),
            value= checkValue(clickData)
        ),

        html.Div([
            html.P('Album: ',id='album-cover-text', style={'font-size': 24}),
            html.P(id='album-name', style={'font-size': 24}),
            html.A(html.Img(id='album-photo', style={'height':'7vw', 'width':'7vw', 'cursor': 'pointer'}),
                   id='song-link', href='', target='_blank')
        ],id="album-div"),

        html.Div(id="wordcloud-div"),

        html.Div([
            html.P('Most played songs in recent concerts: ', style={'font-size': 18}),
            html.Div(id="setlist-div")
        ])
    ]
)