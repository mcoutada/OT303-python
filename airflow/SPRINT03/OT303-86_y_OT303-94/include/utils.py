import os
import sys

import boto3
import pandas as pd
from decouple import config
from sqlalchemy import create_engine

# Airflow sets $AIRFLOW_HOME as the current working directory
# which makes same level imports to fail (like import logger.py from utils.py)
curr_work_directory = os.getcwd()
project_folder = os.path.dirname(os.path.realpath(sys.argv[0]))

if curr_work_directory != project_folder:
    sys.path.append(project_folder)
    from include import logger
    sys.path.remove(project_folder)
else:
    from include import logger


class University:
    def __init__(self, p_name, p_dag_file):
        self.name = p_name
        self.log = logger.set_logger(
            logger_name=f"{self.name}@{logger.get_rel_path(p_dag_file)}"
        )
        self.sql_folder, self.sql_name, self.sql_file = self.find_file(
            os.path.dirname(__file__), ".sql"
        )
        self.csv_name = os.path.splitext(self.sql_name)[0] + ".csv"
        self.csv_file = os.path.join(self.sql_folder, self.csv_name)
        self.txt_name = os.path.splitext(self.sql_name)[0] + ".txt"
        self.txt_file = os.path.join(self.sql_folder, self.txt_name)
        self.sql_query = self.read_sql()
        # decorate/wrap functions with log_basics, to log the function's start,
        # end and elapsed time
        self.extract = logger.log_basics(self.log)(self.extract)
        self.transform = logger.log_basics(self.log)(self.transform)
        self.load = logger.log_basics(self.log)(self.load)
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

    def extract(self):

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
        pd.read_sql(sql=self.sql_query, con=engine).to_csv(
            path_or_buf=self.csv_file, index=False
        )

    def transform(self):

        uni_df = pd.read_csv(
            filepath_or_buffer=self.csv_file, parse_dates=["inscription_date"]
        )

        # university: str minúsculas, sin espacios extras, ni guiones
        # career: str minúsculas, sin espacios extras, ni guiones
        # first_name: str minúscula y sin espacios, ni guiones
        # last_name: str minúscula y sin espacios, ni guiones
        # location: str minúscula sin espacios extras, ni guiones
        # email: str minúsculas, sin espacios extras, ni guiones

        cols = [
            "university",
            "career",
            "first_name",
            "last_name",
            "location",
            "email"]

        # Remove Hyphen -, en dash –, em dash —, Underscore _
        # Set to lowercase
        # remove all leading, trailing, and duplicate whitespace characters
        # (space, tab, newline, and so on)

        # replace seems to achieve the best replacement performance
        # https://stackoverflow.com/questions/3411771/best-way-to-replace-multiple-characters-in-a-string
        uni_df[cols] = uni_df[cols].applymap(
            lambda x: " ".join(
                x.replace("-", " ")
                .replace("–", " ")
                .replace("—", " ")
                .replace("_", " ")
                .lower()
                .split()
            )
        )

        # inscription_date: str %Y-%m-%d format
        uni_df["inscription_date"] = pd.to_datetime(
            uni_df["inscription_date"]
        ).dt.strftime("%Y-%m-%d")

        # postal_code: str
        # str(x) is needed in case you rerun (it doesn't matter if you do
        # .astype(str), pandas takes it as an int on next run)
        uni_df["postal_code"] = (
            uni_df["postal_code"]
            .apply(lambda x: "".join(filter(str.isdigit, str(x))))
            .astype(str)
        )

        # gender: str choice(male, female)
        uni_df["gender"] = uni_df["gender"].apply(
            lambda x: "male"
            if x[0].upper() == "M"
            else "female"
            if x[0].upper() == "F"
            else None
        )

        # age: int
        uni_df = uni_df.astype({"age": int})

        uni_df.to_csv(path_or_buf=self.txt_file, index=False)

        self.log.info(f"{self.txt_file} first lines:\n{uni_df.head()}")

    def load(self):

        AWS_BUCKET_NAME = config("AWS_BUCKET_NAME")
        AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
        REGION = config("REGION")

        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3 = session.resource("s3")
        # Filename: File to upload
        # Bucket: Bucket to upload to (the top level directory under AWS S3)
        # Key - S3 object name. How and where the file is stored in S3.
        # Key = filename --> file is stored in the S3's root folder with the same name from source.
        # Key = subfolder/newname.ext --> file is renamed and stored in subfolder (it will be created if it doesn't exist in remote)
        # Key = os.path.join(os.path.basename(project_folder), self.txt_name)
        # --> /OT303-71/salvador.txt
        s3.meta.client.upload_file(
            Filename=self.txt_file,
            Bucket=AWS_BUCKET_NAME,
            Key=os.path.join(os.path.basename(project_folder), self.txt_name),
        )