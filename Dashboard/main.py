import dash
import dash_core_components as dcc
import dash_html_components as html

import dash_table_experiments as dt
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import datetime

# -*- coding: utf-8 -*-

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']
# external_stylesheets-[dbc.themes.DARKLY] or [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],prevent_initial_callbacks=False)

colors = {
    'background': '#303030',
    'text': '#7FDBFF'
}

theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
    'backgroundColor': '#303030'
}


app.title = "Solar Car Dashboard"
def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])

app.layout = html.Div(style={'textAlign': 'center','backgroundColor': theme['backgroundColor'], 'padding' : '0px 20px 20px 20px'},
    children=[
        html.Br(),
        html.Div(className="row", children=[

            #HOUR
            html.Div([
                html.H1(id='live-update-time'),
                html.Br([]),html.Br([]),html.Br([]),html.Br([]),
                #GET LIVE VALUE of time. but the use?????????????????????????????????
                #USE INTERVAL: FOR LIVE UPDATES

                    dcc.Interval(
                    id='interval-component',
                    interval=1*1000, # in milliseconds
                    n_intervals=0)
                    ],style={'color': '#FFFFFF'}, className='ml-auto'),

            html.Br([]),html.Br([]),

            # #SPEED ALERT
            html.Div(
                [
                    # html.Div(id='alert'),
                    dbc.Alert(
                    [
                        # dbc.PopoverHeader(
                        "Optimal speed not respected",
                        #),
                    ],
                    id="alert",
                ),
                ],style={"display": "block"}, className='modal'
            ),

            html.Br([]),html.Br([]),

            #SPEED numerical
            html.Div([
                    html.Br([]),html.Br([]),html.Br([]),html.Br([]),
                    daq.LEDDisplay(
                        id='LED1',
                        value=10,
                        color=theme['primary'],
                        size=50,
                        backgroundColor=theme['secondary'],
                        # className='row'
                            ),
                    html.Br([]),
                ],
                className='mb-auto'
                ),

            #Speed digital
            html.Div([
                    html.Br([]),
                    daq.Gauge(
                        id='gauge',
                        min=0,
                        max=50,
                        value=55,
                        size=400,
                        style={'fontSize':20},
                        color=theme['primary'],
                        ),
                ],
                className='ml-auto'
                ),

            #Battery temperature
            html.Div([
                html.Br([]),html.Br([]),
                daq.Thermometer(
                    id='thermo',
                    min=0,
                    max=100,
                    value=40,
                    scale=1,
                    label=' Motor temperature',
                    # labelPosition='bottom',
                    color = theme['primary'],
                    showCurrentValue=True,
                    units="°C",
                )
                #html.Br()
            ],className='ml-auto'),
            ],
        style={'border': 'solid 1px #A2B1C6', 'border-radius': '5px', 'padding': '50px', 'margin-top': '20px'}),
    ])



##speed callback LED DISPLAY
@app.callback(
    [Output(component_id='gauge', component_property='value'),
    Output(component_id='LED1', component_property='value'),
    Output("alert", "is_open"),
    Output("alert","color"),
    # Output('alert', 'children')
    ],
    Input('interval-component', 'n_intervals'),
    # [],
    )

def update_speed(n):
    speednumber=20
    SpeedGauge=float(speednumber)
    #    speed = speed.klsreader.py
    #Compare with profil de vitesse
    if int(speednumber)>21.6:
        is_open=True
        color='danger'
    else:
        is_open=False
        color='dark'

    return SpeedGauge, speednumber,is_open,color


#Thermometre

@app.callback(
    [Output(component_id='thermo', component_property='value'),
    Output('thermo', 'color'),],
    [Input('interval-component', 'n_intervals')])

def update_thermo(n):
    temp=30
    #    temp = temp.klsreader.py
    if int(temp) >= 20:
        color = 'red'
    elif int(temp) < 20:
        color = 'blue'
    return temp, color

#----------------------------
#TODO:
#ADD values from klsreaders
#FIXME speed interval
#FIXME temperature interval



##TIME CALLBACK
@app.callback(Output('live-update-time', 'children'),
    Input('interval-component', 'n_intervals'))
def update_time(n):
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

if __name__ == '__main__':
    app.run_server(debug=True)