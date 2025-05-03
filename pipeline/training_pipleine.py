from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.model_training import ModelTraining
from src.feature_store import RedisFeatureStore
from config.paths_config import *
from config.database_config import DB_CONFIG
from src.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Pipeline started...")

    data_ingestion = DataIngestion(DB_CONFIG, RAW_DIR)
    data_ingestion.run()
    logger.info("Data ingestion completed.")

    feature_store = RedisFeatureStore()

    data_processor = DataProcessing(TRAIN_PATH, TEST_PATH, feature_store)
    data_processor.run()
    logger.info("Data processing and feature storing completed.")

    model_trainer = ModelTraining(feature_store)
    model_trainer.run()
    logger.info("Model training pipeline completed successfully.")
