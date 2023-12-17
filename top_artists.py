from dash import Dash, html, Input, Output, dcc, callback_context
import pandas as pd
import random
import json


# Dataframe
df = pd.DataFrame(pd.read_json('data.json'))
artists = list(df.columns)

with open('photos.json', 'r') as f:
    data = json.load(f)

artists_img = []
for artist, img_list in data.items():
    if img_list:  # Check it is not empty
        artists_img.append(img_list[0])

num_bubbles = 25
bubble_size = []
for i in range(num_bubbles):
    bubble_size.append(str(250 - 8 * i))

artists_info = html.Div(
        children=[
            html.H1('TOP ARTISTS', id='artists-title'),
            html.P("The size of the bubble is proportional to the popularity of the artist. In future versions, the bubbles will be interactive, and redirect to artist's information.", id='bubble-info'),
            
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.I(className='fa fa-search', id='Search-icon'),
                                    dcc.Input(id='search', value='', type='text', placeholder= ' Search...',
                                            style={'borderRadius': '10px', 'fontSize': '15px', 'backgroundColor': '#B8938E',
                                                    'border': '10px solid #B8938E'}),
                                ],
                                id='Search-bar'
                            ),
                            dcc.Store(id='my-output', data=[]),
                            html.Div(id='resultados')  # Aquí se mostrarán los resultados
                        ],
                        className='parte-artistas'
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        className='bubble',
                                        id=f'bubble{index}',
                                        style={'width': f'{i}px',
                                            'height': f'{i}px',
                                            'top': f"{random.uniform(5, 80)}%",
                                            'left': f"{random.uniform(5, 80)}%",
                                            'backgroundImage': f'url({artists_img[index]})',
                                            'backgroundSize': 'cover',
                                            'borderRadius': '50%'},
                                    )
                                    for index, i in enumerate(bubble_size)
                                ],
                                id='bubbles-container',
                            )
                        ],
                        style={'grid-area': 'bubbles'},
                        id='bubble-space'
                    ),
                ],
                className='layout'
            ),
        ]
    )

def configure_callbacks_update_results(app: Dash) -> None:
    """
    Configures the callbacks for the app.
    This is a workaround for circular imports.
    :param app: The Dash app.
    """
    app.callback(
        Output(component_id='my-output', component_property='data'),
        Input(component_id='search', component_property='value')
    )(update_results)


def update_results(search_term):
    if not search_term:
        return artists  # Devuelve todos los artistas si el término de búsqueda está vacío

    filtered_artists = [artist for artist in artists if artist.lower().startswith(search_term.lower())]
    return filtered_artists


def configure_callbacks_display_results(app: Dash) -> None:
    """
    Configures the callbacks for the app.
    This is a workaround for circular imports.
    :param app: The Dash app.
    """
    app.callback(
    Output('resultados', 'children'),
    [Input('my-output', 'data')]
    )(display_results)

def display_results(filtered_artists):
    search_term = callback_context.triggered[0]['prop_id'].split('.')[0] if callback_context.triggered else ''
    return [html.P(f'{index + 1}. {artist}', className='artistas-encontrados') for index, artist in enumerate(filtered_artists)]

