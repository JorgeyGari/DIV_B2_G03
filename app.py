from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# CREAR TABLA
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# ESTILO
colors = {
    'background': '#19323C',
    'text': '#A93F55'
}

df = pd.read_json('data.json')

app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children = [
    html.H1(
        children='EVENTFUL',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    generate_table(df)
])

if __name__ == '__main__':
    app.run(debug=True)