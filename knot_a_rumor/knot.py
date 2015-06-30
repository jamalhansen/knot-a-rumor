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
            "turn": 0 
            }
        return player_state 

    def play(self, player_state):
        player_state["turn"] += 1
        self.load_scene(player_state["story"], player_state["current_scene"])
        return player_state

    def narrate(self):
        return self.scene.narration

    def load_scene(self, story_name, scene_name):
        self.scene = Scene(self.build_story_path(story_name), scene_name)
