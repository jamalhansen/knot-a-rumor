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
        state = { 
            "current_scene": story.scene, 
            "story": name,
            "location": {"x":0, "y":0},
            "turn": 0 ,
            "seen": [],
            "inventory": []
            }
        return state 

    def play(self, state):
        scene = self.load_scene(state)
        state["location"] = scene.start
        return state

    def move(self, state, direction, times=1):
        scene = self.load_scene(state)
        
        if not scene.valid_move(state["location"], direction, times):
            return state

        if direction == "n":
            state["location"]["y"] += times
        elif direction == "s":
            state["location"]["y"] -= times
        elif direction == "e":
            state["location"]["x"] += times
        elif direction == "w":
            state["location"]["x"] -= times

        state["turn"] += 1
        return state

    def load_scene(self, state):
        story_name = state["story"]

        return Scene(self.build_story_path(story_name), state)

    def scene_map(self, state):
        scene = self.load_scene(state)
        return scene.build_map(state)

    def narrate(self, state):
        scene = self.load_scene(state)
        narration = scene.view(state["location"])

        if narration == None:
            return scene.narration

        return narration

    def look(self, state):
        scene = self.load_scene(state)
        state, seen = scene.look(state)
        return (state, seen)

    def describe(self, state, char):
        scene = self.load_scene(state)
        return scene.describe(state, char)

    def take(self, state):
        scene = self.load_scene(state)
        new_state = scene.take(state)
        success = len(new_state["inventory"]) > len(state["inventory"])
        return new_state, success
