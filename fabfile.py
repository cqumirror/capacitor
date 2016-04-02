#!/usr/bin/env python

import os

from fabric.api import cd, run, put
from fabric.contrib.files import exists

# where to install the app
app_root = "/srv/apps"
git_root = "~/source-git"

project_name = "capacitor"
app_name = project_name     # normally project name equals to app name
app_cfg_src = "confs_production/"
app_cfg_filename = "settings.cfg"
app_src = os.path.join(git_root, project_name)
app_dst = os.path.join(app_root, app_name)

gunicorn_cfg_src = "confs_production/"
gunicorn_cfg_filename = "gunicorn.py"
gunicorn_log_path = "/var/log/gunicorn"
gunicorn_pid_file = "gunicorn.pid"   # defined in gunicorn.py


def update_web_pages():
    """Update web pages, temp use only."""
    web_pages_src = os.path.join(git_root, "index-of-mirrors")
    web_pages_dst = "/www/mirrors/static"
    with cd(web_pages_src):
        run("git pull")
        run("rm -rf /www/mirrors/static.bak")
        run("mv /www/mirrors/static{,.bak}")     # backup firstly
        run("cp -r . /www/mirrors/static")


def git_pull():
    with cd(app_src):
        run("git pull")


def prepare_env():
    requirements_txt = os.path.join(app_src, "requirements.txt")
    app_venv_name = "venv"

    run("mkdir -p {}".format(app_dst))
    with cd(app_dst):
        if not exists(app_venv_name):
            run("virtualenv {}".format(app_venv_name))
        # upgrade pip
        run("venv/bin/pip install --upgrade pip")
        # update requirements.txt and upgrade venv
        run("cp {} .".format(requirements_txt))
        run("venv/bin/pip install --upgrade -r requirements.txt")
    # create log dir for gunicorn
    run("mkdir -p {}".format(gunicorn_log_path))


def put_config_files():
    app_settings_cfg = os.path.join(app_cfg_src, app_cfg_filename)
    gunicorn_cfg = os.path.join(gunicorn_cfg_src, gunicorn_cfg_filename)
    put(app_settings_cfg, app_dst)
    put(gunicorn_cfg, app_dst)


def deploy():
    # update configurations
    put_config_files()
    # update app
    app_lib_old = os.path.join(app_dst, app_name)
    app_lib_new = os.path.join(app_src, app_name)
    # remove old app lib
    run("rm -rf {}".format(app_lib_old))
    # copy new app lib to app dst
    run("cp -r {} {}".format(app_lib_new, app_dst))


def start():
    with cd(app_dst):
        # kill old processes gracefully if app is running
        if exists(gunicorn_pid_file):
            run("kill -TERM $(<{})".format(gunicorn_pid_file))
        # start new gunicorn processes
        app_settings_cfg = os.path.join(app_dst, app_cfg_filename)
        cmd_export_settings = "export {}_SETTINGS={}".format(
            app_name.upper(),
            app_settings_cfg)
        gunicorn_cfg = os.path.join(app_dst, gunicorn_cfg_filename)
        cmd_run_app = "venv/bin/gunicorn -c {} " \
                      "{}:app -D".format(gunicorn_cfg, app_name)
        run("{} && {}".format(cmd_export_settings, cmd_run_app))


def all():
    git_pull()
    prepare_env()
    deploy()
    start()
    update_web_pages()
