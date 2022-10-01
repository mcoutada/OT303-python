"""
Este script se encargará de ejecutar las consultas SQL para extraer la información y guardarla en csv dentro de la carpeta files.
"""
import pandas as pd

from Sprint2.conexion_db import get_engine
from config.logger_base import log

def extract_data():
    engine = get_engine()
    connection = engine.raw_connection()

    # Ejecutando la consulta SQL para la Universidad de Moron.
    log.info('Obteniendo datos de la Universidad de Moron.')
    with open("sql\moron_nacional_pampa.sql") as file:
        query = file.read()
        table_df = pd.read_sql(query, connection)
    
    # Ejecutando la consulta SQL para la Universidad Nacional del Rio Cuarto.
    log.info('Obteniendo datos de la Universidad Nacional del Rio Cuarto.')
    with open("sql/rio_cuarto_interamericana.sql") as file:
        query = file.read()
        table_df = table_df.append(pd.read_sql(query, connection), ignore_index = True)
    
    # Guardando los datos en el archivo .csv
    log.info('Guardando los datos obtenidos.')
    table_df.to_csv(path_or_buf = 'files/universidades.csv')
    
    log.info('Se han guardado todos los datos correctamente.')
    
    """
    Se retorna el df de las universidades 
    para usarlo y normalizar los datos
    sin necesidad de cargar el csv.
    """
    return table_df
    
if __name__ == '__main__':
    extract_data()
