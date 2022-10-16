import pandas as pd
import sys
import os
import re
from datetime import datetime

score_time=open(f"Score_time_mapped.txt","r")

# Reducer 3 
# Del ranking de los primeros 0-100 por score tomar el tiempo de respuesta promedio 
# informar un único valor

questions_id=[]
questions_dates=[]

answers_parentid=[]
answers_date=[]
answers_score=[]

def date_normalization(date):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')

for line in score_time:
    line=line.strip()
    line=line.split(",")
    try:
        if int(line[1])==2:
            pass
            # TEST print(line[4],line[2],line[3]) # ParentId, date and score if post is type 2
            answers_parentid.append(int(line[4]))
            answers_date.append(date_normalization(line[2]))
            answers_score.append(int(line[3]))
        else:
            # TEST print(line[0],line[2]) #Id and Date if post is type 1
            questions_id.append(int(line[0]))
            questions_dates.append(date_normalization(line[2]))
    except:
        pass

df_questions=pd.DataFrame(columns=["Id","Date"],index=None)
df_questions["Id"]=questions_id
df_questions["Date"]=questions_dates

df_answers=pd.DataFrame(columns=["Id","Date_new","Score"],index=None)
df_answers["Id"]=answers_parentid
df_answers["Date_new"]=answers_date
df_answers["Score"]=answers_score

top_100 = df_answers.sort_values('Score',ascending=False).head(100)

inner_joined = pd.merge(df_questions,top_100,on=["Id"],how="inner")

inner_joined.sort_values('Score',ascending=False)

with open("average_time.txt","w") as VA:
    VA.write("{}".format(pd.DataFrame.mean(inner_joined["Date_new"]-inner_joined["Date"])))
