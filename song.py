from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import dash
from dash import Dash, html, dcc
from collections import Counter
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import random

df = pd.read_json('data.json')

def wordCloud(song, clickData):
    df = pd.read_json('data.json')
    if not clickData:
       return error_figure()
    else:
        artist = clickData["points"][0]["text"]
        if song == 'Nothing' or song == None:
            song = songs_of_artist(artist)[0]
    song_words = df.loc["Spotify tracks", str(artist)][song]["words"]
    if len(song_words) == 0:
        return error_figure()  # Devolver la figura de error en un formato adecuado

    sorted_words = sorted(song_words.items(), key = lambda x:x[1], reverse = True)
    top_10 = dict(sorted_words[:10])

    top_10 = {k: v * 10 for k, v in top_10.items()}

    colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]
    data = go.Scatter(x=[random.random() for i in range(10)],
                 y=[random.random() for i in range(10)],
                 mode='text',
                 text=list(top_10.keys()),
                 marker={'opacity': 0.3},
                 textfont={'size': list(top_10.values()),
                           'color': colors}
                #            ,
                #  hovertext=[str(top_10.keys()), list(top_10.values())]
                )
    return data

def error_figure():
    error_figure = go.Scatter(x=[5],
                 y=[5],
                 mode='text',
                 text=['No data available for selected song'],
                 marker={'opacity': 0.3},
                 textfont={'size': 60}
                )

    return error_figure  # Devolver la figura de error en un formato adecuado

def songs_of_artist(name):
    if name == None:
        name = 'Taylor Swift'        
    tracks = df.loc["Spotify tracks", name]
    song_list = []
    for song in tracks:
        song_list.append(song)
    return song_list

@dash.callback(
    [dash.dependencies.Output('wordcloud-div', 'children'), 
     dash.dependencies.Output('album-name', 'children'),
     dash.dependencies.Output('album-photo', 'src'),
     dash.dependencies.Output('song-link', 'href'),
     dash.dependencies.Output('setlist-div', 'children')],
    [dash.dependencies.Input('song_dropdown', 'value'),
     Input(component_id='map', component_property='clickData')]  # Aquí define tu activador (Input) adecuado
)
def updatecallback(value, clickData):
    return update_wordcloud(value, clickData), showalbumname(value, clickData), showalbumcover(value, clickData),\
    createlink(value, clickData), setlistGraph(value, clickData)

def update_wordcloud(song, clickData):  # El valor del activador dependerá de tu caso específico
    # Llama a la función wordCloud con los parámetros adecuados
    # Supongamos que aquí defines el artista y la canción seleccionados
    
    wordcloud_figure = wordCloud(song, clickData)

    #  layout = go.Layout(yaxis=dict(range=[0, 2]),xaxis=dict(range=[0, 2]))
    
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                    'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
                    
    fig = go.Figure(data=[wordcloud_figure], layout=layout)

    return dcc.Graph(figure=fig)

def showalbumname(song, clickData):
    if not clickData:
        return None
    artist = clickData["points"][0]["text"]
    if song == 'Nothing' or song == None:
        song = songs_of_artist(artist)[0]
    album = df.loc["Spotify tracks", artist][song]["album_name"]
    return album

def showalbumcover(song, clickData):
    if not clickData:
        return None
    artist = clickData["points"][0]["text"]
    if song == 'Nothing' or song == None:
        song = songs_of_artist(artist)[0]
    cover = df.loc["Spotify tracks", artist][song]["album_photo"]
    return cover

def createlink(song, clickData):
    if not clickData:
        return None
    artist = clickData["points"][0]["text"]
    if song == 'Nothing' or song == None:
        song = songs_of_artist(artist)[0]
    url = df.loc["Spotify tracks", artist][song]["url"]
    return url

def setlistGraph(song,clickData):
    if not clickData:
        return None
    artist = clickData["points"][0]["text"]
    if song == 'Nothing' or song == None:
        song = songs_of_artist(artist)[0]
    setlist_tracks = df.loc["Setlist tracks", artist]

    songs = setlist_tracks.keys()
    values = setlist_tracks.values()
    colors = ['green' if s == song else 'blue' for s in songs]

    fig = go.Figure(data=[go.Bar(x=list(range(1, len(setlist_tracks)+1)), y=list(values), 
                                 hovertext=list(songs), marker=dict(color=colors))])
    
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
    app.callback(
        Output(component_id='song-info', component_property='children'),
        Input(component_id='map', component_property='clickData')
    )(update_song_info)

    return

def checkOptions(clickData):
    if not clickData:
        return [{'label': 'no data', 'value': 'no data'}]
    else:
        return [{'label': song, 'value': song} for song in songs_of_artist(clickData["points"][0]["text"])]

def checkValue(clickData):
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
            value= checkValue(clickData) # Valor predeterminado para el drop-down
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