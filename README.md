# capacitor
To cache data from mirror back-end and provide APIs to access them.

##Features
- [x] Provide RESTful APIs for front-end to get resources.

##Layout
- `capacitor/`: Flask APP sits here. **Capacitor** is the APP's name.
 - `app_logging.py`: Logging utilities.
 - `views.py`: Routers and its implementation.
 - `response.py`:
 - `security.py`: Access control utilities.
- `run_app.py`: For debugging. Just `./run_app.py` in the CLI.

##Quick Start for Dev.
- Change into the project directory. Everything happens here.
- Initialize a virtualenv with the command `virtualenv venv && venv/bin/pip install --upgrade -r requirements.txt`.
- Custom a `settings_local.cfg` with a copy of `settings.cfg`.
- Run the APP with the command `./run_app.py` or `venv/bin/python run_app.py`.
- To know detail of APIs, see [docs/apis.md](docs/apis.md).

##How to Deploy
TODO

##License
MIT, see `LICENSE` for details.

