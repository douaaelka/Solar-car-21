import dash
import dash_core_components as dcc
import dash_html_components as html

import dash_table_experiments as dt
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import datetime
import readcontroller

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

            # html.Br([]),html.Br([]),

            # # #SPEED ALERT
            # html.Div(
            #     [
            #         # html.Div(id='alert'),
            #         dbc.Alert(
            #         [
            #             # dbc.PopoverHeader(
            #             "Optimal speed not respected",
            #             #),
            #         ],
            #         id="alert",
            #     ),
            #     ],style={"display": "block"}, className='modal'
            # ),
            html.Div(
                className='two columns',
                children=[
                #HOUR
                    html.Div([
                        html.H1(id='live-update-time'),
                        #USE INTERVAL: FOR LIVE UPDATES
                        dcc.Interval(
                            id='interval-component',
                            interval=1*1000, # in milliseconds
                            n_intervals=0)
                            ],style={'color': '#FFFFFF',"margin-right":100},
                            className='two columns'
                        ),

                    html.Br([]),html.Br([]),
                    html.Div([
                        html.Br([]),
                        #angle pedal
                        daq.Gauge(
                            id='gauge2',
                            showCurrentValue=True,
                            units="•",
                            min=0,
                            max=90,
                            value=50,
                            size=200,
                            label={'label':'Pedal Angle', 'style':{'color':'white','font-size':'10px'}},
                            style={'fontSize':10,"margin-top":50},
                            color=theme['primary'],
                            ),
                        html.Br([]),html.Br([]),
                        #Speed digital
                        daq.Gauge(
                            id='gauge',
                            showCurrentValue=True,
                            units="MPH",
                            min=0,
                            max=50,
                            value=55,
                            size=300,
                            style={'fontSize':20, "margin-left": 50,"margin-right": 50},
                            label={'label':'Speed', 'style':{'color':'white','font-size':'10px'}},
                            color=theme['primary'],
                            ),
                        html.Br([]),html.Br([]),
                        #Battery temperature
                        daq.Thermometer(
                            id='thermo',
                            min=0,
                            max=100,
                            value=40,
                            scale=1,
                            # size=100,
                            label={'label':'Motor temperature', 'style':{'color':'white','font-size':'10px'}},
                            # labelPosition='bottom',
                            color = theme['primary'],
                            showCurrentValue=True,
                            style={'fontSize':10, "margin-left": 50, "margin-right": 200},
                            units="°C",
                        )
                        ],
                        className='row'
                        ),
                    ]),

            #SPEED numerical
            html.Div([
                    daq.LEDDisplay(
                        id='LED1',
                        value=10,
                        color=theme['primary'],
                        size=0,
                        backgroundColor=theme['secondary'],
                        # className='row'
                            ),
                    html.Br([]),
                ],
                className='ml-auto'
                ),
            ],

        style={'border': 'solid 1px #A2B1C6', 'border-radius': '5px', 'padding': '50px', 'margin-top': '20px'}),
    ])



##Gauge callbacks, speed and angle
@app.callback(
    [Output(component_id='gauge', component_property='value'),
    Output(component_id='gauge2', component_property='value'),
    Output(component_id='gauge2', component_property='color'),
    Output(component_id='LED1', component_property='value'),
    ],
    Input('interval-component', 'n_intervals'),
    )

def update_speed(n):
    speednumber=20
    SpeedGauge=float(speednumber)
    # speed = speed.klsreader.py
    #Compare with profil de vitesse
    angle=int(speednumber)/4
    if int(speednumber)>21.6:
        # is_open=True
        color='danger'
    else:
        # is_open=False
        color='dark'

    return SpeedGauge, angle, speednumber, color #,is_open


#Thermometer

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


##TIME CALLBACK
@app.callback(Output('live-update-time', 'children'),
    Input('interval-component', 'n_intervals'))
def update_time(n):
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

if __name__ == '__main__':
    app.run_server(debug=True)