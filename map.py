# Referencias

# Para el date selector he usado la primera, pero podríamos explorar la segunda
# https://dash.plotly.com/dash-core-components/rangeslider
# https://plotly.com/python/range-slider/

# Para el mapa he usado la primera, y también se podría explorar la segunda. Y si nos apetece motivarnos, podemos considerar la tercera
# https://plotly.com/python/scattermapbox/
# https://plotly.com/python/scatter-plots-on-maps/
# https://dash.plotly.com/dash-core-components/geolocation

# Expansión de la Timeline: Añadir una graduación más fina

# Expansión del Mapa: Añadir clusters, crear markers personalizados, asociar a un color por artista

# He tenido que borrar manualmente a Kanye West, a SZA y a Lana del Rey. Podemos considerar volver a añadirlos

from dash import Dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go

df = pd.read_json('data.json')

mapbox_access_token = "pk.eyJ1IjoicGFibG9zYXZpbmEiLCJhIjoiY2xwbXVreXo4MGN5bTJscXk3YjJwY291ciJ9.Kyrlg9CR1Rdo7wAzD3IAVQ"

def date2num(date):
    broken = date.split("-")
    numeric = int(broken[0]) * 10000 + int(broken[1]) * 100 + int(broken[2])
    return numeric

def month2num(date):
    numeric = 2024 * 10000 + date * 100
    return numeric

def update_map_info(selection):
    initial = selection[0]
    final = selection[1]

    latitudes = []
    longitudes = []
    names = []

    for artist in df.loc["Concerts"].index:
        for concert in df.loc["Concerts"][artist]:
            if date2num(concert["Date"]) > month2num(initial) and date2num(concert["Date"]) < month2num(final):
                name = concert["Concert Name"]
                
                latitude = concert["Latitude"]
                longitude = concert["Longitude"]

                while latitude in latitudes: 
                    latitude = str(float(latitude) + 0.005)
                    longitude = str(float(longitude) + 0.005)
                
                latitudes.append(latitude)
                longitudes.append(longitude)
                names.append(name)
    
    map = go.Figure()
    map.add_trace(go.Scattermapbox(
            lat = latitudes,
            lon = longitudes,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=10,
                color="rgb(0,0,255)"
            ),
            text=names,
            cluster=dict(enabled=True, color = "rgb(0,0,255)")
    ))
    map.update_layout(
        # title ="Concerts",
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
            # Options for style --> basic, streets, outdoors, light, dark, satellite, satellite-streets
            style = "outdoors"
        ),
    )

    return html.Div(
        [
            dcc.Graph(figure=map)
        ]
    )

def create_map_timeline() -> html.Div:
    """Creates the map timeline."""
    return html.Div(
        [
            dcc.RangeSlider
            (
                min=1,
                max=12,
                step=None,
                marks = 
                { 
                    1: "January",
                    2: "February",
                    3: "March",
                    4: "April",
                    5: "May",
                    6: "June",
                    7: "July",
                    8: "August",
                    9: "September",
                    10: "October",
                    11: "November",
                    12: "December"
                }, 
                value=[1, 12], 
                allowCross = False,
                id="date-selector"
            )
        ]
    )

def configure_callbacks_map(app) -> None:
    """
    Configures the callbacks for the app.
    This is a workaround for circular imports.
    :param app: The Dash app.
    """
    app.callback(
        Output(component_id='map', component_property='children'),
        Input(component_id='date-selector', component_property='value')
    )(update_map_info)

if __name__ == '__main__':
    app = Dash(__name__)
    app.layout = html.Div(
        [
            create_map_timeline(),
            html.Div(id='map')
        ]
    )
    configure_callbacks_map(app)
    app.run_server(debug=True)