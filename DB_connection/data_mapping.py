# %%
import sys
sys.path.append('../')
# %%
from DB_connection.mapping import generate_mapping_function
from DB_connection.mapping_dict import get_breed_dict
import pandas as pd
from tqdm import tqdm
# %%
Diagnosis_df = pd.read_pickle('../data/Diagnosis.pkl')
# %%
mapping_dict = get_breed_dict()
# def serial_contain_check(row, container):
#     return row["Name2"] in container or row["Name3"] in container
# mapping_func = generate_mapping_function(mapping_dict, contain=serial_contain_check)
mapping_func = generate_mapping_function(mapping_dict)
# %%
input_list = Diagnosis_df['Name2']
mapped_list = list(map(mapping_func, tqdm(input_list)))
Diagnosis_df['Name'] = mapped_list
# %%
input_list = Diagnosis_df['Name3']
mapped_list = list(map(mapping_func, tqdm(input_list)))
Diagnosis_df['Name_ko'] = mapped_list

# %%
def merge_name(row):
    if row['Name'] == "Unknown" and row['Name_ko'] != "Unknown":
        row['Name'] = row['Name_ko']
    return row['Name']
# %%
Diagnosis_df['Name'] = Diagnosis_df.apply(lambda x : merge_name(x), axis = 1)
# %%
Diagnosis_df.query('Name == "Unknown" and Name_ko == "Unknown"')

# %%
Diagnosis_df = Diagnosis_df.query('Name != "Unknown"')[['Name', 'Sex', '_Month', '_Year', 'Diagnosis']]
Diagnosis_df.to_csv('../data/Diagnosis_named.csv', index = False)
# %%
