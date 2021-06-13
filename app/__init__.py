from flask import Flask

import logging
import datetime as dt
import urllib.parse
import os


# Initializing the Flask App.
app = Flask(__name__)

# Creating logs directory if doesn't already exist
if not os.path.exists(os.path.dirname(__file__) + "/logs"):
    os.makedirs(os.path.dirname(__file__) + "/logs")
output_file = os.path.dirname(__file__)+"/logs/appinfo.log"

# Configuring logger to output logs in .json format and rotate to .zip every 12 hours
logging.basicConfig(format= '{"levelname":"%(levelname)s","lineno":"%(lineno)s", "funcname":"%(funcName)s" ,"filename": "%(filename)s",  "message": "%(message)s","timestamp":"%(asctime)s"}',
level = logging.DEBUG, filename = output_file) # change when and interval parameters for development if necessary



from app import routes