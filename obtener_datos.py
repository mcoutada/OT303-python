"""
Este script se encargará de ejecutar las consultas SQL para extraer la información y guardarla en csv dentro de la carpeta files.
"""
import csv

from sqlalchemy import text

from conexion_db import get_engine
from config.logger_base import log

def extract_data():
    engine = get_engine()
    connection = engine.raw_connection()
    cursor = connection.cursor()

    # Ejecutando la consulta SQL de la Universidad de Moron.
    log.info('Obteniendo datos de la Universidad de Moron.')
    with open("sql\moron_nacional_pampa.sql") as file:
        query = file.read()
        cursor.execute(query)
    
    # Creando el archivo .csv
    log.info('Guardando los datos obtenidos.')
    with open('files/universidades.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(cursor) 
    
if __name__ == '__main__':
    extract_data()
