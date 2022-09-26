import os
from getpass import getuser

from . import logger
import pandas as pd
from decouple import config
from sqlalchemy import create_engine


def set_logger(file_path):
    return logger.set_logger(logger_name=logger.get_rel_path(file_path))


class University:
    def __init__(self, p_name, p_log):
        self.name = p_name
        self.log = p_log
        self.os_user = getuser()
        self.sql_folder, self.sql_name, self.sql_file = self.find_file(
            os.path.dirname(__file__), ".sql"
        )
        self.csv_name = os.path.splitext(self.sql_name)[0] + ".csv"
        self.csv_file = os.path.join(self.sql_folder, self.csv_name)
        self.sql_query = self.read_sql()
        self.log.info(f"Finished setting files and folders for {self.name}")

    def find_file(self, p_fpath, p_ext):
        for folder, folders_in_folder, files_in_folder in os.walk(p_fpath):
            for file in files_in_folder:
                if self.name.lower() in file.lower() and file.lower().endswith(
                    p_ext.lower()
                ):
                    return folder, file, os.path.join(folder, file)
        # If file not found log error and raise FileNotFoundError
        self.log.error(
            f"No {p_ext} file found for University {self.name} in {p_fpath}")
        raise FileNotFoundError

    def read_sql(self):
        with open(self.sql_file, "r") as file:
            sql_query = file.read()
        return sql_query

    def get_db_conn(self):

        POSTGRES_USER = config("POSTGRES_USER")
        POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
        POSTGRES_DB = config("POSTGRES_DB")
        POSTGRES_PORT = config("POSTGRES_PORT")
        POSTGRES_HOST = config("POSTGRES_HOST")
        POSTGRES_SCHEMA = config("POSTGRES_SCHEMA")

        url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        engine = create_engine(
            url, connect_args={"options": f"-csearch_path={POSTGRES_SCHEMA}"}
        )
        engine.connect()

        return engine

    def extract(self):

        pd.read_sql(sql=self.sql_query, con=self.get_db_conn()).to_csv(
            path_or_buf=self.csv_file, index=False
        )
