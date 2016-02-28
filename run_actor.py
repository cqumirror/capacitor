#!.pyenv/bin/python

import os
curr_path = os.path.abspath(os.curdir)
os.environ["ACTOR_SETTINGS"] = os.path.join(curr_path, "settings_local.cfg")

from actor import app


def main():
    app.run(host="127.0.0.1", debug=True,)


if __name__ == '__main__':
    main()
