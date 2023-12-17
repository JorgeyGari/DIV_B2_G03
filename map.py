# Referencias

# Para el date selector he usado la primera, pero podríamos explorar la segunda
# https://dash.plotly.com/dash-core-components/rangeslider
# https://plotly.com/python/range-slider/

# Para el mapa he usado la primera, y también se podría explorar la segunda. Y si nos apetece motivarnos, podemos considerar la tercera
# https://plotly.com/python/scattermapbox/
# https://plotly.com/python/scatter-plots-on-maps/
# https://dash.plotly.com/dash-core-components/geolocation

# Expansión de la Timeline: Añadir una graduación más fina

# Expansión del Mapa: Crear markers personalizados, asociar a un color por artista

# He tenido que borrar manualmente a Kanye West, a SZA y a Lana del Rey. Podemos considerar volver a añadirlos

from dash import Dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go

df = pd.read_json('data.json')

mapbox_access_token = "pk.eyJ1IjoicGFibG9zYXZpbmEiLCJhIjoiY2xwbXVreXo4MGN5bTJscXk3YjJwY291ciJ9.Kyrlg9CR1Rdo7wAzD3IAVQ"

# Function to transform a date from the format in the json file (yyyy/mm/dd) to a number
def date2num(date):
    broken = date.split("-")
    numeric = int(broken[0]) * 10000 + int(broken[1]) * 100 + int(broken[2])
    return numeric

# Function to transform a month into a number. Note how we only consider concerts in 2024
def month2num(date):
    numeric = 2024 * 10000 + date * 100
    return numeric

# Function to create the map depending on the data coming from the timeline
def update_map_info(selection):
    # Initial and final month, coming from the timeline
    initial = selection[0]
    final = selection[1]

    # Lists used to then create markers in the map
    latitudes = []
    longitudes = []
    artists = []

    # We access all of the available concerts, and check if their date is the interval selected in the timeline
    # If it is, we store its latitude, longitude, and artist+date
    for artist in df.loc["Concerts"].index:
        for concert in df.loc["Concerts"][artist]:
            if date2num(concert["Date"]) > month2num(initial) and date2num(concert["Date"]) < month2num(final):
                latitude = concert["Latitude"]
                longitude = concert["Longitude"]

                # If there are multiple concerts in the same location, we place them in slightly different locations
                while latitude in latitudes: 
                    latitude = str(float(latitude) + 0.005)
                    longitude = str(float(longitude) + 0.005)
                
                latitudes.append(latitude)
                longitudes.append(longitude)
                artists.append(artist + "*" + concert["Date"])
    
    # We create a map, feeding it the data gathered. We also specify the marker style
    map = go.Figure()
    map.add_trace(go.Scattermapbox(
            mode='markers',
            lat = latitudes,
            lon = longitudes,
            marker = {"size" : 12, "symbol" : ["marker"] * len(latitudes), "color" : "rgb(255, 150, 102)"},
            text=artists,
            hoverinfo='text',
    ))
    # We set some additional visualization properties for the map
    map.update_layout(
        autosize=True,
        hovermode='closest',
        paper_bgcolor = '#19323C',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=39.833333,
                lon=-98.583333
            ),
            pitch=0,
            zoom=2,
            style = "dark",
        ),
    )

    return map

# Function to create the timeline
def create_map_timeline() -> html.Div:
    return html.Div(
        [
            # The range slider is created with the months of the year
            dcc.RangeSlider
            (
                min=1,
                max=12,
                step=None,
                marks = { 
                    1: {'label': "January", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    2: {'label': "February", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    3: {'label': "March", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    4: {'label': "April", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    5: {'label': "May", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    6: {'label': "June", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    7: {'label': "July", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    8: {'label': "August", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    9: {'label': "September", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    10: {'label': "October", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    11: {'label': "November", 'style': {'fontSize': '30px', 'color': '#FF9666'}},
                    12: {'label': "December", 'style': {'fontSize': '30px', 'color': '#FF9666'}}
                }, 
                value=[1, 12], 
                allowCross = False,
                id="date-selector"
            )
        ],
        id= 'date-slider'
    )

def configure_callbacks_map(app) -> None:
    """
    Configures the callbacks for the app.
    This is a workaround for circular imports.
    :param app: The Dash app.
    """
    app.callback(
        Output(component_id='map', component_property='figure'),
        Input(component_id='date-selector', component_property='value')
    )(update_map_info)
