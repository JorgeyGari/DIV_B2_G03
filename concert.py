from dash import html, dcc
import pandas as pd

# Dataframe
df = pd.read_json('data.json')

# Dropdown options
artists = []
for artist in df.loc["Concerts"].index:
    artists.append({'label': artist, 'value': artist})

print(artists)

concert_dropdown = html.Div(
    [
        html.H2("Concerts", id="concerts"),
        dcc.Dropdown(
            id='concert-dropdown',
            options=artists,
            style={'width': '40%'}
        )
    ]
)
