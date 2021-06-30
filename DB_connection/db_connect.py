# %%
import sys
sys.path.append('../')
import multiprocessing
from datetime import datetime
from functools import reduce

import pandas as pd
from tqdm import tqdm

from DB_connection import load_data
from DB_connection.mapping_dict import get_breed_dict
from DB_connection.mapping import *

dataconn = load_data.LoadData()

dataconn.show_db_version()
ShowDB_Df = dataconn.select_data(
    "show databases"
)
ShowDB_Df
# %%
Schema_all = ShowDB_Df.iloc[0:-5].values.tolist()
Schema_all = pd.Series(sum(Schema_all, []))

mapping_dict = get_breed_dict()
mapping_func = generate_mapping_function(mapping_dict)

# %%
Vital_df = pd.DataFrame()
results = None
def makeDf(Schema):
    dataconn = load_data.LoadData()
    tmp = dataconn.select_data(
        f"""select b.Name2, b.Name3, p.Sex,
            timestampdiff(month,p.BirthDate,v.VT_Date) as "_Month",
            timestampdiff(year,p.BirthDate,v.VT_Date) as "_Year", v.VT_BW
            from `{Schema}`.pet p, `{Schema}`.breed b, `{Schema}`.vital v
            where (p.breed = b.SNO and p.SNo = v.Pet_NO)"""
    )
    dataconn.close()
    return tmp
start = datetime.now()
print(start)
with multiprocessing.Pool()  as pool:
    results = list(pool.map(makeDf, Schema_all))
print(datetime.now() - start)

Vital_df = pd.concat(results)
Vital_df.to_pickle('../data/Vital.pkl')

# %%
# # %%
# Dx_df = pd.DataFrame()
# def makeDf(iter):
#     temp = dataconn.select_data(
#         "SELECT d.SNO, d.CODE, d.NAME_ENG, d.NAME_KOR, d.sInsCode, d.bInsur FROM `%s`.dx as d; " % iter
#         )
#     return temp

# tmp = list(map(lambda x : makeDf(x), tqdm(Schema_all)))
# Dx_df = pd.concat(tmp)


# %%
# # %%
# Vital_df = pd.DataFrame()
# for Schema in tqdm(Schema_all):
#     temp = dataconn.select_data(
#         "SELECT v.SNO, v.Pet_NO, v.VT_BW FROM `%s`.vital as v; " % Schema
#         )
#     Dx_df = pd.concat([Dx_df,temp])
# # %%
# Pet_df = pd.DataFrame()
# for Schema in tqdm(Schema_all):
#     temp = dataconn.select_data(
#         """SELECT p.SNO, p.Pet_No, p.Name, p.Breed, p.Species, p.Sex, p.BirthDate, p.Reg_Date, p.Last_Visit_Date,
#         p.Last_Status, p.Last_Status_Date, p.Insert_ID, p.Update_ID
#         FROM `%s`.pet as p; """ % Schema
#         )
#     Pet_df = pd.concat([Pet_df,temp])
# # %%
# Chart_df = pd.DataFrame()
# def makeDf(iter):
#     temp = dataconn.select_data(
#         """SELECT c.SNO, c.Pet_NO, c.Chart_Date, c.Class_Code
#         FROM `%s`.chartlist as c; """ % iter
#         )
#     return temp

# tmp = list(map(lambda x : makeDf(x), tqdm(Schema_all)))
# Chart_df = pd.concat(tmp)
# %%
Dog = pd.DataFrame()
results = None
def makeDf(Schema):
    dataconn = load_data.LoadData()
    tmp = dataconn.select_data(
        f"""select b.Name2,b.Name3 , p.Sex, diag.Diagnosis,
            timestampdiff(month,p.BirthDate, diag.Chart_Date) as "_Month",
            timestampdiff(year,p.BirthDate, diag.Chart_Date) as "_Year"
        From (SELECT c.Pet_No, c.Chart_Date, a.Diagnosis FROM `{Schema}`.chartlist as c
        Join `{Schema}`.assessment as a on c.SNO = a.Chart_No) as diag
        join `{Schema}`.pet as p on diag.Pet_No = p.SNO
        join `{Schema}`.breed as b on p.breed = b.SNO
        having `_Month` is not null;""")
    dataconn.close()
    return tmp
