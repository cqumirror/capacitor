# capacitor
To provide cache service with RESTful API.

##Layout
- `capacitor/`: flask APP sits here. **capacitor** is the APP's name.
 - `app_logging.py`: logging utilities.
 - `views.py`: routers and its implementation.
 - `response.py`:
 - `security.py`: access control utilities.
- `run_app.py`: for debugging. Just `./run_app.py` in the CLI.

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

