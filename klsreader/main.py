import dash
import dash_core_components as dcc
import dash_html_components as html

import dash_table_experiments as dt
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import datetime
import time
from pprint import pprint
from serial import Serial
from controllerdata import *
from controllercommand import *
from sys import platform


# if __name__ == "__main__":
    # change to the appropriate commport when running as __main__
if platform.startswith("win"):
    serialport = 'COM4'
else:
    serialport = '/dev/tty.usbserial-1440'

class ControllerConnector(object):
    def __init__(self, serialport):
        self.serialport = serialport

    def startSerial(self):
        self.connection = Serial(self.serialport, 19200, timeout=5)

    def getBytes(self, *commands):
        ser = self.connection
        packets = []
        for command in commands:
            ser.write(command)
            packet = ser.read(19)
            packets.append(packet)
        return packets

class KLSReader(object):
    def __init__(self, serialport):
        self.connector = ControllerConnector(serialport)
        self.connector.startSerial()
        self.command = ControllerCommand()

    def getData(self):
        packet_a, packet_b = self.connector.getBytes(self.command.a, self.command.b)
        data = ControllerData(packet_a, packet_b)
        return data.__dict__
        
controller = KLSReader(serialport)

# from klsreader import *


# -*- coding: utf-8 -*-

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']
# external_stylesheets-[dbc.themes.DARKLY] or [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],prevent_initial_callbacks=True)

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
            html.Div(
                className='two columns',style={"margin-left":200},
                children=[
                #HOUR
                    html.Div([
                        html.H1(id='live-update-time'),
                        #USE INTERVAL: FOR LIVE UPDATES
                        dcc.Interval(
                            id='interval-component',
                            interval=1*1000, # in milliseconds
                            n_intervals=0)
                            ],style={'color': '#FFFFFF',"margin-right":60},
                            className='two columns'
                        ),

                    html.Br([]),html.Br([]),
                    html.Div([
                        html.Br([]),
                        #angle pedal
                        daq.Gauge(
                            id='gauge2',
                            showCurrentValue=True,
                            units=" ",
                            min=0,
                            max=90,
                            value=0,
                            size=200,
                            label={'label':'Pedal Angle', 'style':{'color':'white','font-size':'20px'}},
                            style={'fontSize':10,"margin-top":50},
                            color=theme['primary'],
                            ),
                        html.Br([]),html.Br([]),
                        #Speed digital
                        daq.Gauge(
                            id='gauge',
                            showCurrentValue=True,
                            units="Km per h",
                            min=0,
                            max=700,
                            value=0,
                            size=300,
                            style={'fontSize':20, "margin-left": 50,"margin-right": 50},
                            label={'label':'Speed', 'style':{'color':'white','font-size':'20px'}},
                            color=theme['primary'],
                            ),
                        html.Br([]),html.Br([]),
                        #Battery temperature
                        daq.Gauge(
                            id='thermo',
                            min=0,
                            max=100,
                            value=40,
                            scale=1,
                            size=200,
                            label={'label':'Motor temperature', 'style':{'color':'white','font-size':'20px'}},
                            # labelPosition='bottom',
                            color = theme['primary'],
                            showCurrentValue=True,
                            style={'fontSize':10,"margin-top":50, "margin-left": 10,"margin-right": 50},
                            units=" C",
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
    Output(component_id='thermo', component_property='value'),
    Output('thermo', 'color'),],
    Input('interval-component', 'n_intervals'),
    )


def update_value(n):
    print("Connected to motor controller")
    data = controller.getData()
    # pprint(data)
    # time.sleep(1)
    #     # print(Dict)
    time.sleep(0.1)
    # throttle=data['throttle']
    temp=data['motorTemp']
    rpm=data['rpm']
    # print("sor3a ta9tol")
    print('-------------------')
    print(rpm)
    # print(throttle)
    # print('-------------------')
    # print("ME UPDATING L7ARARAAAA")
    # print(temp)
    # print('-------------------')
    # speednumber=(throttle-18)*260*0.001885*0.5
    speednumber=rpm/4
    SpeedGauge=float(speednumber)
    # speed = speed.readcontroller.py
    angle=SpeedGauge/6
    # print(angle)
    if int(angle)>25:
        # is_open=True
        colorangle='red'
    else:
        # is_open=False
        colorangle='green'
    if int(temp) >= 20:
        color1 = 'red'
    elif int(temp) < 20:
        color1 = 'blue'

    return SpeedGauge, angle, colorangle, speednumber,temp, color1 #,is_open




##TIME CALLBACK
@app.callback(Output('live-update-time', 'children'),
    Input('interval-component', 'n_intervals'))
def update_time(n):
    now = datetime.datetime.now()
    print("m updating the time")
    return now.strftime("%H:%M")

if __name__ == '__main__':
    print("m in the dash")
    app.run_server(debug=True)