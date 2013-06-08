import bottle
from bottle import jinja2_view as view, jinja2_template as template


class Streamy:

    def __init__(self):
        # the Bottle application
        self.app = bottle.Bottle()
        # the folder where the files to serve are located. Do not set
        # directly, use set_folder instead
        self.folder = "."
        # the TemplateLookup of Jinja
        self.templates = TemplateLookup(directories=[self.folder],
            imports=["from markdown import markdown"],
            input_encoding='utf-8',
            )

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
            data = t.render()
            return data.encode(t.module._source_encoding)

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
        bottle.run(self.app, server="waitress", **kwargs)

run(host='localhost', port=8080)
