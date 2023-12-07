from dash import html, dcc, Input, Output, Dash
import pandas as pd

# Dataframe
df = pd.read_json('data.json')

# FIXME: Many concerts share a name, so the dropdown is not unique.
# It's enough for selecting something while testing, but this should not be the final version.
# In the final version, the user selects a concert by clicking on the map.

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
        return html.Div(
            [
                html.H3(entry["Concert Name"]),
                html.P(entry["Date"]),
                html.P(entry["Venue"])
            ]
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
