# %%
import os
import sys

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

sys.path.append('../')
os.chdir('/home/kimjunho/문서/DB_data')

Diagnosis = pd.read_csv(os.getcwd()+'/data/Diagnosis_named.csv')
Vital = pd.read_csv(os.getcwd()+'/data/Vital_named_cleaned.csv')
# %%
# breed = None
# Vital = Vital.query('not (VT_BW <= 1 and _Month > 12)')
# Vital = Vital.query('not (VT_BW <= 0.1 and _Month > 1)')
# %%
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div(children=[
        html.Div(children=[
            html.H2('질병 통계'),
            dcc.Dropdown(
                id='breed',
                options=[{'label': i, 'value': i}
                         for i in Diagnosis['Name'].unique()],
                placeholder='견종을 선택하세요... (미 선택 시 견종 구분 없이 전체 통계)'
            ),
            dcc.Dropdown(
                id='sex',
                options=[
                    {'label': '남자', 'value': 1},
                    {'label': '여자', 'value': 2},
                    {'label': '중성화 남자', 'value': 3},
                    {'label': '중성화 여자', 'value': 4}
                ],
                placeholder='성별을 선택하세요... (미 선택 시 성별 구분 없이 전체 통계)'

            ),
            dcc.Dropdown(id='year',
                         placeholder='나이를 선택하세요... (미 선택 시 나이 구분 없이 전체 통계)'),
        ],
            style={'width': '33%',
                   'display': 'inline-block',
                   'float': 'left'}),

        html.Div(children=[
            dcc.Graph(id='sex_ratio', style={'display': 'none'}),
            dcc.Graph(id='year_ratio', style={'display': 'none'})
        ],
            style={'width': '66%',
                   'display': 'inline-block',
                   'float': 'left'})
    ], style={'width': '100%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Loading(id='loading',
                    children=[
                        dcc.Store(id='result-value'),
                        html.Div([
                            html.Div(
                                children=[
                                    dt.DataTable(
                                        id='result-table',
                                        columns=[{'name': i, "id": i}
                                                 for i in ["Diagnosis", "Counts", "%"]],
                                        style_table={'minwidth': '43.5%', },
                                        style_cell={'maxWidth': 0, },
                                    ),
                                ],
                                style={'width': '30%',
                                       'display': 'inline-block',
                                       'float': 'left'}
                            ),
                            html.Div(
                                children=[
                                    dcc.Graph(id='result-graph'),
                                    dcc.Graph(id='diagnosis-year'),
                                ],
                                style={'width': '70%',
                                       'display': 'inline-block',
                                       'float': 'left'}
                            ),
                        ], style={'width': '100%', 'display': 'inline-block'}),

                    ],
                    type="circle",),
    ],),
    dcc.Graph(id='vital-graph',
              figure=px.scatter(Vital.groupby(['Name', '_Month'], as_index=False).mean(), x = "_Month", y="VT_BW", color="Name", title='월별 몸무게 평균')),
    dcc.Graph(id='vital-describe',
              figure=px.bar(Vital.groupby(['Name', 'Sex'], as_index=False).mean(), y = 'VT_BW', color='Name', hover_name='Sex', title = '성별 몸무게 평균'))
])
# %%

# @app.callback(
#     Output('vital-graph', 'figure'),
#     Input('breed', 'value')
# )
# def update_vital_df(breed):
#     return px.scatter(Vital.groupby(['Name', 'Sex', '_Month'], as_index=False).mean(), x = "_Month", y="VT_BW", color="Name", hover_name='Sex')
    
    

@app.callback(
    dash.dependencies.Output('year', 'options'),
    dash.dependencies.Output('year', 'value'),
    [dash.dependencies.Input('breed', 'value')])
def update_year_dropdown(value):
    options = [
        {'label': i, 'value': i}
        for i in sorted(Diagnosis.query(f'Name == "{value}"')['_Year'].unique())
    ]
    return options, None


@app.callback(
    Output('result-table', 'data'),
    Input('result-value', 'data')
)
def update_table(result_value):
    return result_value


@app.callback(
    Output('result-graph', 'figure'),
    Input('result-value', 'data')
)
def update_graph(result_value):
    if len(result_value) == 0:
        return px.bar()
    return px.bar(result_value, x='Diagnosis', y='%', title=f'상위 {len(result_value)}개의 질병')


