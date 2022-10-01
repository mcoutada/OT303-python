"""
Esta funcion se va a encargar de normalizar los datos extraidos
usando la libreria de pandas y creando un archivo .txt que se 
encontrará en la carpeta files.
"""
import pandas as pd

from obtener_datos import extract_data
from config.logger_base import log

def transform_data():
    log.info('Extrayendo datos.')
    df = extract_data()

    log.info('Normalizando los datos.')
    # Normalizando la columna university
    df.university = df.university.str.replace('-',' ')
    df.university = df.university.str.lower()

    # Normalizando la columna career
    df.career = df.career.str.replace('-', ' ')
    df.career = df.career.str.lower()

    # Normalizando la columna inscription_date
    df.inscription_date = pd.to_datetime(df.inscription_date)

    # Normalizando las columnas first_name y last_name
    df.first_name = df.first_name.str.lower()
    df.last_name = df.last_name.str.lower()

    # Normalizando la columna gender
    df.gender = df.gender.map({'F': 'female', 'M': 'male'})

    # Normalizando la columna age
    df.age = df.age.astype('int64')

    # Normalizando la columna location
    df.location = df.location.str.lower()
    
    # Normalizando la columna email
    df.email = df.email.str.lower()

    print(df)

    # Filtrando la columna university para crear dos dataframes nuevos
    df_moron = df[(df.university == 'universidad de morón') | (df.university == 'universidad nacional de la pampa')]
    df_rio = df[(df.university == 'universidad nacional de río cuarto') | (df.university == 'universidad abierta interamericana')]
    
    # Guardando los datos en un archivo .txt
    log.info('Guardando los datos normalizados de la Universidad de Moron en un archivo txt.')
    df_file = open('Sprint2/files/universidad_moron.txt', 'a')
    df_file.write(df_moron.to_string())
    df_file.close()

    log.info('Guardando los datos normalizados de la Universidad de Río Cuarto en un archivo txt.')
    df_file = open('Sprint2/files/universidad_rio.txt', 'a')
    df_file.write(df_rio.to_string())
    df_file.close()

if __name__ == '__main__':
    transform_data()