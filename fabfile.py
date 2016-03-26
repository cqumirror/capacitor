#!/usr/bin/env python

from fabric.api import cd, run, put
from fabric.contrib.files import exists

web_pages = "~/source-git/index-of-mirrors"
actor = "~/source-git/actor"
target_dir = "/srv/actor"


def pull():
    with cd(web_pages):
        run("git pull")
    with cd(actor):
        run("git pull")


def prepare():
    actor_env_dir = "venv"
    # create target dir and log dir for actor
    run("mkdir -p /srv/actor/log")
    with cd(target_dir):
        # create virtualenv for actor if not exists and upgrade pip
        if not exists(actor_env_dir):
            run("virtualenv venv")
        # upgrade pip
        run("venv/bin/pip install --upgrade pip")
        # init thevenv
        run("venv/bin/pip install --upgrade -r requirements.txt")
    # create log dir for gunicorn in /var/log
    run("mkdir -p /var/log/gunicorn")


def put_config_files():
    # update gunicorn's config
    put("confs_production/gunicorn.py", target_dir)
    put("confs_production/settings.cfg", target_dir)


def deploy():
    put_config_files()
    with cd(actor):
        run("rm -rf /srv/actor/actor.bak")
        run("mv /srv/actor/actor{,.bak}")   # back up
        run("cp -r actor /srv/actor")
        # update requirements for actor
        run("cp requirements.txt /srv/actor")
    with cd(web_pages):
        # update static files
        run("rm -rf /www/mirrors/static.bak")
        run("mv /www/mirrors/static{,.bak}")     # back up
        run("cp -r . /www/mirrors/static")


def start():
    with cd(target_dir):
        actor_pid_file = "gunicorn-actor.pid"
        # kill old processes gracefully if actor running
        if exists(actor_pid_file):
            run("kill -TERM $(<{})".format(actor_pid_file))
        # start new gunicorn processes
        run("export ACTOR_SETTINGS=/srv/actor/settings.cfg && "
            "venv/bin/gunicorn -c gunicorn.py actor:app -D")


def all():
    pull()
    prepare()
    deploy()
    start()
