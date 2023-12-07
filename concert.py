from dash import html

concert_info = html.Div
(
    [
        html.H2("Concerts", id="concerts"),
        html.Div
        (
            [
                html.H3("Taylor Swift"),
                html.Img(src="https://s1.ticketm.net/dam/a/a67/86eb84c0-ad6a-43c6-a55f-ff5d109c9a67_CUSTOM.jpg"),
            ]
        ),
    ]
)