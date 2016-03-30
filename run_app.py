#!venv/bin/python

import os
curr_path = os.path.abspath(os.curdir)
os.environ["CAPACITOR_SETTINGS"] = \
    os.path.join(curr_path, "settings_local.cfg")

from capacitor import app


def main():
    app.run(host="localhost", debug=True,)


if __name__ == '__main__':
    main()
