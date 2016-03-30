#!/usr/bin/env python

import os

from fabric.api import cd, run, put
from fabric.contrib.files import exists

srv_root = "/srv"
git_root = "~/source-git"

app_name = "capacitor"
app_src = os.path.join(git_root, app_name)
app_dst = os.path.join(srv_root, app_name)

gunicorn_log_path = "/var/log/gunicorn"
gunicorn_pid_file = "gunicorn.pid"          # defined in gunicorn.py


def update_web_pages():
    """Update web pages, temp use only."""
    web_pages_src = os.path.join(git_root, "index-of-mirrors")
    web_pages_dst = "/www/mirrors/static"
    with cd(web_pages_src):
        run("git pull")
        run("rm -rf /www/mirrors/static.bak")
        run("mv /www/mirrors/static{,.bak}")     # backup
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
    put("confs_production/gunicorn.py", app_dst)
    put("confs_production/settings.cfg", app_dst)


def deploy():
    # update configurations
    put_config_files()
    # update app lib
    app_lib_name = app_name
    app_lib_old = os.path.join(app_dst, app_lib_name)
    app_lib_new = os.path.join(app_src, app_lib_name)
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
        app_settings_cfg = os.path.join(app_dst, "settings.cfg")
        cmd_export_settings = "export {}_SETTINGS={}".format(
            app_name.upper(),
            app_settings_cfg)
        cmd_run_app = "venv/bin/gunicorn -c gunicorn.py " \
                      "{}:app -D".format(app_name)
        run("{} && {}".format(cmd_export_settings, cmd_run_app))


def all():
    git_pull()
    prepare_env()
    deploy()
    start()
    update_web_pages()
