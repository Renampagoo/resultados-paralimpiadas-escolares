#%%
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px     
from dash import html

#%% # Abrir e exibir o conteúdo de final.csv

final_df = pd.read_csv('final.csv')

#%% # Remover linhas com valores faltantes na coluna 'Atleta'

final_df = final_df.dropna(subset=['Atleta'])

# Exibir o DataFrame após a remoção
# print(final_df.head())

#%% # Remover linhas com valores faltantes na coluna 'Marca'

final_df = final_df[~final_df['Marca'].isin(['JSTF', 'DNS', 'DQ'])]
final_df['Marca'] = final_df['Marca'].str.replace(':', '', regex=True)
final_df['Marca'] = pd.to_numeric(final_df['Marca'], errors='coerce')

# %%

# App Layout **************************************************************

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Analise de resultados PE", style={"textAlign": "center"}, className="row"),   # Título
    html.Div(dcc.Graph(id="box-chart", figure={}), className="row"), # Gráfico de box plot
    html.Div([
        html.Label("Selecione as classes", className="three columns",style={"textAlign": "center"},),
        html.Label("Selecione as Provas", className="three columns",style={"textAlign": "center"},),], className="row"),
    html.Div([ # Label para o Dropdown
        dcc.Dropdown(  # Dropdown para selecionar as classes
            id="my-Dropdown",
            options=[{"label": x, "value": x} for x in sorted(final_df["classe"].unique())],
            value=['T11', 'T12', 'T13'],
            multi=True,
            searchable=True,

            className="three columns"),
        
        dcc.Dropdown( # Dropdown para selecionar a distância
            id="2-dropdown",
            multi=False,
            options=[{"label": x, "value": x} for x in sorted(final_df["distancia"].unique())],
            value=['100M'],
        
            className="three columns"),
        
])
])


# Callbacks ***************************************************************
@app.callback( # Atualizar o gráfico de box plot
    Output(component_id="box-chart", component_property="figure"),
    [Input(component_id="my-Dropdown", component_property="value"),
     Input(component_id="2-dropdown", component_property="value")],
)
def update_graph(chosen_value, chosen_value2): # Função para atualizar o gráfico

    if not chosen_value:
        return {}
    if not chosen_value2:
        return {}
    
    df_filtered = final_df[final_df['classe'].isin(chosen_value)] # Filtrar o DataFrame com as classes selecionadas
    df_filtered = df_filtered[df_filtered['distancia'].isin([chosen_value2])] # Filtrar o DataFrame com a distância selecionada
    fig = px.box(
        data_frame=df_filtered,
        x="sexo",
        y="Marca",
        color='classe',
        log_y=False,
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)


# %%
