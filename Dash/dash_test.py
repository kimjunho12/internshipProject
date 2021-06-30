# %%
import os
import sys
import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
from dash.dependencies import Input, Output
from dash_core_components.Dropdown import Dropdown

sys.path.append('../')
# %%
os.chdir('/home/kimjunho/문서/DB_data')
# %%
Diagnosis = pd.read_csv(os.getcwd()+'/data/Diagnosis_named.csv')
# %%
breed = None
# %%
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H4('질병 통계'),

    dcc.Dropdown(
        id='breed',
        options=[{'label': i, 'value': i}
                 for i in Diagnosis['Name'].unique()],
        style={'width': '66%'}
    ),
    dcc.Dropdown(
        id='sex',
        options=[
            {'label': '남자', 'value': 1},
            {'label': '여자', 'value': 2},
            {'label': '중성화 남자', 'value': 3},
            {'label': '중성화 여자', 'value': 4}
        ],
        style={'width': '66%'}

    ),

    dcc.Dropdown(
        id='year',
        style={'width': '66%'}

    ),

    html.Div(id='selected'),
    html.Div([
        dcc.Loading(id='loading',
                    children=[html.Div([html.Div(id='loading-output')])],
                    type="circle",),
        dt.DataTable(id='result-table',
                     columns=[{'name': i, "id": i}
                              for i in ["Diagnosis", "Counts", "%"]],
                     style_table={
                         'width': '30%',
                     },
                     style_cell={
                         'maxWidth': 0,
                     }
                     ), ])
])
# %%


@app.callback(Output("loading-output", "children"), Input("selected", "children"))
def input_triggers_spinner(value):
    time.sleep(3)
    return value


@app.callback(
    dash.dependencies.Output('year', 'options'),
    [dash.dependencies.Input('breed', 'value')])
def update_year_dropdown(value):
    options = [
        {'label': i, 'value': i}
        for i in sorted(Diagnosis.query(f'Name == "{value}"')['_Year'].unique())
    ]
    return options
# %%


@app.callback(
    dash.dependencies.Output('result-table', 'data'),
    dash.dependencies.Input('breed', 'value'),
    dash.dependencies.Input('sex', 'value'),
    dash.dependencies.Input('year', 'value'),
)
def update_result(breed, sex, year):
    if (breed != None) and (sex == None) and (year == None):
        result = Diagnosis.query(f'Name == "{breed}"')[
            'Diagnosis'].value_counts().reset_index()
    elif (breed == None) and (sex != None) and (year == None):
        result = Diagnosis.query(f'Sex == {sex}')[
            'Diagnosis'].value_counts().reset_index()
    elif (breed == None) and (sex == None) and (year != None):
        result = Diagnosis.query(f'_Year == {year}')[
            'Diagnosis'].value_counts().reset_index()
    elif breed == None:
        result = Diagnosis.query(
            f'Sex == {sex} and _Year == {year}')['Diagnosis'].value_counts().reset_index()
    elif sex == None:
        result = Diagnosis.query(
            f'Name == "{breed}" and _Year == {year}')['Diagnosis'].value_counts().reset_index()
    elif year == None:
        result = Diagnosis.query(
            f'Name == "{breed}" and Sex == {sex}')['Diagnosis'].value_counts().reset_index()
    else:
        result = Diagnosis.query(
            f'Name == "{breed}" and Sex == {sex} and _Year == {year}')['Diagnosis'].value_counts().reset_index()
    result.columns = ["Diagnosis", "Counts"]
    result['%'] = [round(x/result['Counts'].sum()*100, ndigits=2)
                   for x in result['Counts']]
    return result.head(30).to_dict(orient='records')



@app.callback(
    dash.dependencies.Output('selected', 'children'),
    dash.dependencies.Input('breed', 'value'),
    dash.dependencies.Input('sex', 'value'),
    dash.dependencies.Input('year', 'value'),
)
def update_selected(breed, sex, year):
    return f'breed : {breed} | sex : {sex} | year : {year} is selected'


# %%
if __name__ == '__main__':
    app.run_server(debug=True, port=8088, host='0.0.0.0')
# %%
