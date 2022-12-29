import os 

class TrainingPipelineConfig:
    def __init__(self):
        self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%y__%H%M%S')}")


# class DataIngestionConfig:... three dot represent pass

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.database_name = "aps"
        self.collection_name = "sensor"
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")

class DataValidationConfig:...
class DataTransformationConfig:...  
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...
