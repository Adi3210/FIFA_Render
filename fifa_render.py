"""
# Deployment Link: https://
"""

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Step 1: Create/Load the Dataset
data = [
    {"Year": 1930, "Winner": "Uruguay",       "Runner-Up": "Argentina"},
    {"Year": 1934, "Winner": "Italy",         "Runner-Up": "Czechoslovakia"},
    {"Year": 1938, "Winner": "Italy",         "Runner-Up": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay",       "Runner-Up": "Brazil"},
    {"Year": 1954, "Winner": "Germany",       "Runner-Up": "Hungary"},
    {"Year": 1958, "Winner": "Brazil",        "Runner-Up": "Sweden"},
    {"Year": 1962, "Winner": "Brazil",        "Runner-Up": "Czechoslovakia"},
    {"Year": 1966, "Winner": "England",       "Runner-Up": "Germany"},
    {"Year": 1970, "Winner": "Brazil",        "Runner-Up": "Italy"},
    {"Year": 1974, "Winner": "Germany",       "Runner-Up": "Netherlands"},
    {"Year": 1978, "Winner": "Argentina",     "Runner-Up": "Netherlands"},
    {"Year": 1982, "Winner": "Italy",         "Runner-Up": "Germany"},
    {"Year": 1986, "Winner": "Argentina",     "Runner-Up": "Germany"},
    {"Year": 1990, "Winner": "Germany",       "Runner-Up": "Argentina"},
    {"Year": 1994, "Winner": "Brazil",        "Runner-Up": "Italy"},
    {"Year": 1998, "Winner": "France",        "Runner-Up": "Brazil"},
    {"Year": 2002, "Winner": "Brazil",        "Runner-Up": "Germany"},
    {"Year": 2006, "Winner": "Italy",         "Runner-Up": "France"},
    {"Year": 2010, "Winner": "Spain",         "Runner-Up": "Netherlands"},
    {"Year": 2014, "Winner": "Germany",       "Runner-Up": "Argentina"},
    {"Year": 2018, "Winner": "France",        "Runner-Up": "Croatia"},
    {"Year": 2022, "Winner": "Argentina",     "Runner-Up": "France"}
]

df = pd.DataFrame(data)



# Count the number of times each country has won
wins_df = df.groupby('Winner').size().reset_index(name='Times Won')


# Step 2: Create the Choropleth Map of World Cup wins
fig_choropleth = px.choropleth(
    wins_df,
    locations="Winner",
    color="Times Won",
    hover_name="Winner",
    color_continuous_scale=px.colors.sequential.Plasma,
    locationmode="country names",
    title="FIFA World Cup Wins by Country"
)
fig_choropleth.update_layout(margin={"r":0,"t":50,"l":0,"b":0})


# Step 3: Build the Dash App Layout

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={"textAlign": "center"}),

 
    html.Div([
        dcc.Graph(id='wc-map', figure=fig_choropleth)
    ], style={"width": "70%", "margin": "auto"}),

 
    html.Div([
        html.H3("A) Countries that have won the World Cup:"),
        html.Div(id='list-of-winners'),

        html.Button("Show All Winners", id="show-winners-btn", n_clicks=0),
    ], style={"textAlign": "center", "marginTop": "20px"}),

  
    html.Div([
        html.H3("B) Select a country to see how many times it has won:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{"label": c, "value": c} for c in sorted(wins_df['Winner'].unique())],
            placeholder="Select a country"
        ),
        html.Div(id='country-wins-output', style={"marginTop": "10px"})
    ], style={"width": "50%", "margin": "auto"}),

    html.Div([
        html.H3("C) Select a year to see the Winner and Runner-up:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{"label": y, "value": y} for y in sorted(df['Year'].unique())],
            placeholder="Select a year"
        ),
        html.Div(id='year-output', style={"marginTop": "10px"})
    ], style={"width": "50%", "margin": "auto", "marginBottom": "40px"})
])


# Step 4: Callbacks

@app.callback(
    Output('list-of-winners', 'children'),
    Input('show-winners-btn', 'n_clicks')
)
def show_winners(n_clicks):
    if n_clicks > 0:
        all_winners = sorted(wins_df['Winner'].unique().tolist())
        return html.Ul([html.Li(w) for w in all_winners])
    return ""


@app.callback(
    Output('country-wins-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_wins(selected_country):
    if selected_country is None:
        return ""
    times = wins_df.loc[wins_df['Winner'] == selected_country, 'Times Won'].values
    if len(times) > 0:
        return f"{selected_country} has won the World Cup {times[0]} time(s)."
    else:
        return f"{selected_country} has not won the World Cup."


@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_info(selected_year):
    if selected_year is None:
        return ""
    row = df.loc[df['Year'] == selected_year]
    if not row.empty:
        winner = row.iloc[0]['Winner']
        runner_up = row.iloc[0]['Runner-Up']
        return f"In {selected_year}, the winner was {winner}, and the runner-up was {runner_up}."
    return "No data found for that year."


# Run server
if __name__ == "__main__":
    app.run(debug=True)
