from os import walk
from os.path import join
from knot_a_rumor.story import Story, Scene

class Knot:
    def __init__(self, path):
        self.path = path

    def stories(self):
        return next(walk(self.path))[1]

    def get_story(self, name):
        story = Story(self.build_story_path(name))
        story.load()
        return story

    def build_story_path(self, name):
        return join(self.path, name)

    def init_story(self, name):
        story = self.get_story(name)
        player_state = { 
            "current_scene": story.scene, 
            "story": name,
            "location" : { "x":0, "y":0},
            "turn": 0 ,
            "seen": []
            }
        return player_state 

    def play(self, player_state):
        scene = self.load_scene(player_state)
        player_state["location"] = scene.start
        return player_state

    def move(self, player_state, direction, times=1):
        scene = self.load_scene(player_state)
        
        if not scene.valid_move(player_state["location"], direction, times):
            return player_state

        if direction == "n":
            player_state["location"]["y"] += times
        elif direction == "s":
            player_state["location"]["y"] -= times
        elif direction == "e":
            player_state["location"]["x"] += times
        elif direction == "w":
            player_state["location"]["x"] -= times

        player_state["turn"] += 1
        return player_state

    def load_scene(self, player_state):
        story_name = player_state["story"]

        return Scene(self.build_story_path(story_name), player_state)

    def scene_map(self, player_state):
        scene = self.load_scene(player_state)
        return scene.build_map(player_state)

    def narrate(self, player_state):
        scene = self.load_scene(player_state)
        narration = scene.view(player_state["location"])

        if narration == None:
            return scene.narration

        return narration

    def look(self, player_state):
        scene = self.load_scene(player_state)
        player_state, seen = scene.look(player_state)
        return (player_state, seen)

    def describe(self, player_state, char):
        scene = self.load_scene(player_state)
        return scene.describe(player_state, char)
