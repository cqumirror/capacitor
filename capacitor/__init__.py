from flask import Flask
import app_logging

app = Flask(__name__)

# default configurations
APP_NAME = "Capacitor"
LOG_LEVEL = "error"
LOG_DIR = "/var/log"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"  # ISO 8601
SERVER_NAME = "localhost:5000"
JSON_SORT_KEYS = False
JSONIFY_PRETTYPRINT_REGULAR = True
SECRET_KEY = "null"
REDIS_HOST = "192.168.113.254"

# load configurations
app.config.from_object(__name__)
app.config.from_envvar("CAPACITOR_SETTINGS")

params = dict(
    app_name=app.config["APP_NAME"],
    log_level=app.config["LOG_LEVEL"],
    log_dir=app.config["LOG_DIR"],)
app.logger.addHandler(app_logging.log_file_handler(**params))

from capacitor import views
