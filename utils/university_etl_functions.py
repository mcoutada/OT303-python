
import logging
import os
import pandas as pd
# Use ntpath instead os.path.basename(__path__). It works in linux and windows.
import ntpath

from datetime import datetime

from config.cfg import LOG_ETL, ROOT_CSV, ROOT_SQL, ROOT_TXT, BUCKET_NAME, CONNECTION
from db.db_connection import create_engine_connection
from utils.utils import create_folder, create_txt, get_filename_path
from utils.transform import normalize_data

from airflow.hooks.S3_hook import S3Hook


# Use log created before.
log_name = LOG_ETL + datetime.today().strftime('%Y-%m-%d')
logger = logging.getLogger(log_name)


def extract_data():
    """Get data from both universities. TASK OT303-45
    """
    logger.info('*-----------EXTRACT TASK-----------*')
    # First create csv folder if doesn't exist.
    create_folder(ROOT_CSV)
    # Create engine
    engine = create_engine_connection()
    # Get sql files and full path.
    sql_files = get_filename_path(ROOT_SQL)
    # Connect engine.
    with engine.connect() as connection:
        # Execute each query and create a .csv
        for sql_file_name, sql_full_path in sql_files.items():
            with open(sql_full_path) as f:
                # Read the query.
                query = f.read()
                logger.info('Extracting data from {}'.format(sql_file_name))
                # Execute query.
                result = connection.execute(query)
                # Create a pandas dataframe with the result.
                df = pd.DataFrame(result)
                logger.info('Writing information to csv.')
                # Create .csv file. The name is the same as .sql filename.
                df.to_csv(os.path.join(
                    ROOT_CSV, f'{sql_file_name[:-4]}.csv'), index=False)
    logger.info('Extracting data from database.')


def transform_data():
    """Transform data for both universities. TASK OT303-53

    Returns:
        routes (array[str]): routes to the .txt generated.
    """
    logger.info('*-----------TRANSFORM TASK-----------*')
    # First create txt folder if doesn't exist.
    create_folder(ROOT_TXT)
    # Get csv files and full path.
    csv_files = get_filename_path(ROOT_CSV)
    # Define array with routes.
    routes = []
    for csv_name, csv_path in csv_files.items():
        logger.info('Working on {} file.'.format(csv_name))
        # Read csv file and create dataframe.
        dataframe = pd.read_csv(csv_path)
        # Normalize data.
        logger.info('Clearing data on {} file.'.format(csv_name))
        dataframe = normalize_data(dataframe)
        # Create the txt file to save the changes.
        logger.info('Creating txt for {} file.'.format(csv_name))
        routes.append(create_txt(dataframe, csv_name[:-4]))
    logger.info('Transform data from dataframe/csv.')
    return routes


def load_data(routes):
    """Upload data for both universities to S3. TASK OT303-69 and TASK OT303-70

    Args:
        routes ([str]): array with files path to upload.
    """
    logger.info('*-----------LOAD TASK-----------*')
    logger.info('Loading data to S3.')

    # CONNECTION is the name of the connection defined in airflow.
    hook = S3Hook(CONNECTION)

    for file in routes:
        # Use the basepath as key.
        key = ntpath.basename(file)
        # Upload.
        try:
            logger.info(f'Uploading {key} to S3.')
            hook.load_file(filename=file, key=key,
                           bucket_name=BUCKET_NAME, replace=False,
                           acl_policy='public-read')
        except:
            logger.info(
                f'Key {key} already in use. Change the name of the file to force upload.')
