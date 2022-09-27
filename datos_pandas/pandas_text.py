import pandas as pd
import os
import numpy as np
def create_txt(df:pd.DataFrame , file_name:str):

    path= os.path.join(__path,file_name+'.txt')
    text_file=df.to_csv(path , index=False)

    log.info('Save txt.')
    df_file = open('files/universidades D.txt', 'D')
    df_file.write(df.to_string())
    df_file.close()


    return text_file

#importo las librerias correspondientes para usar la operacion
#creo el archivo txt
#guardo el archivo txt
# lo devuelvo con el return