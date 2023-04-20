import logging
import os
from datetime import datetime


LOG_File = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(),"logs",LOG_File)
os.makedirs(logs_path,exist_ok=True)


LOG_File_PATH = os.path.join(logs_path,LOG_File)

logging.basicConfig(
    filename=LOG_File_PATH,
    format='[ %(asctime)s ] %(lineno)d %(levelname)s %(message)s',
    level=logging.INFO,
)