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
external_stylesheets = [ dbc.themes.SUPERHERO, 'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
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

opciones=['Portal Open Data']
ref=['/']

app._favicon = ("faviconUGR.ico")
app.title="Dashboard de OpenData UGR"


app.index_string = '''
<!DOCTYPE html>
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='es' lang='es'>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''




app.layout=html.Div(children=[

        html.Div(id='superior',children=[

            html.Div(children=[

                html.Ul(id='menu', children=[

                    html.Li(html.A(i,href='/',target='_blank',title='Portal de datos abiertos')) for i in opciones


                ]),

            ]),

        ]),

        html.Div(children=[

            html.Div(children=[

                html.Div(id='titulo',children=[

                    html.A('Estadísticas OpenData',href='',title='Home'),



                ]),


                html.Div(id='imagen',children=[

                    html.A(html.Img(src="assets/logo-ugr-negativo.svg",alt="imagen corporativa UGR"),href='https://www.ugr.es',target='_blank',title='Universidad de Granada'),

                ]),

            ], className="banner"),

        ], className="container"),

        html.Main(children=[


            html.Div(id='fila1',children=[

                html.H1('Estadísticas de uso'),

                dcc.Graph(
                    id='graficaMesAño',
                    figure=go.Figure(data=[
                        go.Bar(name='Descargas',x=estadisticasMesAñoDescargasVisitas['mes/año'], y=estadisticasMesAñoDescargasVisitas['descargas']),
                        go.Bar(name='Visitas',x=estadisticasMesAñoDescargasVisitas['mes/año'], y=estadisticasMesAñoDescargasVisitas['visitas']),



                    ]).update_layout(title='Descargas / visualizaciones realizadas en cada mes',yaxis_title="Nº Descargas/Visualizaciones", xaxis_title="Mes/Año")

                ),

                html.Div(id='selectorDataset',children=[


                    html.Label('Conjunto de datos elegido'),
                    dcc.Dropdown(
                        id='dataset',
                        options=[{'label': i, 'value': i} for i in datasets],
                        value=datasets[0],
                        placeholder='Seleccione un dataset',
                    ),

                    dcc.Graph(
                        id='graficaDV',
                    ),

                ]),






            ]),


            html.Div(id='fila2',children=[



                html.H1('Formatos, recursos y datos'),
                dcc.Graph(
                    id='graficaFormatos',
                    figure=go.Figure(data=[
                        go.Bar(name='Formatos',x=formatos['formato'], y=formatos['contador']),
                    ]).update_layout(title='Formatos alojados en el servidor',yaxis_title="Cantidad", xaxis_title="Formato")
                ),



                dcc.Graph(
                    id='graficaDatasetsTotales',
                    figure=go.Figure(data=[
                        go.Scatter(name='Nº de conjuntos de datos', x= numeroDatasetsFecha['fecha'], y=numeroDatasetsFecha['nº conjuntos']),
                        go.Scatter(name='Nº de recursos de datos', x= numeroDatasetsFecha['fecha'], y=numeroDatasetsFecha['nº recursos']),

                    ]).update_layout(title='Nº total de datasets y recursos alojados',xaxis_title='Fecha',yaxis_title="Nº de datasets")
                ),



            ]),

            html.Div(id='fila3',children=[

                html.H1('Ubicaciones'),
                dcc.Graph(
                    id='mapa',
                    figure=go.Figure(
                        data=go.Scattergeo(lon=latlongIP['long'],lat=latlongIP['lat'], text=latlongIP['city'], mode='markers'),

                    ).update_layout(
                        #showlegend= True,
                        title="Ubicaciones"

                    )

                ),




            ]),


        ]),


        html.Footer(children=[

            html.Div(id='footerSuperior',children=[

                html.Div(id='col1',children=[

                    html.Div(children=[

                        html.A(html.Img(src="assets/logo-ugr-negativo.svg",alt="imagen corporativa UGR"),href='https://www.ugr.es',target='_blank',title='Universidad de Granada'),

                        html.A(html.Img(src="assets/osl_logo_negativo.svg",alt="imagen corporativa OSL"),href='https://osl.ugr.es/',target='_blank',title='Oficina de Software Libre'),

                    ]),


                ]),

                html.Div(id='col2',children=[


                    html.H2('Enlaces destacados'),

                    html.Ul(children=[

                        html.Li(
                            html.A('Portal Open Data',href='/',target='_blank',title='Portal de datos abiertos'),
                        ),

                        html.Li(
                            html.A('Catálogo de datos',href='',target='_blank',title='Catálogo de datos'),
                        ),

                        html.Li(
                            html.A('SPARQL',href='',target='_blank',title='Portal SPARQL'),
                        ),

                    ]),


                ]),

            ]),


            html.Div(id='inferior',children=[

                html.H2('© 2022 Universidad de Granada'),

                html.Ul(children=[


                    html.Li(
                        'Siguenos en redes sociales'
                    ),

                    html.Li(


                        html.A(html.I(className='fab fa-facebook-f fa-2x'),href='https://es-es.facebook.com/SoftwareLibreUGR/',target='_blank',title='Facebook'),
                    ),


                    html.Li(
                        html.A(html.I(className='fab fa-twitter fa-2x'),href='https://twitter.com/OSLUGR',target='_blank',title='Twitter'),
                    ),


                    html.Li(
                        html.A(html.I(className='fab fa-youtube fa-2x'),href='https://www.youtube.com/user/oslugr',target='_blank',title='YouTube'),
                    ),

                ]),


            ]),



        ]),

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

#if __name__ == '__main__':
#    app.run_server(debug=False)
#    app.run_server(debug=True, host='150.214.104.25')
