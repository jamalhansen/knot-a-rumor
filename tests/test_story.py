import pytest
from knot_a_rumor.story import Story 
from os import getcwd
from os.path import join

@pytest.mark.usefixtures("setup_story")
class TestStory:

    @pytest.fixture()
    def setup_story(self):
        self.path = join(getcwd(), "tests", "fixtures", "library", "basic")
        self.story = Story(self.path)
    
    def test_init_accepts_path_to_story(self):
        assert self.story.path == self.path

    def test_story_has_an_author(self):
        self.story.load()
        assert self.story.author == "Abragraham Lincoln"

    def test_story_looks_for_the_story_yaml_file(self):
        file = self.story.filename()
        assert "story.yaml" in file

    def test_story_has_a_title(self):
        self.story.load()
        assert self.story.title == "American Bacon"

    def test_story_has_an_opening_scene(self):
        self.story.load()
        assert self.story.scene == "flourescent"

    def test_story_has_a_synopsis(self):
        self.story.load()
        assert "zombie" in self.story.synopsis
