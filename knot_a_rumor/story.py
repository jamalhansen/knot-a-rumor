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
            self.__dict__ = data

            return True

    def filename(self):
        return join(self.path, "story.yaml")

class Scene():
    def __init__(self, path, state):
        scene_file = state["current_scene"]
        self.load(path, scene_file)

    def load(self, path, scene_file):
        f = open(self.filename(path, scene_file), 'r')
        text = f.read()
        f.close()

        data = yaml.load(text)
        if data == None:
            return False
        else:
            self.__dict__ = data
            self.__dict__["scene_map"] = self.__dict__["scene_map"].strip("\n")

            return True

    def filename(self, path, scene_file):
        return join(path, "{0}.yaml".format(scene_file))

    def disassemble_map(self):
        rows = list(reversed(self.scene_map.split("\n")))
        disassembled = []

        for row in rows:
            disassembled.append(list(row))

        return disassembled

    def reassemble_map(self, grid):
        rows = []

        for row in grid:
            rows.append(''.join(row))

        reassembled = "\n".join(list(reversed(rows)))
        return reassembled

    def build_map(self, state):
        x = state["location"]["x"]
        y = state["location"]["y"]

        grid = self.disassemble_map()

        grid[y][x] = "@"

        if self.level in state["seen"]:
            for item in self.items.values():
                grid[item["y"]][item["x"]] = item["char"]

        reassembled = self.reassemble_map(grid)
        return reassembled

    def valid_move(self, location, direction, times):
        start_x = location["x"]
        start_y = location["y"]

        # validate direction and times
        if not type(times) is int:
            return False

        if not type(direction) is str:
            return False

        if times < 1 or times > 100:
            return False

        if len(direction) > 1:
            return False

        if not direction in "nsew":
            return False

        # find new postion
        x = start_x
        y = start_y

        rows = list(reversed(self.scene_map.split("\n")))

        for i in range (0, times):
            if direction == "n":
                y += 1
            elif direction == "s":
                y -= 1
            elif direction == "e":
                x += 1
            elif direction == "w":
                x -= 1
            
            if len(rows) <= y:
                return False

            if x < 0 or y < 0:
                return False
            
            tiles = list(rows[y])

            if len(tiles) <= x:
                return False

            if tiles[x] != "#":
                return False
           
        return True

    def view(self, location):
        x = location["x"]
        y = location["y"]
        narration = None

        for pview in self.views.values():
            if pview["x"] == x and pview["y"] == y:
                narration = pview["narration"]

        return narration

    def look(self, state):
        seen = "\n".join(self.items.keys())

        if self.level not in state["seen"]:
            state["seen"].append(self.level)

        return state, seen 

    def describe(self, state, char):
        if self.level not in state["seen"]:
            return state, None

        items = self.items.values()

        item_list = list(filter(lambda x: x["char"] == char, items))
        if len(item_list) == 0:
            return state, None

        return state, item_list[0]["description"]
