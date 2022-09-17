
import logging
import os
import pandas as pd
from datetime import datetime

from config.cfg import ROOT_CSV
from db.db_connection import create_engine_connection
from utils.utils import create_csv_folder, get_src_querys

# Create and configure log
today = datetime.now().date()
logging.basicConfig(
    format='%(asctime)s %(message)s',
    filemode='w',
    level='DEBUG')


def extract_data():
    """Get data from both universities.
    """
    # First create csv folder if doesn't exist.
    create_csv_folder()
    # Create engine
    engine = create_engine_connection()
    # Get sql files and full path.
    sql_files = get_src_querys()
    # Connect engine.
    with engine.connect() as connection:
        # Execute each query and create a .csv
        for sql_file_name, sql_full_path in sql_files.items():
            with open(sql_full_path) as f:
                # Read the query.
                query = f.read()
                logging.info('Extracting data from {}'.format(sql_file_name))
                # Execute query.
                result = connection.execute(query)
                # Create a pandas dataframe with the result.
                df = pd.DataFrame(result)
                logging.info('Writing information to csv.')
                # Create .csv file.
                df.to_csv(os.path.join(
                    ROOT_CSV, f'{sql_file_name[:-4]}.csv'), index=False)
    logging.info('Extracting data from database.')


def transform_data():
    """TODO: Transform data for both universities.
    """
    logging.info('Transform data from dataframe/csv.')


def load_data():
    """TODO: Load data for both universities.
    """
    logging.info('Loading data to S3.')


# Test connection & functions.
# Connection & Extract_Data working fine.
# if __name__ == '__main__':
#    extract_data()
