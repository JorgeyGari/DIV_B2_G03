from dash import Dash, html, Input, Output, dcc, callback_context, dash
import dash_vtk
import pandas as pd
import random
import json

# Font icons
# CSS y js
external_stylesheets = ['assets/pruebahtml.css', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css']
external_scripts = ['assets/pruebahtml.js']
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

app.layout = html.Div(
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

@app.callback(
    Output('my-output', 'data'),
    [Input('search', 'value')]
)
def update_results(search_term):
    if not search_term:
        return artists  # Devuelve todos los artistas si el término de búsqueda está vacío

    filtered_artists = [artist for artist in artists if artist.lower().startswith(search_term.lower())]
    return filtered_artists

@app.callback(
    Output('resultados', 'children'),
    [Input('my-output', 'data')]
)
def display_results(filtered_artists):
    search_term = callback_context.triggered[0]['prop_id'].split('.')[0] if callback_context.triggered else ''
    return [html.P(f'{index + 1}. {artist}', className='artistas-encontrados') for index, artist in enumerate(filtered_artists)]

# Nuevo callback para ocultar las burbujas al hacer clic en un artista
# @app.callback(
#     Output('resultados', 'style'),
#     [Input(f'bubble{i}', 'n_clicks') for i in range(1, num_bubbles)]
# )
# def hide_artists(*args):
#     ctx = callback_context
#     if not ctx.triggered_id:
#         return dash.no_update

#     # Si alguna burbuja ha sido clicada, oculta los artistas
#     if any(args):
#         return {'display': 'none'}
#     else:
#         return dash.no_update

@app.callback(
    Output('resultados', 'style'),
    [Input('bubble-space', 'children')]
)
def hide_artists(children):
    return {'display': 'none'} if children else {'display': 'block'}

if __name__ == '__main__':
    app.run(debug=True)
