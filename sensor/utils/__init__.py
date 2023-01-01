import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_client
import os,sys

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading Data from Database: {database_name} and collection: {collection_name}")
        df =  pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "__id" in df.columns:
            df = df.drop("__id",axis=1)
        logging.info(f"Row and columns")
        return df

    except Exception as e:
        raise SensorException(e, sys)