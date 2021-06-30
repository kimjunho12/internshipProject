import pymysql
import pymysql.cursors
import pandas as pd


_breed_list = None

def get_connection():
    connection = pymysql.connect(host='192.168.1.241', 
                                user='intoai', 
                                password='intoai66!', 
                                database='intoai', 
                                cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_breed_dict():
    global _breed_list
    if _breed_list == None:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT `breed`, `text` from `BREED_MAP`"
                cursor.execute(sql)
                _breed_list = cursor.fetchall()

    df = pd.DataFrame(_breed_list)
    breeds = df["breed"].unique()
    mapping_dict = dict()
    for key in breeds:
        value = set(df["text"][df["breed"] == key].to_list())
        mapping_dict[key] = value
    return mapping_dict

if __name__ == "__main__":
    print(get_breed_dict())
