import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import dash_table
import dash_daq as daq
import sys

f = open('/var/log/shiny-server.log', 'r')
f.close()


app = dash.Dash()

params = [
    'Lunes', 'Martes', 'Miercoles', 'Jueves',
    'Viernes', 'Sabado', 'Domingo'
]

app.layout =html.Div([
	dbc.Row([
		dbc.Col(html.Div("One of three columns"), md=4),
		dbc.Col(html.H1("Clasificador de clientes Climo")),
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

    dcc.Interval(id='interval1', interval=1 * 1000, 
n_intervals=0),
    dcc.Interval(id='interval2', interval=5 * 1000, 
n_intervals=0),
    html.H1(id='div-out', children=''),
    html.Iframe(id='console-out',srcDoc='',style={'width': 
'100%','height':400})
])


@app.callback(dash.dependencies.Output('div-out', 
'children'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update_interval(n):
    orig_stdout = sys.stdout
    f = open('out.txt', 'a')
    sys.stdout = f
    print('Resultado de la Ejecución: ' + str(n))
    sys.stdout = orig_stdout
    f.close()
    return 'Intervals Passed: ' + str(n)

@app.callback(dash.dependencies.Output('console-out', 
'srcDoc'),
    [dash.dependencies.Input('interval2', 'n_intervals')])
def update_output(n):
    file = open('out.txt', 'r')
    data=''
    lines = file.readlines()
    if lines.__len__()<=20:
        last_lines=lines
    else:
        last_lines = lines[-20:]
    for line in last_lines:
        data=data+line + '<BR>'
    file.close()
    return data

app.run_server(debug=False, port=8050)

