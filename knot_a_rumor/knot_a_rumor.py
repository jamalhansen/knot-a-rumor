from os import walk
from os.path import join
from knot_a_rumor.story import Story

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
