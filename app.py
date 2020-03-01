import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import dash_table
import dash_daq as daq
import sys
import flask

external_stylesheets = ['assets/bWLwgP.css']

server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server) # call flask server

app.config.suppress_callback_exceptions = True
server = app.server
app.title = 'Clasificador de CLientes CLimo'


params = [
    'Lunes', 'Martes', 'Miercoles', 'Jueves',
    'Viernes', 'Sabado', 'Domingo'
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
            			for i in range(1, 5)
        	],
        	editable=True
    	),

    dcc.Interval(id='interval2', interval=5 * 1000, 
n_intervals=0),
    html.Div([	
    	dbc.Button("Ejecutar Modelo", color="success", className="mr-1"),
    	], style={'margin-top':'10px' ,'float': 'right', 'display': 'block'}),
    html.H1(id='div-out', children=''),
    html.Iframe(id='console-out',srcDoc='',style={'width': 
'75%','height':400})
])


@app.callback(dash.dependencies.Output('console-out', 
'srcDoc'),
    [dash.dependencies.Input('interval2', 'n_intervals')])
def update_output(n):
    file = open('/var/log/capstone.log', 'r')
    data=''
    lines = file.readlines()
    if lines.__len__()<=10:
        last_lines=lines
    else:
        last_lines = lines[-10:]
    for line in last_lines:
        data=data+line + '<BR>'
    file.close()
    return data

app.run_server(debug=False, host="0.0.0.0", port=8050)

