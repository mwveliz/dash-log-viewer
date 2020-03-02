import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
import dash_table
import dash_daq as daq
import requests
import sys
import flask
import json


external_stylesheets = ['assets/bWLwgP.css']

server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server) # call flask server

app.config.suppress_callback_exceptions = True
server = app.server
app.title = 'Clasificador de CLientes CLimo'
TIME_REFRESH = 1000

params = [
    'Lun', 'Mar', 'Mie', 'Jue',
    'Vie', 'Sab', 'Dom'
]

app.layout =html.Div([
	dbc.Row([
		html.Img(src=app.get_asset_url('logoclimo.svg'), style={'height':'25%', 'width':'25%'}),
		dbc.Col(html.H1("Clasificador de clientes Climo"), lg=3),
		dbc.Col(html.Div("Tabla de consumos"), lg=1),
	]),
	
	dash_table.DataTable(
        	id='table-editing-simple',
        	columns=(
           	#[{'id': 'Semana', 'name': 'Semana'}] +
            	[{'id': p, 'name': p} for p in params]
       		),
        	data=[
            		dict(**{param: 0 for param in params})
            			for i in range(1, 2)
        	],
        	editable=True
    	),

    dcc.Interval(id='interval2', interval=3600000, n_intervals=0),
    html.Div([	
    	dbc.Button("Ejecutar Modelo", id="boton-ejecutar",color="success", className="mr-1"),
    	], style={'margin-top':'10px' ,'float': 'right', 'display': 'block'}),
    html.H1(id='div-out', children=''),
    html.Iframe(id='console-out',srcDoc='',style={'width': 
'75%','height':400})
])



#al dar click ejecutar el endpoint de Plumber
# y actualizar el input con lo que tiene el log
@app.callback(
	[dash.dependencies.Output('console-out', 'srcDoc'),
	 dash.dependencies.Output('interval2', 'interval')],
    [dash.dependencies.Input('boton-ejecutar', 'n_clicks'),
	 dash.dependencies.Input('interval2', 'n_intervals'),
	 dash.dependencies.Input('table-editing-simple', 'data')])
def update_output(n_clicks, n_intervals, df):
	data = 'Iniciando script en R...'
	if n_clicks:	
		if n_intervals==0:
			r = requests.post("http://127.0.0.1:8888/clasificar", data=json.dumps(df))
			print('Response is: ' + str(r.status_code) + ' Reason: ' + r.reason)
		data = open('/tmp/capstone.html', 'r').read()
		return [data,TIME_REFRESH]
	raise PreventUpdate

app.run_server(debug=False, host="0.0.0.0", port=8050)

