# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, Patch, no_update
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

# Incorporate data
df = pd.read_csv('midyear_population_age_country_code.csv', usecols=['year', 'age', 'country_name'])
dff = df.groupby(["country_name","year"])[["age"]].mean().reset_index()

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Creating our figure
fig = px.scatter(dff, x='year', y='age', hover_name='country_name')
fig.update_traces(marker=dict(color="blue"))

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div("Partial Properties Update Demo in OSS", className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        dcc.Dropdown(id="dropdown", options=dff.country_name.unique()),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div("Without partial property updates, the whole figure -- including its data -- is passed from the server to the browser"),
            html.Br(),
            dcc.Graph(id="graph-update-example", figure=fig)
        ], width=6),

        dbc.Col([
            html.Div("With partial property updates, only the necessary part -- is passed from the server to the browser"),
            html.Br(),
            dcc.Graph(id="graph-update-example-2", figure=fig),
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            dmc.Prism(
                        language="python",
                        children="""
@app.callback(
    Output("graph-update-example", "figure"),
    Input("dropdown", "value"),
    prevent_initial_call=True
)
def update_markers(country):
    if not country:
        return no_update
    else:
        updated_marker_color = ["red" if country_name == country else "blue" for country_name in dff.country_name]
        updated_marker_size = [24 if country_name == country else 6 for country_name in dff.country_name]

        fig.update_traces(marker_color=updated_marker_color, marker_size=updated_marker_size)
        return fig  
            """,
                    ),
        ], width=6),

        dbc.Col([
            dmc.Prism(
                        language="python",
                        children="""
@app.callback(
    Output("graph-update-example-2", "figure"),
    Input("dropdown", "value"),
    prevent_initial_call=True
)
def update_markers(country):
    if not country:
        return no_update
    else:
        updated_marker_color = ["red" if country_name == country else "blue" for country_name in dff.country_name]
        updated_marker_size = [24 if country_name == country else 6 for country_name in dff.country_name]

        patched_figure = Patch()
        patched_figure['data'][0]['marker']['color'] = updated_marker_color
        patched_figure['data'][0]['marker']['size'] = updated_marker_size
        return patched_figure
            """,
                    ),
        ], width=6),
    ]),

], fluid=True)

# Add controls to build the interaction
@app.callback(
    Output("graph-update-example-2", "figure"),
    Input("dropdown", "value"),
prevent_initial_call=True
)
def update_markers(country):
    if not country:
        return no_update
    else:
        updated_marker_color = ["red" if country_name == country else "blue" for country_name in dff.country_name]
        updated_marker_size = [24 if country_name == country else 6 for country_name in dff.country_name]

        patched_figure = Patch()
        patched_figure['data'][0]['marker']['color'] = updated_marker_color
        patched_figure['data'][0]['marker']['size'] = updated_marker_size
        return patched_figure


@app.callback(
    Output("graph-update-example", "figure"),
    Input("dropdown", "value"),
    prevent_initial_call=True
)
def update_markers(country):
    if not country:
        return no_update
    else:
        updated_marker_color = ["red" if country_name == country else "blue" for country_name in dff.country_name]
        updated_marker_size = [24 if country_name == country else 6 for country_name in dff.country_name]

        fig.update_traces(marker_color=updated_marker_color, marker_size=updated_marker_size)
        return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)