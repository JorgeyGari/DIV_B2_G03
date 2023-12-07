from dash import html, dcc, Input, Output
import pandas as pd

# Dataframe
df = pd.read_json('data.json')

# Dropdown
concert_names = []
for artist in df.loc["Concerts"].index:
    for concert in df.loc["Concerts", artist]:
        concert_names.append(
            {
                'label': concert["Concert Name"],
                'value': concert["Concert Name"]
            }
        )
# FIXME: Many concerts share a name, so the dropdown is not unique.
# It's enough for selecting something while testing, but this should not be the final version.
# In the final version, the user selects a concert by clicking on the map.

def create_dropdown():
    concert_names = []
    for artist in df.loc["Concerts"].index:
        for concert in df.loc["Concerts", artist]:
            concert_names.append(
                {
                    'label': concert["Concert Name"],
                    'value': concert["Concert Name"]
                }
            )

    return html.Div(
        [
            html.H2("Concerts", id="concerts"),
            dcc.Dropdown(
                id='concert-dropdown',
                options=concert_names,
                style={'width': '50%'},
                value=None
            )
        ]
    )

def update_concert_info(concert_name):
    # print(concert_name)
    if concert_name is None:
        return html.Div(
            [
                html.H3("Select a concert to see its information.")
            ]
        )
    else:
        return html.H3(concert_name)    

def configure_callbacks(app):
    app.callback(
        Output(component_id='concert-info', component_property='children'),
        Input(component_id='concert-dropdown', component_property='value')
    )(update_concert_info)