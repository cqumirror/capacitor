from flask import Flask
import app_logging

app = Flask(__name__)

# default configurations
APP_NAME = "Actor"
LOG_LEVEL = "error"
LOG_DIR = "/var/log"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SERVER_NAME = "localhost:5000"
JSON_SORT_KEYS = False
JSONIFY_PRETTYPRINT_REGULAR = True

# load configurations
app.config.from_object(__name__)
app.config.from_envvar("ACTOR_SETTINGS")

params = dict(
    app_name=app.config["APP_NAME"],
    log_level=app.config["LOG_LEVEL"],
    log_dir=app.config["LOG_DIR"],)
app.logger.addHandler(app_logging.log_file_handler(**params))

from actor import views
