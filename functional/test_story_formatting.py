import pytest
from knot_a_rumor.knot_a_rumor import Knot
from os import getcwd
from os.path import join

class TestPennyCanInspectAStory:
    def library_path(self):
        return join(getcwd(), "tests", "fixtures", "library")
    
    def test_penny_can_load_story_info(self):
        # Penny loads up the library
        pennys_story = "penny-pinnacle-pennyslvania"
        library = Knot(self.library_path())

        # Penny lists the stories available(self):
        stories = library.stories()
        assert pennys_story in stories

        # She loads the story
        story = library.get_story(pennys_story)

        # She checks the author
        assert "Penny Pennington" == story.author

        # She checks the title
        assert "Pen's Pennyslvanian Pinnacle" == story.title

        # She checks the filename for the first scene
        assert "Runaway Train Showdown" == story.scene

        # She checks the story synopsis
        assert "Lorem ipsum" in story.synopsis

        # Satisfied, she goes on her way

