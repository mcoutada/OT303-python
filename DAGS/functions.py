from datetime import datetime, timedelta
from importlib.metadata import files
import os
import pandas as pd
from sqlalchemy import create_engine
from config import LOG_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME
from logger import set_logger
from DB_connection import get_engine, db_connection
import logging
import boto3

# Logs configuration
logger = set_logger("ETL")


def extract(university):
    """Get data from universities. TASK OT303-45"""
    engine = get_engine()
    db_connection()
    logger.info("Getting data.")

    query = open(f"SQL/{university}.sql", "r").read()
    df = pd.read_sql(query, engine)

    if not os.path.exists("files"):
        os.mkdir("files")

    df.to_csv(f"files/{university}.csv", index=False)
    logger.info(f"Extraction complete of {university}")

    return df


def normalization(university):
    """Normalize data. TASK"""
    df = pd.read_csv(f"files/{university}.csv")

    logger.info("Transforming data.")
    # University
    df["university"] = df["university"].str.lower()
    df["university"] = df["university"].replace("_", " ", regex=True).str.strip()

    # Career
    df["career"] = df["career"].str.lower()
    df["career"] = df["career"].replace("_", " ", regex=True).str.strip()

    # Inscription Date.

    df["inscription_date"] = pd.to_datetime(df["inscription_date"])
    df["inscription_date"] = df["inscription_date"].dt.strftime("%Y-%m-%d")

    # First name.
    df["first_name"] = df["first_name"].str.lower()
    df["first_name"] = df["first_name"].replace("_", " ", regex=True).str.strip()

    # Last name.
    df["last_name"] = df["last_name"].str.lower()
    df["last_name"] = df["last_name"].replace("_", " ", regex=True).str.strip()

    # Gender.
    df["gender"] = df["gender"].replace(["f", "m"], ["female", "male"])

    # Age.
    df["age"] = df["age"].astype(int)

    # Postal code.
    df["postal_code"] = df["postal_code"].astype("str")

    # Location.
    df["location"] = df["location"].str.lower()
    df["location"] = df["location"].replace("_", " ", regex=True).str.strip()

    # Email.
    df["email"] = df["email"].str.lower()
    df["email"] = df["email"].str.strip()

    logger.info("Normalized Dataframe .")

    return df.to_csv(f"files/{university}.txt", index=False)


def load(university):
    """
    Load data to S3.
    """
    session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    s3 = session.resource("s3")
    s3.meta.client.upload_file(Filename=f"files/{university}.txt", Bucket=AWS_BUCKET_NAME, Key=f"{university}.txt")
    logger.info(f"File {university}.txt uploaded to S3.")

if __name__ == "__main__":
    extract("u_de_palermo")
    normalization("u_de_palermo")
    load("u_de_palermo")