# %%
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append('../')


pd.set_option('float_format', '{:.2f}'.format)

# %%
Vital = pd.read_csv('../data/Vital_named.csv').iloc[:,1:]
# %%
Vital = Vital[(Vital['VT_BW'] > 0) & (Vital['VT_BW'] < 50)]
# %%
Vital = Vital[(Vital['Sex'] > 0) & (Vital['Sex'] < 5)]
# %%
Vital = Vital[(Vital['_Month'] >= 0) & (Vital['_Month'] < 480)]
Vital = Vital.query('not (VT_BW <= 1 and _Month > 12)')
Vital = Vital.query('not (VT_BW <= 0.1 and _Month > 2)')
# %%
# Diagnosis['Sex'] = Diagnosis['Sex'].astype('category')
# %%
Vital.groupby('Name').describe()
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
breed_list = Vital['Name'].unique()
# %%
for x in tqdm(breed_list):
    globals()[f"{x}_df"] = Vital.query(f'Name == "{x}"')
columns = ['_Month', 'VT_BW']
# %%
for x in tqdm(breed_list):
    for m in globals()[f"{x}_df"]['_Month'].astype(int).unique():
        globals()[f"{x}_{m}_df"] = globals()[f"{x}_df"].query(f'_Month == {m}')
# %%
new_df_list = []
for b in tqdm(breed_list):
    for m in globals()[f"{b}_df"]['_Month'].astype(int).unique():
        outlier = get_outlier(df=globals()[f"{b}_{m}_df"], column='VT_BW', weight=1.5)
        outlier_idx = outlier.index
        new_df_list.append(globals()[f"{b}_{m}_df"].drop(outlier_idx, axis=0))
# %%
Vital_cleaned = pd.concat(new_df_list)
Vital_cleaned.groupby('Name').describe()
# %%
Vital_cleaned.to_csv('../data/Vital_named_cleaned.csv', index=False)