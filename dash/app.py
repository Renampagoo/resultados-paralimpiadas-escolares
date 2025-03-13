from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_csv('final.csv')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(df.Classe.unique(), 'Canada', id='dropdown-selection')
        ], width=2, style={'padding': '20px'}),
        dbc.Col([
            dcc.Graph(id='graph-content1')
        ], width=10)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph-content2')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='graph-content3')
        ], width=6)
    ])
], fluid=True)

@callback(
    Output('graph-content1', 'figure'),
    Output('graph-content2', 'figure'),
    Output('graph-content3', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    print('value:', value)
    dff = df[df.Classe == value]
    fig1 = px.bar(dff, x='UF', y='pop')
    fig2 = px.line(dff, x='year', y='lifeExp')
    fig3 = px.pie(df, names='continent', values='pop', title='Population by Continent')
    return fig1, fig2, fig3

if __name__ == '__main__':
    app.run(debug=True)