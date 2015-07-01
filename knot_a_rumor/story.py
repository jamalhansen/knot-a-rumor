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

class Scene():
    def __init__(self, path, scene_file):
        self.load(path, scene_file)

    def load(self, path, scene_file):
        f = open(self.filename(path, scene_file), 'r')
        text = f.read()
        f.close()

        data = yaml.load(text)
        if data == None:
            return False
        else:
            self.narration = data['narration']
            self.name = data['name']
            self.scene_map = data['map'].rstrip('\n')
            self.start = data['start']

            return True

    def filename(self, path, scene_file):
        return join(path, "{0}.yaml".format(scene_file))

    def build_map(self, player_x, player_y):
        rows = list(reversed(self.scene_map.split("\n")))
        replaced = list(rows[player_y])
        replaced[player_x] = "@"
        rows[player_y] = ''.join(replaced)
        return "\n".join(list(reversed(rows)))
