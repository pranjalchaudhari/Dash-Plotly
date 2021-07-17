import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
import copy

df = pd.read_csv('data.csv', thousands=',')

unique_states = sorted(df['State'].unique())

max_population = df[['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']].max(axis=1).max()
min_population = df[['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']].min(axis=1).min()

state_dropdown_data = [{'label':'All','value':'All'}]
for state in unique_states:
    to_push = {'label':state,'value':state}
    state_dropdown_data.append(to_push)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

@app.callback(
    dash.dependencies.Output('results', 'children'),
    [dash.dependencies.Input('submit', 'n_clicks')],
    [dash.dependencies.State('year', 'value')],
    [dash.dependencies.State('state', 'value')],
    [dash.dependencies.State('population-slider', 'value')],
)
def generate_table(n_clicks,year,state,maxLimit):
    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update
    filtered_data = df.loc[df['State'].isin(state)]
    
    filtered_data = filtered_data.loc[filtered_data[year] <= maxLimit]

    filtered_data = filtered_data.filter(['City', 'State', year])
    filtered_data = filtered_data.sort_values([year],ascending = False)

    bar_chart_data = copy.deepcopy(filtered_data).head(20)

    return html.Div(children=[
            html.Div([
                html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in filtered_data.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(filtered_data.iloc[i][col]) for col in filtered_data.columns
                    ]) for i in range(len(filtered_data))
                ])
            ],
            style={"width":"100%"}
            )
        ],
        style={"width": "50%","display":"inline-block",'height': '300px', 'overflowY': 'auto'}
        ),
        dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': bar_chart_data['City'], 'y': bar_chart_data[year], 'type': 'bar', 'name': 'SF'}
            ],
            'layout': {
                'title': '20 most populated cities'
            }
        },
        style={"width": "50%","display":"inline-block"}
    )
    ],
    style={"vertical-align": "top","display": "flex"}
    )
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('population-slider', 'value')],
    [dash.dependencies.State('year', 'value')],
    [dash.dependencies.State('state', 'value')],
    )
def update_output(value,year,state):
    return 'Population limit: "{}"'.format(value)
app.layout = html.Div(children=[
    html.H5(children='What to expect?'),
    html.P(children='1. "All" filter in State dropdown works but takes enormus amount of time as the data is around 20,000 records. It takes 2+ mins approximately. Adding a state filter will give much faster results.'),
    html.P(children='2. For 1st search result, bar chart loads a little slow. It takes 5-10 sec approximately.'),
    html.P(children='3. As per my understanding, after every filter change (Year, State and Population), we need to hit the "Search" button to update the results.'),

    html.H4(children='Annual Estimates of the Resident Population for Incorporated Places in the United States: April 1, 2010 to July 1, 2019'),
    html.Div(
        [
            html.Label('Year'),
            dcc.Dropdown(
                id='year',
                options=[
                    {'label': '2010', 'value': '2010'},
                    {'label': '2011', 'value': '2011'},
                    {'label': '2012', 'value': '2012'},
                    {'label': '2013', 'value': '2013'},
                    {'label': '2014', 'value': '2014'},
                    {'label': '2015', 'value': '2015'},
                    {'label': '2016', 'value': '2016'},
                    {'label': '2017', 'value': '2017'},
                    {'label': '2018', 'value': '2018'},
                    {'label': '2019', 'value': '2019'},
                ],
                value='2019',
            )
        ],
        style={"width": "25%","display":"inline-block","margin-right":"10px"},
    ),
    html.Div(
        [
            html.Label('State'),
            dcc.Dropdown(
                id='state',
                options=state_dropdown_data,
                value=['All'],
                multi=True
            ),
        
        ],
        style={"width": "25%","display":"inline-block","margin-right":"10px"},
    ),
    html.Div(
        [
            html.Div(id='slider-output-container'),
            dcc.Slider(
                id='population-slider',
                min=min_population,
                max=max_population,
                value=max_population,
            ),
        ],
        style={"width": "25%","display":"inline-block","margin-left":"10px"},
    ),
    html.Div(
        [
            html.Button('Search', id='submit', n_clicks=0,style={"margin-top":"10px","background": "dodgerblue","color": "white"}),
        ],
    ),
    html.Div(id='results',children=[]),

])

if __name__ == '__main__':
    app.run_server(debug=True)
