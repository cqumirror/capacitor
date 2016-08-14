import errno
import os
import logging


def _mkdir_p(path):
    ab_path = path
    if not os.path.isabs(ab_path):
        curr_dir = os.getcwd()
        ab_path = os.path.join(curr_dir, path)
    try:
        os.makedirs(ab_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(ab_path):
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
