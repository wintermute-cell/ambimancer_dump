from flask import Flask, request, send_file, send_from_directory
import subprocess
import json
import socket
import sys
import appdirs
import os
import shutil


APPNAME = 'mpad'
APPAUTHOR = 'ambimancer'

CLIENT_DIR = 'client/build/'
RESOURCES_DIR = 'resources/'
USER_DIR = appdirs.user_data_dir(appname=APPNAME, appauthor=APPAUTHOR) + '/'
ICON_DIR = USER_DIR + 'icons/'

LAYOUT_FILE = USER_DIR + 'layout.json'
BUTTONS_FILE = USER_DIR + 'buttons.json'
DEFAULT_LAYOUT_FILE = {
    "layout": [["example_button", "example_button"], ["example_button"]]
}
DEFAULT_BUTTONS_FILE = {
    "buttons": {
        "example_button": {
            "name": "Example Button",
            "icon": "example_button",
            "command": "echo Hello World!"
        }
    }
}

def create_app():
    app = Flask(__name__)

    def try_load_layout():
        try:
            with open(LAYOUT_FILE) as f:
                return json.load(f)
        except FileNotFoundError:
            with open(LAYOUT_FILE, 'w') as f:
                json.dump(DEFAULT_LAYOUT_FILE, f)
            with open(LAYOUT_FILE) as f:
                return json.load(f)


    def try_load_buttons():
        try:
            with open(BUTTONS_FILE) as f:
                return json.load(f)
        except FileNotFoundError:
            with open(BUTTONS_FILE, 'w') as f:
                json.dump(DEFAULT_BUTTONS_FILE, f)
            with open(BUTTONS_FILE) as f:
                return json.load(f)


    # ------
    # INIT
    # ------
    def load_layout_and_buttons():
        return try_load_layout()['layout'], try_load_buttons()['buttons']


    LAYOUT, BUTTONS = load_layout_and_buttons()

    # ------
    # ROUTES
    # ------
    @app.route("/")
    def home():
        return send_from_directory(CLIENT_DIR, 'index.html')


    @app.route("/<path:path>")
    def base(path):
        return send_from_directory(CLIENT_DIR, path)


    @app.route("/reload_config")
    def reload_config():
        global LAYOUT
        global BUTTONS
        LAYOUT, BUTTONS = load_layout_and_buttons()
        return '', 200


    @app.route("/get_icon")
    def get_icon():
        icon_name = request.args.get('name')
        filename = ICON_DIR + f'{icon_name}.jpg'
        if not os.path.isfile(filename):
            return send_file(RESOURCES_DIR+'default_icon.jpg', mimetype='image/jpeg')
        else:
            return send_file(filename, mimetype='image/jpeg')


    @app.route("/get_layout")
    def get_layout():
        with open(LAYOUT_FILE) as f:
            return json.load(f)['layout']


    @app.route("/get_buttons")
    def get_buttons():
        return BUTTONS


    @app.route("/run_button")
    def run_button():
        btn_name = request.args.get('name')
        if btn_name == '':
            return "No button name provided", 400
        else:
            cmd = BUTTONS[btn_name]["command"]
            if cmd == '':
                return "Malformed or missing command", 400

            subprocess.Popen(cmd.split())
            return '', 200

    return app


if __name__ == "__main__":
    if len(sys.argv) != 3:
        ipAddr = '127.0.0.1'
        port = '7999'
    else:
        ipAddr = sys.argv[1]
        port = sys.argv[2]


    if not os.path.exists(USER_DIR):
        print(f'Creating user directory: {USER_DIR}')
        os.makedirs(USER_DIR)
    if not os.path.exists(ICON_DIR):
        print(f'Creating icon directory: {ICON_DIR} and copying default icon')
        os.makedirs(ICON_DIR)
        shutil.copyfile(RESOURCES_DIR + 'default_icon.jpg', USER_DIR + 'default_icon.jpg')


    app = create_app()

    hostname = socket.gethostname()
    intro = '\n\n\n--------------------------------------\n'
    intro += f'{APPNAME} running on device {hostname}\n'
    intro += f'Connect to the client at the address:\n http://{ipAddr}:{port}\n'
    intro += f'User data located at {USER_DIR}\n'
    print(intro)

    app.run(host=ipAddr, port=int(port))
