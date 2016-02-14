from flask import Flask
import app_logging

app = Flask(__name__)

APP_NAME = "Actor"
SERVER_NAME = "localhost:5000"
LOG_LEVEL = "error"
LOG_DIR = "/var/log"

# load configurations
app.config.from_object(__name__)
app.config.from_envvar("ACTOR_SETTINGS")

params = dict(
    app_name=app.config["APP_NAME"],
    log_level=app.config["LOG_LEVEL"],
    log_dir=app.config["LOG_DIR"],)
app.logger.addHandler(app_logging.log_file_handler(**params))

from actor import views
