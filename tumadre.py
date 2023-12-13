from dash import Dash, html, Input, Output, dcc, callback_context, dash
import dash_vtk
import pandas as pd
import random
import json

# Font icons
# CSS y js
external_stylesheets = ['assets/top_artists.css', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css']
external_scripts = ['assets/top_artists.js']
app = Dash(__name__, external_stylesheets=external_stylesheets, 
           external_scripts=external_scripts, suppress_callback_exceptions=True)

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
            html.H1('ARTISTS', id='title'),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.I(className='fa fa-search', id='Search-icon'),
                                    dcc.Input(id='search', value='', type='text', placeholder= ' Search...',
                                            style={'borderRadius': '10px', 'fontSize': '15px', 'backgroundColor': '#B8938E',
                                                    'border': '5px solid #B8938E'}),
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
                    )
                ],
                className='layout'
            ),
        ]
    )


def configure_callbacks_artists(app: Dash) -> None:
    """
    Configures the callbacks for the app.
    This is a workaround for circular imports.
    :param app: The Dash app.
    """
    app.callback(
        Output(component_id='artists-info', component_property='children'),
        Input(component_id='#artists', component_property='clickData')
    )(create_artists_info)