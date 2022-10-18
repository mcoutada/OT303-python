# [Alkemy.org](https://alkemy.org) - Python + Data Analytics

The course is divided in 3 main projects:
1. Admission challenge.
2. Creating Dags with Apache Airflow
3. Processing Big Data files with Apache Hadoop

Led by an expert in the field as a mentor. Organized using Agile methodology, with weekly sprints, and daily meetings, everything formalized through JIRA tickets.

## Admission challenge:
Extract CSV files from different sources through Python's Requests library.
Transform the data using Python's Pandas library.
Load the data frames to a PostgreSQL database using SQLAlchemy.
Set the project into a Virtual Environment (venv) and generate a proper requirements.txt.
Generate a log of the process using Python's logging library.
The DB config is taken from a .env file using Python's decouple library.
[Project's repository](https://github.com/mcoutada/Alkemy_Challenge_Data_Analytics_con_Python)

## Creating Dags with Apache Airflow
Install Ubuntu's Windows Subsystem for Linux (WSL).
Install Apache Airflow in WSL.
Create SQL queries to extract info from a PostgreSQL DB using SQLAlchemy.
Create a DAG with 3 tasks (extract, load, transform).
- Extract from the database using the SQL script to a CSV file.
- Transform the CSV files using Python's Pandas library and save them into TXT files.
- Load the TXT files into an AWS S3 bucket.
Refactor the DAG to be generated dynamically using YAML/jinja2.
Generate a log of the process using Python's logging library.
The DB config is taken from a .env file using Python's decouple library.
[Project's repository](https://github.com/alkemyTech/OT303-python/tree/marianocoutada/airflow)

-Performing SQL queries for an ETL project with Pandas, SQLAlchemy and PostgreSQL.
-Log configuration with the Python Logging library.
-Creating Dags with Apache Airflow, generating dynamic Dags with DagFactory.
-Data processing and analysis with the python pandas library.


## Processing Big Data files with Apache Hadoop
Install Hadoop in WSL.
Implement a MapReduce technique for 3 different tasks using:
- A Python's mapper.py and reducer.py to process a small file (200mb).
- Using Hadoop to process a big file (4 GB), loading it into HDFS and processing it with hadoop-streaming-X.X.X.jar.
Automate the Bash commands through a main.py script for the 3 tasks.
Creation of Unit Tests.
Unit Test Documentation.
[Project's repository](https://github.com/alkemyTech/OT303-python/tree/marianocoutada/bigdata)
