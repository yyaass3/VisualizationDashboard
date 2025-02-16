import pandas as pd
from dash import Dash, dcc, html, Input, Output

# Initializing the Dash Application
data = (pd.read_csv('city_day.csv').assign(Date=lambda data: pd.to_datetime(data['Date'], format="%Y-%m-%d")).sort_values(by='Date'))
regions = data['City'].sort_values().unique()

external_stylesheets = [{'href': ("https://fonts.googleapis.com/css2?"
                                  "family=Lato:wght@400;700&display=swap"),
                         'rel': 'stylesheet'}]
app = Dash(__name__, external_stylesheets= external_stylesheets)
app.title = 'Weather Analytics'

# Defining the Layout of Your Dash Application
app.layout = html.Div(children=[html.Div(children=[
                                                   html.H1(children='Weather Analytics',
                                                           className='header-title'),
                                                   html.P(children=('Analyze the behavior of NO, NO2 and Benzene metric in india and Bengaluru city between 2015 and 2020'
                                                                    ),
                                                          className='header-description'),
                                                   ],
                                         className='header'),
                                html.Div(children=[html.Div(children=[html.Div(children='City', className='menu-title'),
                                                                      dcc.Dropdown(id='region-filter',
                                                                                   options=[{'label': region, 'value': region}
                                                                                           for region in regions],
                                                                                   value='Bengaluru',
                                                                                   clearable=False,
                                                                                   className='dropdown')]),
                                                   html.Div(children=[html.Div(children='Date Range', className='menu-title'),
                                                                      dcc.DatePickerRange(id='date-range',
                                                                                          min_date_allowed=data['Date'].min().date(),
                                                                                          max_date_allowed=data['Date'].max().date(),
                                                                                          start_date=data['Date'].min().date(),
                                                                                          end_date=data['Date'].max().date())])],
                                         className='manu'),

                                html.Div(children=[html.Div(children=dcc.Graph(
                                                                id='price-chart',
                                                                config={'displayModeBar': False}),
                                                            className='card'),
                                                   html.Div(children=dcc.Graph(
                                                                id='volume-chart',
                                                                config={'displayModeBar': False},
                                                                ),
                                                            className='card'),
                                                   html.Div(children=dcc.Graph(
                                                                id='volume2-chart',
                                                                config={'displayModeBar': False},
                                                                ),
                                                            className='card')],
                                         className='wrapper')])


@app.callback(Output('price-chart', 'figure'),
              Output('volume-chart', 'figure'),
              Output('volume2-chart', 'figure'),
              Input('region-filter', 'value'),
              Input('date-range', 'start_date'),
              Input('date-range', 'end_date'))
def update_charts(region, start_date, end_date):
    filtered_data = data.query("City == @region and Date >= @start_date and Date <= @end_date")
    price_chart_figure = {'data': [{'x': filtered_data['Date'],
                                    'y': filtered_data['NO'],
                                    'type': 'lines',
                                    'hovertemplate': '$%{y:.2f}<extra></extra>'}],
                          'layout': {'title': {'text': 'NO Changes',
                                               'x': 0.05,
                                               'xanchor': 'left'},
                                     'xaxis': {'fixedrange': True},
                                     'yaxis': {'tickprefix': '$', 'fixedrange': True},
                                     'colorway': ['#17b897']}}
    volume_chart_figure = {'data': [{'x': filtered_data['Date'],
                                     'y': filtered_data['NO2'],
                                     'type': 'lines'}],
                           'layout': {'title': {'text': 'NO2 changes', 'x': 0.05, 'xanchor': 'left'},
                                      'xaxis': {'fixedrange': True},
                                      'yaxis': {'fixedrange': True},
                                      'colorway': ['#E12D39']}}
    volume2_chart_figure = {'data': [{'x': filtered_data['Date'],
                                      'y': filtered_data['Benzene'],
                                      'type': 'lines'}],
                            'layout': {'title': {'text': 'Benzene changes', 'x': 0.05, 'xanchor': 'left'},
                                       'xaxis': {'fixedrange': True},
                                       'yaxis': {'fixedrange': True}}}
    return price_chart_figure, volume_chart_figure, volume2_chart_figure


# run
if __name__ == '__main__':
    app.run_server(debug=True)

