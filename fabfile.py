#!/usr/bin/env python

import os

from fabric.api import cd, run, put
from fabric.contrib.files import exists

PROJECT_NAME = "capacitor"
REPO_URL = "https://github.com/cqumirror/capacitor.git"
# where to install the app
# DST_HOST = "dev.mirrors.lanunion.org"
DST_HOST = "mirrors.cqu.edu.cn"
APP_ROOT = "/srv/apps"

APP_NAME = PROJECT_NAME     # normally project name equals to app name
APP_CFG = "confs_production/settings.cfg"
APP_DST = os.path.join(APP_ROOT, APP_NAME)

GUNICORN_CFG = "confs_production/gunicorn.py"
GUNICORN_LOG_PATH = "/var/log/gunicorn/"     # defined in gunicorn.py
GUNICORN_PID_FILE = "/var/run/gunicorn.pid"          # defined in gunicorn.py


def git_clone_or_pull(repo_url):
    root = "/tmp/source-git"
    if not exists(root):
        run("mkdir -p {}".format(root))
    with cd(root):
        if not exists(PROJECT_NAME):
            run("git clone {}".format(repo_url))
        with cd(PROJECT_NAME):
            run("git pull")
    app_src = os.path.join(root, PROJECT_NAME)
    return app_src


def prepare_venv(app_src):
    requirements_txt = os.path.join(app_src, "requirements.txt")
    app_venv_name = "venv"

    run("mkdir -p {}".format(APP_DST))
    with cd(APP_DST):
        if not exists(app_venv_name):
            run("virtualenv {}".format(app_venv_name))
        # upgrade pip
        run("venv/bin/pip install --upgrade pip")
        # update requirements.txt and upgrade venv
        run("cp {} .".format(requirements_txt))
        run("venv/bin/pip install --upgrade -r requirements.txt")
    # create log dir for gunicorn
    run("mkdir -p {}".format(GUNICORN_LOG_PATH))


def put_config_files():
    put(APP_CFG, APP_DST)
    put(GUNICORN_CFG, APP_DST)


def deploy():
    app_src = git_clone_or_pull(REPO_URL)
    prepare_venv(app_src)
    # update configurations
    put_config_files()
    # update app
    app_lib_old = os.path.join(APP_DST, APP_NAME)
    app_lib_new = os.path.join(app_src, APP_NAME)
    # remove old app lib
    run("rm -rf {}".format(app_lib_old))
    # copy new app lib to app dst
    run("cp -r {} {}".format(app_lib_new, APP_DST))


def start():
    with cd(APP_DST):
        # kill old processes gracefully if app is running
        if exists(GUNICORN_PID_FILE):
            run("kill -TERM $(<{})".format(GUNICORN_PID_FILE))
        # start new gunicorn processes
        settings_cfg = os.path.join(APP_DST, "settings.cfg")
        cmd_export_settings = "export {}_SETTINGS={}".format(
            APP_NAME.upper(),
            settings_cfg)
        gunicorn_cfg = os.path.join(APP_DST, "gunicorn.py")
        cmd_run_app = "venv/bin/gunicorn -c {} " \
                      "{}:app -D".format(gunicorn_cfg, APP_NAME)
        run("{} && {}".format(cmd_export_settings, cmd_run_app))


def update_web_pages():
    """Update web pages, temp use only."""
    repo_url = "https://github.com/cqumirror/index-of-mirrors.git"
    web_pages_src = "/tmp/source-git/index-of-mirrors"
    web_pages_dst = "/www/mirrors/static"
    if not exists(web_pages_src):
        with cd("/tmp/source-git"):
            run("git clone {}".format(repo_url))
    with cd(web_pages_src):
        run("git pull")
    if not exists(web_pages_dst):
        run("mkdir -p {}".format(web_pages_dst))
    with cd(web_pages_src):
        run("rm -rf {}.bak".format(web_pages_dst))
        run("mv /www/mirrors/static{,.bak}")     # backup firstly
        run("cp -r . {}".format(web_pages_dst))


def all():
    deploy()
    start()
    update_web_pages()
