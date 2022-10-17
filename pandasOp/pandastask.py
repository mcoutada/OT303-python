import pandas as pd
import os
import numpy as np
import io


# normalizacion de datos con pandas

def normalize_data(df: pd.DataFrame):
    df = pd.read_sql_query(sql)


univ_n["university"] = univ_n["university"].astype("str").str.lower()
univ_n["university"] = univ_n["university"].replace(["_", "-", ","])

univ_n["career"] = univ_n["career"].astype("str").str.lower().replace(["_", "-", ","])
univ_n["career"] = univ_n["career"].astype("str").str.lower()

univ_n['inscription_date'] = pd.to_datetime(df['inscription_date'])
univ_n['inscription_date'] = df['inscription_date'].dt.strftime('%Y-%m-%d')

univ_n['first_name'] = df['first_name'].str.lower()
univ_n['first_name'] = df['first_name'].replace(["_", "-", ","])

univ_n['last_name'] = df['last_name'].str.lower()
univ_n['last_name'] = df['last_name'].replace(["_", "-", ","])

univ_n['gender'] = df['gender'].replace(['F', 'M'], ['female', 'male'])

univ_n['age'] = df['age'].astype(dtype=np.int16)

univ_n['postal_code'] = df['postal_code'].astype('str')

univ_n['location'] = df['location'].str.lower()
univ_N['location'] = df['location'].replace(["_", "-", ","])

df['email'] = df['email'].str.lower()
df['email'] = df['email'].replace(["-", ","])

#creo un txt trabajando sobre el dataframe y que me devuelva un archivo txt

def create_txt(df: pd.DataFrame, file_name: str):
    path = os.path.join(__path, file_name + '.txt')

    text_file = df.to_csv(path, index=False)

    return text_file


jujuy_utn_df = pd.read_csv('UTN .csv')
jujuy_utn_df = normalize_data('UTN .csv')

create_txt(jujuy_utn_df, "universidad tecnologica nacional")
df.show()

tres_de_febrero_df = pd.read_csv('universidad de tres de febrero result')
tres_de_febrero_df = normalize_data('universidad de tres de febrero result')
df.show()

create_txt(tres_de_febrero_df, "universidad tres de febrero")

#proceso comppleto de lectura de csv y extraccion-transformacion a txt
