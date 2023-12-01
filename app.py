from dash import Dash, html
import pandas as pd

df = pd.read_json('data.json')

app = Dash(__name__)

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
        [html.A("Concerts", href="#concerts")]
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