import sys
import os
import re
from datetime import datetime
import pandas as pd

# Reducer 1
# Top 10 fechas con mayor cantidad de post creados

def conv_datetime(date):
    conv =  datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d')
    return conv

def conv_just_date(date):
    conv = datetime.strptime(date,'%Y-%m-%d')
    return conv

file1 = open(f"newfile_mapped.txt","r")
fechas=[]
for line in file1:
    line = line.strip()
    line = line.split(" ")
    try: 
        date = conv_datetime(line[1])
        date = conv_just_date(date)
        fechas.append(date)
    except:
        pass
df_fechas=pd.DataFrame(columns=["fechas"])
df_fechas["fechas"]=df_fechas["fechas"].append(pd.Series(fechas))

tabla_conteo=df_fechas["fechas"].value_counts().rename_axis("registros").reset_index(name='cantidad')
tabla10=tabla_conteo.head(10)
tabla10.to_csv("posts_by_date.txt",header=None, index=None, sep=' ',mode='a')
