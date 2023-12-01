# Referencias

# Para el date selector he usado la primera, pero podríamos explorar la segunda
# https://dash.plotly.com/dash-core-components/rangeslider
# https://plotly.com/python/range-slider/

# Para el mapa he usado la primera, y también se podría explorar la segunda. Y si nos apetece motivarnos, podemos considerar la tercera
# https://plotly.com/python/scattermapbox/
# https://plotly.com/python/scatter-plots-on-maps/
# https://dash.plotly.com/dash-core-components/geolocation

from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objects as go


df = pd.read_json('data.json')

app = Dash(__name__)

mapbox_access_token = "pk.eyJ1IjoicGFibG9zYXZpbmEiLCJhIjoiY2xwbXVreXo4MGN5bTJscXk3YjJwY291ciJ9.Kyrlg9CR1Rdo7wAzD3IAVQ"

map = go.Figure(go.Scattermapbox(
        lat=["40.3324408", "51.5287398"],
        lon=["-3.7676849", "-0.2664044"],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=["Universidad", "Londres"],
    ))

map.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=40.3324408,
            lon=-3.7676849
        ),
        pitch=0,
        zoom=1
    ),
)

app.layout = html.Div([
    html.H1
    (
        'EVENTFUL'
    ),
    
    html.Div 
    (
        [html.A("Artists", href="#artists")]
    ),

    html.Div
    (
        [
            html.A("Concerts", href="#concerts"),
            dcc.Graph(figure=map),
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
    ),
    
    html.Div 
    (
        [html.H2("Artists", id="artists")] +
        [html.Br()]*50 +
        [html.H2("Concerts", id="concerts")]
    )
])

if __name__ == '__main__':
    app.run(debug=True)