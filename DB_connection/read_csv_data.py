# %%
import sys
sys.path.append('../')
import pandas as pd
# %%
Vital = pd.read_csv('../data/Vital_named_diet.csv')
# %%
from matplotlib import pyplot as plt
# %%
plt.boxplot(Vital.query('Name == "Maltese"')['VT_BW'])
# %%
Vital_info = Vital.groupby('Name').describe()
# %%
Vital_info['VT_BW']
# %%
Vital.query('Sex == 6')
# %%
Vital['_Year'].describe()
# %%
Vital['Sex'].value_counts()
# %%
import numpy as np

def get_outlier(df=None, column=None, weight=1.5):
  # target 값과 상관관계가 높은 열을 우선적으로 진행
  quantile_25 = np.percentile(df[column].values, 25)
  quantile_75 = np.percentile(df[column].values, 75)

  IQR = quantile_75 - quantile_25
  IQR_weight = IQR*weight
  
  lowest = quantile_25 - IQR_weight
  highest = quantile_75 + IQR_weight
  
  outlier_idx = df[column][ (df[column] < lowest) | (df[column] > highest) ].index
  return outlier_idx
# %%
pom = Vital.query('Name == "Pomeranian"')
# %%
# 함수 사용해서 이상치 값 삭제
outlier_idx = get_outlier(df=pom, column='_Year', weight=1.5)
pom.drop(outlier_idx, axis=0, inplace=True)
