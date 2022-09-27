import pandas as pd
import psycopg2


def norm_universidades(path,name):
    univ_norm = pd.read_csv(path)

    univ_norm["university"]=univ_norm["university"].astype("str").str.lower()
    univ_norm["university"]=univ_norm["university"].replace(["_","-","\xa0\xa0"],"")

    univ_norm["career"]=univ_norm["career"].astype("str").str.lower().replace(["_","-","\xa0\xa0"],"")
    
    univ_norm["inscription_date"]=pd.to_datetime(univ_norm["inscription_date"],format='%d/%m/%Y').astype("str")

    univ_norm["first_name"]=univ_norm["first_name"].astype("str").str.lower().replace(["_","-","\xa0\xa0","\xa0"],"")
    univ_norm["last_name"]=univ_norm["last_name"].astype("str").str.lower().replace(["_","-","\xa0\xa0","\xa0"],"")
   
    univ_norm["gender"]=univ_norm["gender"].astype("str").replace(["M"],"male")
    univ_norm["gender"]=univ_norm["gender"].astype("str").replace(["F"],"female")
    
    univ_norm["age"]=univ_norm["age"].astype("int")
    univ_norm["postal_code"]=univ_norm["postal_code"].astype("str")
    univ_norm["location"]=univ_norm["location"].astype("str").str.lower().replace(["_","-","\xa0\xa0"],"")
    univ_norm["email"]=univ_norm["email"].astype("str").str.lower().replace(["\xa0"],"")
    univ_norm.to_csv(name+".csv",header=True,index=False)
