import datetime as dt
import random
import time

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

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

# TODO
### Reduce to one graph, with all keg values as lines
### Fix times

### Resize first graph to make room for bar graph on side
### Add second graph, bars, showing dispensed quantities

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
                data_of_interest.append(data_of_interest[-1]-random.random()*8)
            else:
                data_of_interest.append(data_of_interest[-1])

    return times, keg_1, keg_2, keg_3, keg_4

times, keg_1, keg_2, keg_3, keg_4 = update_keg_values(times, keg_1, keg_2, keg_3, keg_4)

app.layout = html.Div(
    [
        # header
        dbc.Jumbotron(
            [
                html.H1("Live Beverage Forecasting", className="display-1 text-center"
                        ),
                html.H4(
                    "Tracking and prediction of beverage longevity in the midst of intensive innovation and networking.", className='text-center'
                ),
            ],
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
                ]
            ),
            dcc.Interval(
                id='graph-update',
                interval=10000,
                n_intervals=10000       ### Added to get around events
            )

            ]
        )
    ]
)

@app.callback(
    [dash.dependencies.Output('graphs','children'),
    dash.dependencies.Output('bar-graph', 'children')],
    [dash.dependencies.Input('graph-update', 'n_intervals')])

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
                        xaxis=dict(
                            range=[min(times),max(times)+10],
                            title='Time Elapsed (sec)'
                        ), #max(times)
                        yaxis=dict(
                            range=[0,60],#range=[min(data_dict[data_name])-10,131],
                            title='Weight of Remaining Beverage (lbs)'),
                        margin={'l': 75,'r':75,'t':45,'b':45}, #margins for top and left for text
                        title='{}'.format('Keg quantities remaining (actual)'),
                                )
                }
        )#, className='eight col')
    )
    # UPDATE BAR GRAPH
    fig2 = html.Div(
        dcc.Graph(
            id='keg-bars',  # data_name,
            animate=True,
            figure={'data': [

                    data_dict
                    # 'x': [keg_1_name, keg_2_name, keg_3_name, keg_4_name],
                    # 'y': [keg_1, keg_2, keg_3, keg_4],
                    # 'type': 'bar'

            ],
                'layout': go.Layout(
                    xaxis=dict(
                        # range=[min(times),max(times)],
                        title='Quantities Dispensed'
                    ),  # max(times)
                    yaxis=dict(
                        range=[0, 60],  # range=[min(data_dict[data_name])-10,131],
                        title='Weight Dispensed (lbs)'),
                    margin={'l': 75, 'r': 75, 't': 45, 'b': 45},  # margins for top and left for text
                    title='{}'.format('Beer Dispensed to Guests (lbs)'),
                )
            }
        )  # , className='eight col')
    )
    return fig, fig2

# @app.callback(
#     dash.dependencies.Output('bar-graph', 'children'),
#     [  # dash.dependencies.Input('vehicle-data-name', 'value'),
#         dash.dependencies.Input('graph-update', 'n_intervals')]
# )
# def update_bar_graph(n_intervals):
#     update_keg_values(times, keg_1, keg_2, keg_3, keg_4)
#
#     fig2 = html.Div(
#         dcc.Graph(
#             id='keg-bars',#data_name,
#             animate=True,
#             figure={'data': [
#                             {
#                                 'x': [keg_1_name, keg_2_name, keg_3_name, keg_4_name],
#                             'y': [keg_1, keg_2, keg_3, keg_4],
#                             'type': 'bar'
#                             }
#                             ],
#                     'layout' : go.Layout(
#                         xaxis=dict(
#                             #range=[min(times),max(times)],
#                             title='Quantities Dispensed'
#                         ), #max(times)
#                         yaxis=dict(
#                             range=[0,60],#range=[min(data_dict[data_name])-10,131],
#                             title='Weight Dispensed (lbs)'),
#                         margin={'l': 75,'r':75,'t':45,'b':45}, #margins for top and left for text
#                         title='{}'.format('Beer Dispensed to Guests (lbs)'),
#                                 )
#                 }
#         )#, className='eight col')
#     )
#     return fig2
#

external_css = ["https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)