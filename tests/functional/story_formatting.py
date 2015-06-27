import pytest
from knot_a_rumor.knot_a_rumor import Knot
from os import getcwd
from os.path import join

class TestPennyCanInspectAStory:
    def pennys_story_path(self):
        return join(getcwd(), "tests", "fixtures", "penny")
    
    def test_penny_can_load_story_info(self):
        # Penny has a story that she wants to discover information about
        library = Knot(self.pennys_story_path())

        # She loads the story
        story = library.get_story()

        # She checks the author
        assert story.author == "Penny Pennington"

        # She checks the title
        assert story.title == "Pen's Pennyslvanian Pinnacle"

        # She checks the filename for the first scene
        assert story.starting_scene == "Runaway Train Showdown"

        # Satisfied, she goes on her way

