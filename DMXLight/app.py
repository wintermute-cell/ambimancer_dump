from flask import Flask, request, send_from_directory
import importlib.util
import sys
import os
import appdirs
import shutil
import threading

SIMULATED = True
if SIMULATED:
    from flask_socketio import SocketIO
    import eventlet
    eventlet.monkey_patch()
else:
    from PyDMXControl.controllers import OpenDMXController
    from PyDMXControl.profiles.defaults import Fixture

APPNAME = 'DMXLight'
APPAUTHOR = 'ambimancer'
EDITING = False

USER_DIR = appdirs.user_data_dir(appname=APPNAME, appauthor=APPAUTHOR) + '/'
SHOW_DIR = USER_DIR + 'shows/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aVerySecretKey'
if SIMULATED and SocketIO:
    socketio = SocketIO(app)

SHOW_THREAD = None
stop_thread = False

if not SIMULATED:
    dmx = OpenDMXController()
    class uking(Fixture):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._register_channel('dimmer')
            self._register_channel_aliases('dimmer', 'dim', 'd')
            self._register_channel('red')
            self._register_channel_aliases('red', 'r')
            self._register_channel('green')
            self._register_channel_aliases('green', 'g')
            self._register_channel('blue')
            self._register_channel_aliases('blue', 'b')
            self._register_channel('strobe')
            self._register_channel('function')
            self._register_channel('shade')
    f1 = dmx.add_fixture(uking, name="RGB1")


class FixtureWrapper:
    def __init__(self, fixture):
        self.fixture = fixture

    def color(self, rgb: list[int], time_ms=0):
        if not SIMULATED:
            self.fixture.color(rgb, time_ms)
        else:
            socketio.emit('fixture_signal', [rgb, time_ms])

    def dim(self, brightness: int, time_ms=0):
        if not SIMULATED:
            self.fixture.dim(brightness, time_ms)
        else:
            socketio.emit('fixture_signal', [brightness, time_ms])


if SIMULATED:
    wfix1 = FixtureWrapper(None)
else:
    wfix1 = FixtureWrapper(f1)


@app.route("/run")
def launch():
    args = request.args
    show_name = args['n']
    if show_name == '':
        return 'Missing lightshow name!', 400
    try:
        # copy color definition
        if not os.path.isfile(SHOW_DIR + 'colors.py'):
            return f'Missing \'colors.py\'!', 400
        shutil.copy(SHOW_DIR + 'colors.py', './colors.py', follow_symlinks=True)

        # create module spec
        modpath = SHOW_DIR + f'{show_name}.py'
        spec = importlib.util.spec_from_file_location(show_name, modpath)
        if not spec:
            return f'Invalid lightshow: {show_name}, file not found.', 400

        # register module
        module = importlib.util.module_from_spec(spec)
        sys.modules[show_name] = module

        # get loader
        loader = spec.loader
        if not loader:
            return f'Failed to acquire spec loader.', 400

        # import the module
        try:
            loader.exec_module(module)
        except FileNotFoundError:
            return f'Invalid lightshow: {show_name}, file not found.', 400

        # call the modules run function
        try:
            global SHOW_THREAD
            if SHOW_THREAD and SHOW_THREAD.is_alive():
                global stop_thread
                stop_thread = True
                SHOW_THREAD.join()
            stop_thread = False
            if SIMULATED:
                SHOW_THREAD = socketio.start_background_task(module.run, [wfix1], lambda: stop_thread)
            else:
                SHOW_THREAD = threading.Thread(target=module.run, args=([wfix1], lambda: stop_thread))
                SHOW_THREAD.start()
        except (AttributeError, TypeError):
            return f'Malformed lightshow: {show_name}, missing or malformed \'run\' attribute.', 400

    except ImportError:
        return f'Invalid lightshow: {show_name}, import failed.', 400
    return '', 200

@app.route("/simulated")
def simuated():
    if SIMULATED:
        return 'simulated', 200
    else:
        return 'not simulated', 404


@app.route("/")
def frontend():
    return send_from_directory('frontend/dist', 'index.html')


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory('frontend/dist', path)


# -------------------
# SOCKET HANDLERS
# -------------------
if SIMULATED:
    @socketio.on('connect')
    def test_connect():
        print('client connected')

    
if __name__ == '__main__':
    if not SIMULATED:
        app.run()
    else:
        socketio.run(app)

    # initialize directories
    if not os.path.exists(USER_DIR):
        print(f'Creating user directory: {USER_DIR}')
        os.makedirs(USER_DIR)
    if not os.path.exists(SHOW_DIR):
        print(f'Creating show directory: {SHOW_DIR}')
        os.makedirs(SHOW_DIR)
    
