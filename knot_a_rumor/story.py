from os.path import join
import yaml

class Story:
    def __init__(self, path):
        self.path = path 
        self.author = None
        self.title = None
        self.scene = None
        self.synopsis = None

    def load(self):
        f = open(self.filename(), 'r')
        text = f.read()
        f.close()

        data = yaml.load(text)
        if data == None:
            return False
        else:
            self.author = data['author']
            self.title = data['title']
            self.scene = data['scene']
            self.synopsis = data['synopsis']
            return True

    def filename(self):
        return join(self.path, "story.yaml")
