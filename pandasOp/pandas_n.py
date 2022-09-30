import pandas as pd
import os
import numpy as np
import io

#normalizacion de datos con pandas 

def normalize_data (df: pd.DataFrame):

   df= pd.read_sql_query(sql)

univ_n["university"]=univ_n["university"].astype("str").str.lower()
univ_n["university"] = univ_n["university"].replace(["_","-",","])

univ_n["career"]=univ_n["career"].astype("str").str.lower().replace(["_","-",","])
univ_n["career"]=univ_n["career"].astype("str").str.lower()

univ_n['inscription_date'] = pd.to_datetime(df['inscription_date'])
univ_n['inscription_date'] = df['inscription_date'].dt.strftime('%Y-%m-%d')

univ_n['first_name'] = df['first_name'].str.lower()
univ_n['first_name'] = df['first_name'].replace(["_","-",","])


univ_n['last_name'] = df['last_name'].str.lower()
univ_n['last_name'] = df['last_name'].replace(["_","-",","])


univ_n['gender'] = df['gender'].replace(['F', 'M'], ['female', 'male'])

univ_n['age'] = df['age'].astype(dtype=np.int16)

univ_n['postal_code'] = df['postal_code'].astype('str')

univ_n['location'] = df['location'].str.lower()
univ_N['location'] = df['location'].replace(["_","-",","])


df['email'] = df['email'].str.lower()
df['email'] = df['email'].replace(["-",","])




