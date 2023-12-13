from dash import html, Input, Output, Dash, ALL
import pandas as pd

# Dataframe
df = pd.read_json('data.json')

# Month number to month abbreviation
month_dict = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}

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
        'backgroundPosition': 'center'
        # 'height': '100vh',
        # 'width': '100vw',
        # 'position': 'relative',
        # 'margin': '0',
        # 'padding': '0',
    }

def update_concert_info(clickData) -> html.Div:
    """
    Updates the concert info based on the map.
    If no selection is made, a default message is displayed.
    :param selection: The clickData from the map.
    """
    # FIXME: The show is still not selected correctly (map returns the first one for each artist, not the correct one)
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
                            'fontSize': '70px',
                            'fontFamily': 'Jomhuria-Regular'
                        }
                    ),
                    html.P(
                        "♿" if entry["Accessibility Services"] == "Yes" else "",
                        style=default_style
                    ),
                    # html.P(
                    #     "🎫 " + entry["Ticket Price"],
                    #     style=default_style
                    # ),
                    html.Div(
                        [
                            html.Div(
                                html.P(
                                    [
                                        html.Span(
                                            entry["Date"].split("-")[2],
                                            style={
                                                'font-size': '120px',
                                                'font-weight': 'bold',
                                                'display': 'block',
                                            }
                                        ),
                                        html.Span(
                                            month_dict[entry["Date"].split("-")[1]],
                                            style={
                                                'font-size': '60px',
                                                'display': 'block',
                                            }
                                        ),
                                        html.Span(
                                            entry["Date"].split("-")[0],
                                            style={
                                                'font-size': '40px',
                                                'opacity': '0.8',
                                                'display': 'block',
                                            }
                                        )
                                    ],
                                    style={
                                        'border': '1px solid black',
                                        'background-color': 'white',
                                        'opacity': '0.8',
                                        'text-align': 'center',
                                        'line-height': '0.5',
                                        'padding': '10px',
                                        'margin': '0',  # Updated margin value
                                        'width': '100px',
                                        'height': '100px',
                                    }
                                ),
                                style={'flex': '1'}
                            ),
                            html.Div(
                                html.P(
                                    [
                                        html.Span(
                                            entry["Time"].split(":")[0],
                                            style={
                                                'font-size': '120px',
                                                'font-weight': 'bold',
                                                'display': 'block',
                                            }
                                        ),
                                        html.Span(
                                            ":" + entry["Time"].split(":")[1],
                                            style={
                                                'font-size': '100px',
                                                'opacity': '0.8',
                                                'display': 'block',
                                            }
                                        )
                                    ],
                                    style={
                                        'border': '1px solid black',
                                        'background-color': 'white',
                                        'opacity': '0.8',
                                        'text-align': 'right',
                                        'line-height': '0.5',
                                        'padding': '10px',
                                        'margin': '0',  # Updated margin value
                                        'width': '100px',
                                        'height': '100px',
                                    }
                                ),
                                style={'flex': '1'}
                            ),
                        ],
                        style={
                            'display': 'flex',
                            'flexDirection': 'column',
                            'gap': '0',  # Remove space between grid cells
                        }
                    ),
                    html.P(
                        [
                            "📍 ",
                            html.A(
                                entry["Venue"],
                                href=f"https://www.google.com/maps/search/?api=1&query={entry['Venue']}",
                                target="_blank",
                                style=default_style
                            )
                        ]
                    ),
                ],
                style=get_background_style(artist=clickData["points"][0]["text"])
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
# if __name__ == '__main__':
#     app = Dash(__name__)
#     app.layout = html.Div(
#         [
#             create_dropdown(),
#             html.Div(id='concert-info')
#         ]
#     )
#     configure_callbacks(app)
#     app.run_server(debug=True)
