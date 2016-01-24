actor
===
Back-end server for front-end web pages.

##Features
- [x] Provide RESTful APIs for front-end to get resources.

##Organization
- `actor/`: Flask APP sits here. **Actor** is the APP's name.
 - `domains.py`: Some data objects.
 - `views.py`: Routers and its implementation.
 - `static/`: Web pages are here!
- `run_actor.py`: For debugging. Just `./run_actor.py` in the CLI.

##Quick Start for Dev.
- Change into the project directory. Everything happens in it.
- Initialize a virtualenv with the command `virtualenv .pyenv && .pyenv/bin/pip install --upgrade -r requirements.txt --allow-external mysql-connector-python`.
- Create a database and restore it with `schema.sql`. We use `MariaDB` in production.
- Custom a `settings.cfg` with a copy of `example_settings.cfg`.
- Run the APP with the command `./run_actor.py` or `.pyenv/bin/python run_actor.py`.
- To know details of API, see [here](docs/mirror-site-api.md).

##How to Deploy
TODO

##License
MIT, see `LICENSE` for details.