@app.callback(
    Output('year_ratio', 'figure'),
    Output('year_ratio', 'style'),
    Input('breed', 'value'),
    Input('sex', 'value'),
)
def update_year_ratio_graph(breed, sex):
    if sex is not None:
        sex_label = {1: '남자', 2: '여자', 3: '중성화 남자', 4: '중성화 여자'}[sex]
    display = {'width': '70%', 'display': 'inline-block', 'float': 'left'}
    

    if breed is not None and sex is None:
        year_count = Diagnosis.query(f'Name == "{breed}"').groupby([
            '_Year']).count()['Name']
        return px.bar(year_count, title=f'{breed} 나이 분포', height=300), display
    elif breed is None and sex is not None:
        year_count = Diagnosis.query(f'Sex == {sex}').groupby([
            '_Year']).count()['Name']
        return px.bar(year_count, title=f'{sex_label}의 나이 분포', height=300), display
    elif breed is not None and sex is not None:
        year_count = Diagnosis.query(f'Name == "{breed}" and Sex == {sex}').groupby([
            '_Year']).count()['Name']
        return px.bar(year_count, title=f'{breed} - {sex_label}의 나이 분포', height=300), display
    else:
        year_count = Diagnosis.groupby(['_Year']).count()['Name']
        return px.bar(year_count, title='나이 분포', height=300), display
    


@app.callback(
    Output('sex_ratio', 'figure'),
    Output('sex_ratio', 'style'),
    Input('breed', 'value'),
    Input('year', 'value')
)
def update_sex_ratio_graph(breed, year):
    display = {'width': '30%', 'display': 'inline-block', 'float': 'left'}
    if breed is not None and year is None:
        sex_count = Diagnosis.query(f'Name == "{breed}"').groupby([
            'Sex']).count()['Name']
        return px.pie(names=sex_count.index, values=sex_count, title=f'{breed} 성별 분포', height=300), display
    elif breed is None and year is not None:
        sex_count = Diagnosis.query(f'_Year == {year}').groupby([
            'Sex']).count()['Name']
        return px.pie(names=sex_count.index, values=sex_count, title=f'{year}살 성별 분포', height=300), display
    elif breed is not None and year is not None:
        sex_count = Diagnosis.query(f'Name == "{breed}" and _Year == {year}').groupby([
            'Sex']).count()['Name']
        return px.pie(names=sex_count.index, values=sex_count, title=f'{year}살 {breed} 성별 분포', height=300), display
    else :
        sex_count = Diagnosis.groupby(['Sex']).count()['Name']
        return px.pie(names=sex_count.index, values=sex_count, title=f'성별 분포', height=300), display
    


@app.callback(
    Output('diagnosis-year', 'figure'),
    Output('result-table', 'active_cell'),
    dash.dependencies.Input('breed', 'value'),
    dash.dependencies.Input('sex', 'value'),
    [dash.dependencies.Input('result-table', 'active_cell'),
     dash.dependencies.Input('result-table', 'data')]
)
def update_diagnosis_year_graph(breed, sex, active_cell, data):
    diagnosis = data[active_cell['row']
                     ]['Diagnosis'] if data and active_cell else None
    if diagnosis is None:
        return px.line(), None

    if breed is not None and sex is not None:
        d = Diagnosis.query(f'Name == "{breed}" and Sex == {sex} and Diagnosis == "{diagnosis}"').groupby(
            ['_Year'], as_index=False).count()[['_Year', 'Diagnosis']]
    elif breed is not None and sex is None:
        d = Diagnosis.query(f'Name == "{breed}" and Diagnosis == "{diagnosis}"').groupby(
            ['_Year'], as_index=False).count()[['_Year', 'Diagnosis']]
    elif breed is None and sex is not None:
        d = Diagnosis.query(f'Sex == {sex} and Diagnosis == "{diagnosis}"').groupby(
            ['Name', '_Year', ], as_index=False).count()[['Name', '_Year', 'Diagnosis']]
        return px.line(d, x='_Year', y='Diagnosis', color='Name', title=f'성별에 따른 {diagnosis}'), None
    d.rename(columns={'Diagnosis': 'Count'}, inplace=True)
    return px.line(d, x='_Year', y='Count', title=f'{breed} - {diagnosis}'), None


# %%
@app.callback(
    dash.dependencies.Output('result-value', 'data'),
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

# %%
if __name__ == '__main__':
    app.run_server(debug=True, port=8088, host='0.0.0.0')
# %%
