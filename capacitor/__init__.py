
from flask import Flask
import app_logging

app = Flask(__name__)

# default configurations
APP_NAME = "Capacitor"
LOG_LEVEL = "error"
LOG_DIR = "/var/log"
# e.g. 2016-08-22T15:49:38Z ERROR: it works [in capacitor/__init__.py:35]
LOG_FMT = "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
DATE_FMT = "%Y-%m-%dT%H:%M:%SZ"  # ISO 8601, e.g. 2016-11-11T12:20:03Z
SERVER_NAME = "localhost:5000"
JSON_SORT_KEYS = False
JSONIFY_PRETTYPRINT_REGULAR = True
SECRET_KEY = "null"

# to load configurations
app.config.from_object(__name__)
app.config.from_envvar("CAPACITOR_SETTINGS")


def settings_get(name, default=None):
    name_upper = name.upper()
    ret = app.config[name_upper] if name_upper in app.config else default
    return ret

# register app log
params = dict(
    app_name=settings_get("APP_NAME"),
    log_level=settings_get("LOG_LEVEL"),
    log_dir=settings_get("LOG_DIR"),
    log_fmt=LOG_FMT, date_fmt=DATE_FMT)
app.logger.addHandler(app_logging.log_file_handler(**params))

from capacitor import views
