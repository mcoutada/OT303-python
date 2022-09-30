#COMO: Analista de datos
#QUIERO: Utilizar un operador creado por la comunidad
#PARA: poder subir el txt creado por el operador de Python al S3

#Criterios de aceptación:

#Tomar el .txt del repositorio base

#Buscar un operador creado por la comunidad que se adecue a los datos.

#Configurar el S3 Operator para la Universidad Tecnológica Nacional , universidad de tres de febrero

#Subir el archivo a S3



import logging
import os
import pandas as pd


from datetime import datetime

from config.cfg import LOG_ETL, ROOT_CSV, ROOT_SQL, ROOT_TXT, BUCKET_NAME, CONNECTION
from db.db_connection import create_engine_connection
from utils.utils import create_folder, create_txt, get_filename_path
from utils.transform import normalize_data

from airflow.hooks.S3_hook import S3Hook
import ntpath


log_name = LOG_ETL + datetime.today().strftime('%Y-%m-%d')
logger = logging.getLogger(log_name)


def extract_data():


    logger.info('task_extract')


    engine = create_engine_connection()

    sql_files = get_filename_path(ROOT_SQL)


    DATABASES = {
        'training': {
            'ENGINE': create_engine_connection(),
            'NAME': os.path.join(BASE_DIR, 'db.training'),
        }
    }
    with engine.connect() as connection:

        for sql_file_name, sql_full_path in sql_files.items():
            with open(sql_full_path) as f:

                query = f.read()
                logger.info('Extract data from {}'.format(sql_file_name))

                result = connection.execute(query)

                df = pd.DataFrame(result)
                logger.info('Writing information to csv.')

                df.to_csv(os.path.join(
                    ROOT_CSV, f'{sql_file_name[:-4]}.csv'), index=False)
    logger.info('Extract data from database.')


def transform_data():


    logger.info('task transform')

    create_folder(ROOT_TXT)

    csv_files = get_filename_path(ROOT_CSV)

    routes = []
    for csv_name, csv_path in csv_files.items():
        logger.info('Working on {} file.'.format(csv_name))

        dataframe = pd.read_csv(csv_path)

        logger.info('Normalize data on {} file.'.format(csv_name))
        dataframe = normalize_data(dataframe)

        logger.info('Creating a txt for {} file.'.format(csv_name))
        routes.append(create_txt(dataframe, csv_name[:-4]))
    logger.info('Transform data from dataframe/csv.')
    return routes


def load_data(routes):

    logger.info('task load')
    logger.info('Loading to S3.')


    hook = S3Hook(connect)

    for file in routes:

        try:
            logger.info(f'Uploading {key} to S3.')
            hook.load_file(filename=file, key=key,
                           bucket_name=BUCKET_NAME, replace=False,
                           acl_policy='public-read')
        except:
            logger.info(
                f'Key {key} already in use. Change the name of the file to force upload.')

            #en este codigo lo que realice fue utilizar parte del codigo ETL_PARA_UNIV de la task anterior
            # agrege las librerias para poder leer , normalizar y subir los datos a un bucket de s3