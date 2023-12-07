from dash import html, dcc, Input, Output, Dash
import pandas as pd

# Dataframe
df = pd.read_json('data.json')

# FIXME: Many concerts share a name, so the dropdown is not unique unless we add the date.
# It's enough for selecting something while testing, but this should not be the final version.
# In the final version, the user selects a concert by clicking on the map.

import json

def get_background_style(artist):
    with open('photos.json') as f:
        photos = json.load(f)
    return {
        'backgroundImage': f'url({photos[artist][7]})',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'height': '100vh',
        'width': '100vw',
        'position': 'relative',
        #'filter': 'brightness(50%)'
    }

def create_dropdown():
    concert_names = []
    for artist in df.columns:
        for i, concert in enumerate(df[artist]["Concerts"]):
            concert_names.append(
                {
                    "label": concert["Concert Name"] + " - " + concert["Date"],
                    "value": f"{artist}.{i}"
                }
            )

    return html.Div(
        [
            html.H2("Concerts", id="concerts"),
            dcc.Dropdown(
                id='concert-dropdown',
                options=concert_names,
                value=None,
                style={'width': '50%'},
            )
        ]
    )

def update_concert_info(selection):
    # print(concert_name)
    if selection is None:
        return html.Div(
            [
                html.H3("Select a concert to see its information.")
            ]
        )
    else:
        entry = df[selection.split(".")[0]]["Concerts"][int(selection.split(".")[1])]
        default_style = {
            'color': '#A93F55',
            'textShadow': '2px 0 0 white, -2px 0 0 white, 0 2px 0 white, 0 -2px 0 white, 1px 1px white, -1px -1px 0 white, 1px -1px 0 white, -1px 1px 0 white, \
                                            2px 2px 4px rgba(0, 0, 0, 0.5)',
            'textAlign': 'left',
            'fontSize': '40px',
            'fontFamily': 'Arial'
        }
        return html.Div(
            [
                html.H3(
                    entry["Concert Name"],
                    style={
                        'color': '#A93F55',
                        'textShadow': '2px 0 0 white, -2px 0 0 white, 0 2px 0 white, 0 -2px 0 white, 1px 1px white, -1px -1px 0 white, 1px -1px 0 white, -1px 1px 0 white, \
                                            2px 2px 4px rgba(0, 0, 0, 0.5)',
                        'textAlign': 'center',
                        'fontSize': '70px',
                        'fontFamily': 'Arial'
                    }
                ),
                html.P(
                    "♿" if entry["Accessibility Services"] == "Yes" else "",
                    style=default_style
                ),
                html.P("📅 " + entry["Date"],
                    style=default_style
                ),
                html.P("📍 " + entry["Venue"],
                    style=default_style
                 ),
            ],
            style=get_background_style(artist=selection.split(".")[0])
        )

def configure_callbacks(app):
    app.callback(
        Output(component_id='concert-info', component_property='children'),
        Input(component_id='concert-dropdown', component_property='value')
    )(update_concert_info)

if __name__ == '__main__':
    app = Dash(__name__)
    app.layout = html.Div(
        [
            create_dropdown(),
            html.Div(id='concert-info')
        ]
    )
    configure_callbacks(app)
    app.run_server(debug=True)
