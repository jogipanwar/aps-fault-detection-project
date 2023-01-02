import os,sys
import pandas as pd
import numpy as np
from sensor.entity import artifact_entity,config_entity 
from sensor.logger import logging
from sensor.exception import SensorException
from scipy.stats import ks_2samp
from typing import Optional
from sensor import utils

class DataValidation:
    
    def __init__(
                self,data_validation_config:config_entity.DataValidationConfig,
                data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try: 
            logging.info(f"{'>>'*20} Data Validation {'>>'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()

        except Exception as e:
            raise SensorException(e,sys)



    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        """
        This function will drop columns from Dataframe which contain missing Values morn than specified criteria.

        df: Accepts a Pandas DataFrame
        =======================================================================================

        return a pandas DataFrame if atleast a single column is available
        """
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]  # return missing values in percentage
            drop_column_names = null_report[null_report>0.3].index
            
            self.validation_error[report_key_name] = drop_column_names
            df.drop(list(drop_column_names),axis=1,inplace=True)

            if len(df.columns)==0:  #return noe if all thecolumns are dropped
                return None
            return df

        except Exception as e:
            raise SensorException(e,sys)
    
    
    
    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns
            
            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_key_name] = missing_columns
                return False
            return True

        except Exception as e:
            raise SensorException(e,sys)


    
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:

                # Null Hypothesis: Both Column data drawn from same distribution
                base_data,current_data = base_df[base_column],current_df[base_column]
                logging.info(f"base column name: {base_column}")
                same_distribution = ks_2samp(base_data, current_data)

                if same_distribution.pvalue>0.05:
                    #we are accepting null Hypothesis
                    drift_report[base_column] = {
                        "pvalue": same_distribution.pvalue,
                        "same_distribution": True
                    }
                    #same distribution
                else:
                    drift_report[base_column] = {
                        "pvalue": same_distribution.pvalue,
                        "same_distribution": False
                    #diffrent distribution
                    }

            self.validation_error[report_key_name] = drift_report

        except Exception as e:
            raise SensorException(e,sys)


    
    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            
            logging.info(f"Replace na value in base df")
            #base_df has na as null
            base_df.replace({"na":np.NAN},inplace=True)

            logging.info(f"Drop null values colums from base df")
            base_df=self.drop_missing_values_columns(df=base_df,report_key_name="missing_values_within_base_dataset")

            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Drop null values colums from train df")
            train_df = self.drop_missing_values_columns(df=train_df,report_key_name="missing_values_within_train_dataset")
            logging.info(f"Drop null values colums from test df")
            test_df = self.drop_missing_values_columns(df=test_df,report_key_name="missing_values_within_test_dataset")
            
            exclude_columns = ["class"]
            base_df = utils.convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df, exclude_columns=exclude_columns)


            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")

            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")

            #write the yaml report
            logging.info("Write reprt in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise SensorException(e,sys)