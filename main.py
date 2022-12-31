from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
from sensor.utils import get_collection_as_dataframe
from sensor.entity import config_entity


if __name__ =="__main__":
     try:
          #get_collection_as_dataframe(database_name = "aps", collection_name = "sensor")
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config = training_pipeline_config)
     except Exception as e:
          print(e)