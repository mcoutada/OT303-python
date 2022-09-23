
import logging
import os
import pandas as pd
from datetime import datetime

from config.cfg import LOG_ETL, ROOT_CSV, ROOT_SQL, ROOT_TXT
from db.db_connection import create_engine_connection
from utils.utils import create_folder, create_txt, get_filename_path
from utils.transform import normalize_data

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
    """Transform data for both universities.
    """
    logger.info('*-----------TRANSFORM TASK-----------*')
    # First create txt folder if doesn't exist.
    create_folder(ROOT_TXT)
    # Get csv files and full path.
    csv_files = get_filename_path(ROOT_CSV)
    for csv_name, csv_path in csv_files.items():
        logger.info('Working on {csv_name} file.')
        # Read csv file and create dataframe.
        dataframe = pd.read_csv(csv_path)
        # Normalize data.
        logger.info('Clearing data on {csv_name} file.')
        dataframe = normalize_data(dataframe)
        # Create the txt file to save the changes.
        logger.info('Creating txt for {csv_name} file.')
        create_txt(dataframe, csv_name)
    logger.info('Transform data from dataframe/csv.')


def load_data():
    """TODO: Load data for both universities.
    """
    logger.info('*-----------LOAD TASK-----------*')
    logger.info('Loading data to S3.')


# Test connection & functions.
# Connection & Extract_Data working fine.
# if __name__ == '__main__':
#    extract_data()
