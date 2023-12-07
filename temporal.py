from dash import Dash, html
from map import map_timeline
from concert import concert_info

app = Dash(__name__)

# Referencias

# Para el date selector he usado la primera, pero podríamos explorar la segunda
# https://dash.plotly.com/dash-core-components/rangeslider
# https://plotly.com/python/range-slider/

# Para el mapa he usado la primera, y también se podría explorar la segunda. Y si nos apetece motivarnos, podemos considerar la tercera
# https://plotly.com/python/scattermapbox/
# https://plotly.com/python/scatter-plots-on-maps/
# https://dash.plotly.com/dash-core-components/geolocation

# Expansión del Mapa: Añadir clusters, crear markers personalizados, asociar a un color por artista

# He tenido que borrar manualmente a Kanye West, a SZA y a Lana del Rey. Podemos considerar volver a añadirlos

from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go

df = pd.read_json('data.json')

app = Dash(__name__)

mapbox_access_token = "pk.eyJ1IjoicGFibG9zYXZpbmEiLCJhIjoiY2xwbXVreXo4MGN5bTJscXk3YjJwY291ciJ9.Kyrlg9CR1Rdo7wAzD3IAVQ"

map = go.Figure(id='map')

"""
map = go.Figure(go.Scattermapbox(
        lat = latitudes,
        lon = longitudes,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color="rgb(255,0,0)"
        ),
        text=artists,
    ))
"""

map.update_layout(
    # title="Concerts",
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=39.833333,
            lon=-98.583333
        ),
        pitch=0,
        zoom=2,
        # options for style --> basic, streets, outdoors, light, dark, satellite, satellite-streets
        style = "outdoors"
    ),
)

"""
@callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def map2concert():
    pass
"""
    
@callback(
    Output(component_id='map', component_property='figure'),
    Input(component_id='date-selector', component_property='value')
)
def date2map(selected_months):
    initial = selected_months[0]
    final = selected_months[1]

    latitudes = []
    longitudes = []
    artists = []

    for artist in df.loc["Concerts"].index:
        for concert in df.loc["Concerts"][artist]:
            # if concert in date:
            latitude = concert["Latitude"]
            longitude = concert["Longitude"]

            while latitude in latitudes: 
                latitude = str(float(latitude) + 0.005)
                longitude = str(float(longitude) + 0.005)
            
            latitudes.append(latitude)
            longitudes.append(longitude)
            artists.append(artist)