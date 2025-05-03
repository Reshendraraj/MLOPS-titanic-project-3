import psycopg2
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import os
from sklearn.model_selection import train_test_split
import sys
from config.database_config import DB_CONFIG
from config.paths_config import *  # Ensure this file contains necessary path constants

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, db_params, output_dir):
        self.db_params = db_params
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure the output directory exists

    def connect_to_Db(self):
        try:
            conn = psycopg2.connect(
                host=self.db_params['host'],
                port=self.db_params['port'],
                dbname=self.db_params['dbname'],
                user=self.db_params['user'],
                password=self.db_params['password']  # Fixed the typo here
            )
            logger.info("Database connection established.")
            return conn
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise CustomException(f"Database connection failed: {e}", sys)

    def extract_data(self):
        try:
            conn = self.connect_to_Db()
            query = "SELECT * FROM public.titanic"
            df = pd.read_sql_query(query, conn)
            conn.close()
            logger.info("Data extraction completed.")
            return df
        except Exception as e:
            logger.error(f"Data extraction failed: {e}")
            raise CustomException(f"Data extraction failed: {e}", sys)

    def save_data(self, df):
        try:
            train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
            train_df.to_csv(TRAIN_PATH, index=False)  # Ensure TRAIN_PATH is defined in paths_config
            test_df.to_csv(TEST_PATH, index=False)    # Ensure TEST_PATH is defined in paths_config
            logger.info("Data splitting and saving completed.")
        except Exception as e:
            logger.error(f"Error while saving data: {e}")
            raise CustomException(f"Error while saving data: {e}", sys)

    def run(self):
        try:
            logger.info("Data Ingestion Pipeline Started...")
            df = self.extract_data()
            self.save_data(df)
            logger.info("Data Ingestion Pipeline Completed.")
        except Exception as e:
            logger.error(f"Error in Data Ingestion Pipeline: {e}")
            raise CustomException(f"Error in Data Ingestion Pipeline: {e}", sys)

if __name__ == "__main__":
    try:
        data_ingestion = DataIngestion(DB_CONFIG, RAW_DIR)  # Ensure RAW_DIR is defined in paths_config
        data_ingestion.run()
    except CustomException as ce:
        logger.error(f"Custom exception occurred: {ce}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
