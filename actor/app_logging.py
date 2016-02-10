import errno
import os
import logging


def _mkdir_p(path):
    try:
        os.mkdir(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def log_file_handler(app_name, log_level, log_dir):
    app_log_dir = os.path.join(log_dir, app_name.lower())
    _mkdir_p(app_log_dir)

    log_name = "{}.log".format(log_level)
    log_path = os.path.join(app_log_dir, log_name)

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
        datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    return file_handler
