import bottle
from jinja2 import Environment, FileSystemLoader


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

if __name__ == "__main__":
    streamy = Streamy()
    streamy.run(host='localhost', port=8080)
