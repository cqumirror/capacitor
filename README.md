actor
===
Back-end server for front-end web pages.

##Features
- [x] Provide RESTful APIs for front-end to get resources.

##Organization
- `actor/`: Flask APP sits here. **Actor** is the APP's name.
 - `app_logging.py`: Logging utils for actor.
 - `views.py`: Routers and its implementation.
 - `response.py`:
- `run_actor.py`: For debugging. Just `./run_actor.py` in the CLI.

##Quick Start for Dev.
- Change into the project directory. Everything happens in it.
- Initialize a virtualenv with the command `virtualenv .pyenv && .pyenv/bin/pip install --upgrade -r requirements.txt`.
- Custom a `settings.cfg` with a copy of `settings.cfg`.
- Run the APP with the command `./run_actor.py` or `.pyenv/bin/python run_actor.py`.
- `./actor_tests.py` or `.pyenv/bin/python actor_tests.py` to auto post data.
- To know details of API, see [here](docs/actor-api.md).

##How to Deploy
TODO

##License
MIT, see `LICENSE` for details.

