# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import json
import dash_bootstrap_components as dbc





#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [ dbc.themes.SUPERHERO]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/estadisticas/')
#app = dash.Dash(__name__, url_base_pathname='/estadisticas/')

server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

#Ej con s16 serie 3 dia 1


#Grafica de estadisticas/dataset
estadisticasR=pd.read_json('../scriptPythonEstadisticas/estadisticas/stats.json')
datasets=estadisticasR['dataset'].unique()

#Grafica estadisticas mes/año
estadisticasMesAñoDescargasVisitas=pd.read_json('../scriptPythonEstadisticas/estadisticas/statsDescargasVisitasMesAño.json')

#Grafica estadisticas nº datasets
numeroDatasetsFecha=pd.read_json('../scriptPythonEstadisticas/estadisticas/numeroTotalDatasets.json')



#mapa de IPs
latlongIP=pd.read_json('../scriptPythonEstadisticas/estadisticas/infoIPs.json')

#Grafica de formatos
formatos=pd.read_json('../scriptPythonEstadisticas/estadisticas/statsFormatos.json')

opciones=['Open data','hola','adios']
ref=['/']

app.title="Dashboard"

app.layout=html.Div(children=[

        html.Div(id='superior'),


        html.Div(children=[

            html.Div(children=[


                html.Img(src="assets/logo-ugr-negativo.svg"),

            

                html.Div(children=[

                    html.Ul(id='menu', children=[


                        html.Li(html.A(i,href='/')) for i in opciones


                    ]),

                ]),



            ], className="banner"),

        ], className="container"),

        html.Main(children=[


            html.H2('Estadisticas del portal open data de la UGR'),



            html.Div(id='fila1',children=[

                dcc.Graph(
                    id='graficaMesAño',
                    figure=go.Figure(data=[
                        go.Bar(name='Descargas',x=estadisticasMesAñoDescargasVisitas['mes/año'], y=estadisticasMesAñoDescargasVisitas['descargas']),
                        go.Bar(name='Visitas',x=estadisticasMesAñoDescargasVisitas['mes/año'], y=estadisticasMesAñoDescargasVisitas['visitas']),



                    ]).update_layout(title='Descargas / visualizaciones realizadas en cada mes',yaxis_title="Nº Descargas/Visualizaciones", xaxis_title="Mes/Año")

                ),



                dcc.Graph(
                    id='graficaDatasetsTotales',
                    figure=go.Figure(data=[
                        go.Scatter(name='Nº de conjuntos de datos', x= numeroDatasetsFecha['fecha'], y=numeroDatasetsFecha['nº conjuntos']),
                        go.Scatter(name='Nº de recursos de datos', x= numeroDatasetsFecha['fecha'], y=numeroDatasetsFecha['nº recursos']),

                    ]).update_layout(title='Nº total de datasets y recursos alojados',xaxis_title='Fecha',yaxis_title="Nº de datasets")
                ),


            ]),


            html.Div(id='fila2',children=[


                dcc.Graph(
                    id='graficaFormatos',
                    figure=go.Figure(data=[
                        go.Bar(name='Formatos',x=formatos['formato'], y=formatos['contador']),
                    ]).update_layout(title='Formatos alojados en el servidor',yaxis_title="Cantidad", xaxis_title="Formato")
                ),


                html.Div(id='selectorDataset',children=[


                    html.Label('Conjunto de datos elegido'),
                    dcc.Dropdown(
                        id='dataset',
                        options=[{'label': i, 'value': i} for i in datasets],
                        value=datasets[0]
                    ),

                    dcc.Graph(
                        id='graficaDV',
                    ),

                ]),






            ]),



            dcc.Graph(
                id='mapa',
                figure=go.Figure(
                    data=go.Scattergeo(lon=latlongIP['long'],lat=latlongIP['lat'], text=latlongIP['city'], mode='markers'),

                ).update_layout(
                    #showlegend= True,
                    title="Ubicaciones"

                )


            ),




        ])

    ])

@app.callback(
    Output(component_id='graficaDV',component_property='figure'),
    Input(component_id='dataset',component_property='value'),
)

def update_graph(dataset):
    resourceElegido=estadisticasR.loc[estadisticasR['dataset'] == dataset]

    fig=go.Figure(data=[
        go.Bar(name='Descargas',y=resourceElegido['nombre'],x=resourceElegido['descargas'], orientation='h'),
        go.Bar(name='Visitas',y=resourceElegido['nombre'],x=resourceElegido['visitas'], orientation='h', textposition='auto')

    ]).update_layout(title='Descargas / Visualizaciones totales',xaxis_title="Nº Descargas/Visualizaciones", yaxis_title="Nombre del resource",)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=True, host='150.214.104.25')
