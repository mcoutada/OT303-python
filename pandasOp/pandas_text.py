import pandas as pd
import os
import numpy as np
def create_txt(df:pd.DataFrame , file_name:str):

    path= os.path.join(__path,file_name+'.txt')
    text_file=df.to_csv(path , index=False)

    return text_file

#importo las librerias correspondientes para usar la operacion
#creo el archivo txt
# lo devuelvo con el return