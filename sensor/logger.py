import logging
import os
from datetime import datetime

# Log File name
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%y__%H%M%S')}.log"
# Log File Directory
LOG_FILE_DIR = os.path.join.(os.getcwd(),"logs")

# create a dir if not exists
os.makedirs(LOG_FILE_DIR,exist_ok=True)

# Log File Path
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)