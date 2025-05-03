from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime
import pandas as pd
import sqlalchemy
import os

def load_to_sql(file_path):
    conn = BaseHook.get_connection('postgres_default')  # This connection must be set up in Airflow
    db_uri = (
        f"postgresql+psycopg2://{conn.login}:{conn.password}"
        f"@{conn.host}:{conn.port}/{conn.schema or 'postgres'}"
    )
    engine = sqlalchemy.create_engine(db_uri)

    df = pd.read_csv(file_path)
    df.to_sql(name="titanic", con=engine, if_exists="replace", index=False)

# Define the DAG
with DAG(
    dag_id="extract_titanic_data",
    schedule=None,  # Use schedule_interval instead of schedule
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["example", "gcs", "postgres"]
) as dag:

    # Task: List files in the GCS bucket
    list_files = GCSListObjectsOperator(
        task_id="list_files",
        bucket="raj-bucket-97",
        gcp_conn_id="google_cloud_default",
    )

    # Task: Download the Titanic CSV file from GCS to local file system
    download_file = GCSToLocalFilesystemOperator(
        task_id="download_file",
        bucket="raj-bucket-97",
        object_name="Titanic-Dataset.csv",
        filename="/tmp/Titanic-Dataset.csv",
    )

    # Task: Load the downloaded file to Postgres
    load_data = PythonOperator(
        task_id="load_to_sql",
        python_callable=load_to_sql,
        op_kwargs={"file_path": "/tmp/Titanic-Dataset.csv"},
    )

    # Define task dependencies
    list_files >> download_file >> load_data