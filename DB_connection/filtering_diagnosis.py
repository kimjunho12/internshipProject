# %%
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append('../')


pd.set_option('float_format', '{:.2f}'.format)

# %%
Diagnosis = pd.read_csv('../data/Diagnosis_named.csv')
# %%
# Diagnosis = Diagnosis[(Diagnosis['VT_BW'] > 0) & (Diagnosis['VT_BW'] < 50)]
# %%
Diagnosis = Diagnosis[(Diagnosis['Sex'] > 0) & (Diagnosis['Sex'] < 5)]
# %%
Diagnosis = Diagnosis[(Diagnosis['_Month'] > 0) & (Diagnosis['_Month'] < 480)]
# %%
# Diagnosis['Sex'] = Diagnosis['Sex'].astype('category')
# %%
Diagnosis.groupby('Name').describe()
# %%
Diagnosis.to_csv('../data/Diagnosis_named.csv', index=False)
# %%


def get_outlier(df=None, column=None, weight=1.5):
    # target 값과 상관관계가 높은 열을 우선적으로 진행
    quantile_25 = np.percentile(df[column].values, 25)
    quantile_75 = np.percentile(df[column].values, 75)

    IQR = quantile_75 - quantile_25
    IQR_weight = IQR*weight

    lowest = quantile_25 - IQR_weight
    highest = quantile_75 + IQR_weight

    outlier = df[column][(df[column] < lowest) | (df[column] > highest)]
    return outlier


# %%
breed_list = Diagnosis['Name'].unique()
# %%
for x in tqdm(breed_list):
    globals()[f"{x}_df"] = Diagnosis.query(f'Name == "{x}"')
columns = ['_Month']
# %%
with pd.ExcelWriter('../data/Diagnosis_info.xlsx') as writer:
    for b in tqdm(breed_list):
        for c in columns:
            outlier = get_outlier(df=globals()[f"{b}_df"], column=c, weight=1.5)
            outlier_idx = outlier.index
            globals()[f"{b}_df"].drop(outlier_idx, axis=0, inplace=True)
        globals()[f"{b}_df"].describe().to_excel(writer, sheet_name = b)
# %%
# %%
for b in breed_list:
    plt.scatter(globals()[f"{b}_df"].groupby('_Month').mean()['VT_BW'].index, globals()[f"{b}_df"].groupby('_Month').mean()['VT_BW'].values)
# %%
dd = Diagnosis.groupby(["Name","Sex","_Year","Diagnosis"]).count()
# %%
d = Diagnosis.groupby(["Name","Sex","_Year","Diagnosis"], as_index=False)[['_Month']].count()
d.rename(columns = {"_Month":"Count"},inplace=True)
# %%
with pd.ExcelWriter('../data/Diagnosis_Count.xlsx') as writer:
    for b in tqdm(breed_list):
        d.query(f'Name == "{b}"').to_excel(writer, sheet_name=b)
# %%

# %%
while True:
    b = input("종을 입력하세요 : ")
    if b == 'x':
        break
    s = input("성별을 입력하세요 : ")
    y = input("나이를 입력하세요 : ")
    result = Diagnosis.query(f'Name == "{b}" and Sex == {s} and _Year == {y}')['Diagnosis'].value_counts()
    print((result / result.sum() * 100).head(10))
# %%
# %%