start = datetime.now()
print(start)
with multiprocessing.Pool()  as pool:
    results = list(pool.map(makeDf, Schema_all))
print(datetime.now() - start)
Dog = pd.concat(results)
Dog.to_pickle('../data/Diagnosis.pkl')

# %%
dataconn.close()

# %%
diag_dict = {
    "Maltese": ["구토", "소화", "장염", "외이", "내번", "유루", "개존", "슬개골", "허탈", "부신피질기능 저하증", "류마"],
    "Cocker Spaniel": ["백내장", "녹내장", "망막위축", '구토', '심비대', '피부', '외이'],
    "Bichon Frise": ["백내장", "슬개", "피부", '외이'],
    "Miniature Schnauzer": ["외이", "췌장", "결석"],
    "Poodle": ["구토", "소화", "장염", "외이", "내번", "유루", "개존", "슬개골", "허탈", "부신피질기능 저하증", "분리불안증"],
    "Pomeranian": ["식욕", "수두증", "허탈", "유루", "슬개골"],
    "Chihuahua": ["식욕", "난산", "수두증", "허탈", "녹내장", "특발성 발작", "슬개골"],
    "Shih Tzu": ["안검 내반", "망막박리", "단두", "슬개골"],
    "Yorkshire Terrier": ["구토", "설사", "수두증", "외이염", "슬개골", "판막"],
    "Golden Retriever": ["입질", "아토피", "습성", "고관절", "갑상선기능 저하증"]
}

full_diag_dict = {
    "Maltese": ["구토", "소화불량", "장염", "외이염", "안검내반증", "유루증", "동맥관개존증", "슬개골탈구", "기관허탈", "부신피질기능저하증", "류마티스염"],
    "Cocker Spaniel": ["백내장", "녹내장", "진행성망막위축증", "구토", "심장 비대증", "피부병", "외이염"],
    "Bichon Frise": ["백내장", "슬개골 탈구", "피부염", "외이염"],
    "Miniature Schnauzer": ["외이염", "췌장염", "결석,신장"],
    "Poodle": ["구토", "소화불량", "장염", "외이염", "안검내반증", "유루증", "동맥관개존증", "슬개골탈구", "기관허탈", "부신피질기능저하증", "분리불안증"],
    "Pomeranian": ["식욕 부진", "수두증", "기관 허탈", "유루증", "슬개골 질환"],
    "Chihuahua": ["식욕 부진", "난산", "수두증", "기관 허탈", "녹내장", "특발성 간질", "슬개골 질환"],
    "Shih Tzu": ["안검 내반증", "망막 박리", "단두종 증후군", "슬개골 탈구"],
    "Yorkshire Terrier": ["구토", "설사", "수두증", "외이염", "슬개골 탈구", "심장 판막증"],
    "Golden Retriever": ["입질", "아토피", "습성피부병", "고관절 탈구", "갑상선기능 저하증"]
}

# %%
with pd.ExcelWriter('../data/result.xlsx') as writer:
    for breed in tqdm(diag_dict.keys()):
        tmp_df = pd.DataFrame(columns=diag_dict[breed], index=range(0, 21, 1))
        for diag in diag_dict[breed]:
            for age in range(21):
                if age >= 20:
                    tmp_df[diag][age] = len(Dog.query(
                        f'Name == "{breed}" and Year >= {age} and Diagnosis.str.contains("{diag}")'))
                else:
                    tmp_df[diag][age] = len(Dog.query(
                        f'Name == "{breed}" and Year == {age} and Diagnosis.str.contains("{diag}")'))
        tmp_df.columns = full_diag_dict[breed]
        tmp_df.to_excel(writer, sheet_name=f'{breed}')
# %%
for idx, name in enumerate(full_diag_dict["Golden Retriever"]):
    print(idx, name)
# %%
Assessment = pd.DataFrame()
results = None
def makeDf(Schema):
    dataconn = load_data.LoadData()
    tmp = dataconn.select_data(
        f"""select Diagnosis from `{Schema}`.assessment""")
    dataconn.close()
    return tmp
start = datetime.now()
print(start)
with multiprocessing.Pool()  as pool:
    results = list(pool.map(makeDf, Schema_all))
print(datetime.now() - start)
Assessment = pd.concat(results)
Assessment.to_pickle('../data/Assessment.pkl')
# %%
