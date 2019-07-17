import datetime as dt
import random
import time
from collections import deque

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash('Venture Cafe Beverage Forecasting')

app_color = {"graph_bg": "#082255",
             "graph_line": "007ACE"}

max_length = 1000
times = deque(maxlen=max_length)
keg_1 = deque(maxlen=max_length)
keg_2 = deque(maxlen=max_length)
keg_3 = deque(maxlen=max_length)
keg_4 = deque(maxlen=max_length)

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


# This function instantiates dummy data
def update_keg_values(times, keg_1, keg_2, keg_3, keg_4):

    times.append(time.time())

    #times.append()
    if len(times) == 1:
        #starting relevant values ~ roughly the weight of the contents of a pony keg
        keg_1.append(131)
        keg_2.append(131)
        keg_3.append(131)
        keg_4.append(131)

    else:
        for data_of_interest in [keg_1, keg_2, keg_3, keg_4]:
            if random.random() < 0.5:
                data_of_interest.append(data_of_interest[-1]-random.random()*12)

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
            children=html.Div(id='graphs'),
            #className='row'),
        ),
        dcc.Interval(
            id='graph-update',
            interval=5000,
            n_intervals=10000       ### Added to get around events
        ),


        ],


)


@app.callback(
    dash.dependencies.Output('graphs','children'),
    [#dash.dependencies.Input('vehicle-data-name', 'value'),
    dash.dependencies.Input('graph-update', 'n_intervals')]
)

def update_graph(n_intervals):
    graphs = []

    update_keg_values(times, keg_1, keg_2, keg_3, keg_4)

    for data_name in list(data_dict.keys()):

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],
                    'layout' : go.Layout(
                        # plot_bgcolor=app_color["graph_bg"],
                        # paper_bgcolor=app_color["graph_bg"],
                        xaxis=dict(
                            range=[min(times),max(times)],
                        ), #max(times)
                        yaxis=dict(
                            range=[min(data_dict[data_name])-10,131],
                            title='Weight of Remaining Beverage (lbs)'),
                            #margin={'l':50,'r':1,'t':45,'b':45}, #margins for top and left for text
                            title='{}'.format(data_name),
                                )
                    }
            ), className='col s6')
        )

    return graphs

external_css = ["https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)