from sensor.logger import logging
from sensor.exception import SensorException
import sys,os
from sensor.utils import get_collection_as_dataframe

if __name__ =="__main__":
     try:
          get_collection_as_dataframe(database_name = "aps", collection_name = "sensor")
          