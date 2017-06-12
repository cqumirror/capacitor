app_name = "capacitor"
# server socket
bind = "127.0.0.1:8000"
backlog = 2048

# worker process
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 30

# logging
errorlog = "/var/log/gunicorn/{}.error.log".format(app_name)
accesslog = "/var/log/gunicorn/{}.access.log".format(app_name)

# server mechanics
daemon = False
pidfile = "/var/run/gunicorn.pid"

# test
preload_app = True
