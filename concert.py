from dash import html, dcc, Input, Output, Dash, ALL
import pandas as pd

# Dataframe
df = pd.read_json('data.json')

def get_background_style(artist: str) -> dict:
    """
    Returns the background image CSS style for the artist.
    The image is retrieved from photos.json.
    :param artist: The artist performing at the concert.
    """
    photos = pd.read_json('photos.json', typ='series')
    return {
        'backgroundImage': f'url({photos[artist][7]})',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'height': '100vh',
        'width': '100vw',
        'position': 'relative',
        'margin': '0',
        'padding': '0',
        #'filter': 'brightness(50%)'
    }

# FIXME: Many concerts share a name, so the dropdown is not unique unless we add the date.
# It's enough for selecting something while developing, but this should not be the final version.
# In the final version, the user selects a concert by clicking on the map.

# def update_concert_info(selection: str | None) -> html.Div:
def update_concert_info(clickData) -> html.Div:
    """
    Updates the concert info based on the map.
    If no selection is made, a default message is displayed.
    :param selection: The clickData from the map.
    """
    # The show is still not selected correctly (I am getting the first one for each artist, not the correct one)
    if clickData is None:
        return html.Div(
            [
                html.H3("Select a concert to see its information.")
            ]
        )
    else:
        entry = df[clickData["points"][0]["text"]]["Concerts"][0]
        default_style = {
            'color': '#A93F55',
            'textShadow': '2px 0 0 white, -2px 0 0 white, 0 2px 0 white, 0 -2px 0 white, 1px 1px white, -1px -1px 0 white, 1px -1px 0 white, -1px 1px 0 white, \
                                            2px 2px 4px rgba(0, 0, 0, 0.5)',
            'textAlign': 'left',
            'fontSize': '40px',
            'fontFamily': 'Jomhuria-Regular'
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
                        'fontSize': '90px',
                        'fontFamily': 'Jomhuria-Regular'
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

def configure_callbacks(app: Dash) -> None:
    """
    Configures the callbacks for the app.
    This is a workaround for circular imports.
    :param app: The Dash app.
    """
    app.callback(
        Output(component_id='concert-info', component_property='children'),
        Input(component_id='map', component_property='clickData')
    )(update_concert_info)

# App that only shows the concert info, developing purposes only
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
