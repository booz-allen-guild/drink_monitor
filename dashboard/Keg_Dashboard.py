import datetime as dt
import random
import time

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
# import pymysql
from statsmodels.tsa.arima_model import ARIMA


def arima_kegs(times, keg_data):
    keg_df = pd.DataFrame({'Time': times, 'keg_data': keg_data})
    keg_train, keg_test = train_test_split(keg_df.keg_data, test_size=0.25, random_state=42, shuffle=False)
    for k, v in data_dict.items():
        if v == keg_data:
            name = f'{k} Forecast'
        else:
            name = 'forecasted'
    model = ARIMA(keg_train, order=(3, 2, 1))
    fitted = model.fit(disp=-1)

    # Forecast
    forecast, se, conf = fitted.forecast(len(keg_test), alpha=0.05)  # 95% conf
    #return keg_test.index, forecast
    return {'x':keg_test.index, 'y': forecast, 'type': 'line', 'name':name}

# {'x': times, 'y': list(v), 'type': 'line', 'name': k} for k, v in data_dict.items()
app = dash.Dash('Venture Cafe Beverage Forecasting')

app_color = {"graph_bg": "#082255",
             "graph_line": "007ACE"}

times = []
keg_1 = []
keg_2 = []
keg_3 = []
keg_4 = []

keg_1_name = 'Fantasyland'
keg_2_name = 'Zwickel'
keg_3_name = 'Schnickelfritz'
keg_4_name = '1910 St. Louis Lager'

# These will be selected via dropdown menu in the app
data_dict = {keg_1_name:keg_1,
keg_2_name: keg_2,
keg_3_name: keg_3,
keg_4_name:keg_4,}

now = dt.datetime.now()
sec = now.second
minute = now.minute
hour = now.hour

totalTime = (hour * 3600) + (minute * 60) + (sec)

# TODO ### Fix lines for forecasting so they go into the future, not overlaying the last several steps
# TODO ### Make colors match for all graphs

start_time = time.time()


# This function instantiates dummy data
def update_keg_values(times, keg_1, keg_2, keg_3, keg_4):


    times.append(time.time()-start_time)

    #times.append() Restart kegs every 2 minutes
    if len(times) == 1:
        #starting relevant values ~ roughly the weight of the contents of a pony keg
        keg_1.append(60)
        keg_2.append(60)
        keg_3.append(60)
        keg_4.append(60)

    elif 0 in (keg_1, keg_2, keg_3, keg_4):
        keg_1 = [60]
        keg_2 = [60]
        keg_3 = [60]
        keg_4 = [60]

    else:
        for data_of_interest in [keg_1, keg_2, keg_3, keg_4]:
            if random.random() < 0.5:
                data_of_interest.append(data_of_interest[-1]-random.random()*1)
            else:
                data_of_interest.append(data_of_interest[-1])

    return times, keg_1, keg_2, keg_3, keg_4

times, keg_1, keg_2, keg_3, keg_4 = update_keg_values(times, keg_1, keg_2, keg_3, keg_4)

app.layout = html.Div(
    [
        # header

        html.Div(
            #dbc.Container(
                html.Div(#style={'background-image':'/assets/taps.jpg'},
                         children=
                [
                    html.H1("Live Beverage Forecasting", className="display-1 text-center"
                            ),
                    html.H4(
                        "Tracking and prediction of beverage longevity in the midst of intensive innovation and networking.", className='text-center'
                    ),
                ],className='jumbotron',style={'background-image':"url('/assets/taps_transparent.jpg')",
                                                'background-size':'cover',
                                                'background-position': 'center top',
                                                 },
                #fluid=True,
                ),
            #),
        ),


        # body
        html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(id='graphs'

                        ),
                        width=8,

                    ),


                    dbc.Col(
                        html.Div(id='bar-graph'
                        ),
                        width=3,

                    ),
                ],
            ),
            # predictive frame
            dbc.Row(
                [
                    #dcc.Graph(),
                    dbc.Col(
                        html.Div(id='pred-graph'#,children=[]
                        ),
                        width=8,
                    ),

                ],
            ),

            dcc.Interval(
                id='graph-update',
                interval=1000,          ### Original 10000
                n_intervals=10000       ### Added to get around events
            )

        ]
        )
    ]
)

