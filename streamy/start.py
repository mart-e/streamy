import bottle
import socyallib
from jinja2 import Environment, FileSystemLoader

import os
import sys
import thread
import urlparse
from datetime import datetime, timedelta

# add project dir and libs dir to the PYTHON PATH to ensure they are
# importable
from utils import settings, SettingsValidationError

import bottle
from bottle import (Bottle, run, static_file, view, request)

import clize

app = Bottle()
GLOBAL_CONTEXT = {
    'settings': settings,
    'pastes_count': Paste.get_pastes_count(),
    'refresh_counter': datetime.now()
}

class Streamy:

    def __init__(self):
        # the Bottle application
        self.app = bottle.Bottle()
        # the folder where the files to serve are located. Do not set
        # directly, use set_folder instead
        self.folder = "templates/"
        # the TemplateLookup of Jinja
        self.templates = Environment(loader=FileSystemLoader('./templates'))

        def base_lister():
            files = []
            for dirpath, dirnames, filenames in os.walk(self.folder):
                for f in filenames:
                    absp = os.path.join(dirpath, f)
                    path = os.path.relpath(absp, self.folder)
                    good = True
                    for ex in self.file_exclusion:
                        if re.match(ex, path):
                            good = False
                            continue
                    if good:
                        files.append(path)
            return files

        @self.app.route('/', method=['GET'])
        def home():
            t = self.templates.get_template("index.html")
            return t.render()

        @self.app.route('/fetch/<stream_id:int>/<from_id:int>', method=['GET'])
        @self.app.route('/fetch/<stream_id:int>/<from_id:int>/<size:int>', method=['GET'])
        def fetch(stream_id, from_id, size=None):
            pass

    def set_folder(self, folder):
        """
        Sets the folder where the files to serve are located.
        """
        self.folder = folder
        self.templates.directories[0] = folder

    def run(self, **kwargs):
        """
        Launch a development web server.
        """
        kwargs.setdefault("host", "0.0.0.0")
        bottle.run(self.app, **kwargs)


@clize.clize(coerce={'debug': bool, 'compressed_static': bool})
def runserver(host='', port='', debug=None, user='', group='',
              settings_file='', compressed_static=None,
              version=False, paste_id_length=None):

    if version:
        print('Streqmy V%s' % settings.VERSION)
        sys.exit(0)

    settings.HOST = host or settings.HOST
    settings.PORT = port or settings.PORT
    settings.USER = user or settings.USER
    settings.GROUP = group or settings.GROUP
    settings.PASTE_ID_LENGTH = paste_id_length or settings.PASTE_ID_LENGTH

    try:
        _, app = get_app(debug, settings_file, compressed_static, settings=settings)
    except SettingsValidationError as err:
        print >>sys.stderr, 'Configuration error: %s' % err.message
        sys.exit(1)

    thread.start_new_thread(drop_privileges, (settings.USER, settings.GROUP))

    if settings.DEBUG:
        run(app, host=settings.HOST, port=settings.PORT, reloader=True,
            server="cherrypy")
    else:
        run(app, host=settings.HOST, port=settings.PORT, server="cherrypy")


def main():
    clize.run(runserver)

if __name__ == "__main__":
    main()
    # streamy = Streamy()
    # streamy.run(host='localhost', port=8080)