@app.callback(
    [
        dash.dependencies.Output('graphs','children'),
        dash.dependencies.Output('bar-graph', 'children'),
        dash.dependencies.Output('pred-graph', 'children')
    ],
    [
        dash.dependencies.Input('graph-update', 'n_intervals')
    ]
)

def update_graphs(n_intervals):

    # graphs=[]
    update_keg_values(times, keg_1, keg_2, keg_3, keg_4)

    # UPDATE LINE GRAPH
    fig = html.Div(#graphs.append(html.Div(
        dcc.Graph(
            id='keg-lines',#data_name,
            animate=True,
            figure={'data': [
                            #data_dict#[data]
                            {'x':times,'y':list(v),'type': 'line', 'name':k} for k, v in data_dict.items() #removed x:times
                            ],

                    'layout' : go.Layout(
                        legend=dict(
                            orientation='v',
                            #yanchor='top',
                            #xanchor='right',
                            y=.01,
                            x=0,
                            font=dict(
                                family="sans-serif",
                                size=16,
                                color="black"
                            )
                        ),
                        xaxis=dict(
                            range=[min(times),max(times)+10],
                            title='Time Elapsed (sec)'
                        ), #max(times)
                        yaxis=dict(
                            range=[0,60],#range=[min(data_dict[data_name])-10,131],
                            title='Weight of Remaining Beverage (lbs)'),
                        margin={'l': 75,'r':75,'t':45,'b':45}, #margins for top and left for text
                        title='{}'.format('Keg quantities remaining (actual)'),

                        height=700
                                )
                }
        )#, className='eight col')
    )
    # UPDATE BAR GRAPH
    fig2 = html.Div(
        dcc.Graph(
            id='keg-bars',  # data_name,
            #animate=True,
            figure={'data': [
                {'x': [keg_1_name, keg_2_name, keg_3_name, keg_4_name],
                     'y': [60-keg_1[-1], 60-keg_2[-1], 60-keg_3[-1], 60-keg_4[-1]],
                     'type': 'bar'}
            ],
                'layout': go.Layout(
                    xaxis=dict(
                        # range=[min(times),max(times)],
                        title='Quantities Dispensed'
                    ),  # max(times)
                    yaxis=dict(
                        range=[0, 60],  # range=[min(data_dict[data_name])-10,131],
                        title='Weight Dispensed (lbs)'),
                    margin={'l': 75, 'r': 75, 't': 45, 'b': 85},  # margins for top and left for text
                    title='{}'.format('Beer Dispensed to Guests (lbs)'),
                    height=400,
                )
            }
        )  # , className='eight col')
    )

    # UPDATE PREDICTIONS GRAPH
    fig3 = html.Div(  # graphs.append(html.Div(
        dcc.Graph(
            id='prediction-lines',  # data_name,
            animate=True,
            figure={'data': [*[
                # data_dict#[data]

                {'x': times, 'y': list(v), 'type': 'line', 'name': k} for k, v in data_dict.items()],
                *[arima_kegs(times, v) for k, v in data_dict.items()if len(times)>10]
                                                                                  # removed x:times
            ],

                'layout': go.Layout(
                    legend=dict(
                        orientation='v',
                        # yanchor='top',
                        # xanchor='right',
                        y=.01,
                        x=0,
                        font=dict(
                            family="sans-serif",
                            size=16,
                            color="black"
                        )
                    ),
                    xaxis=dict(
                        range=[min(times), max(times) + 10],
                        title='Time Elapsed (sec)'
                    ),  # max(times)
                    yaxis=dict(
                        range=[0, 60],  # range=[min(data_dict[data_name])-10,131],
                        title='Weight of Remaining Beverage (lbs)'),
                    margin={'l': 75, 'r': 75, 't': 45, 'b': 45},  # margins for top and left for text
                    title='{}'.format('Keg quantities remaining (actual)'),

                    height=700
                )
            }
        )  # , className='eight col')
    )
    return fig, fig2, fig3


external_css = ["https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)