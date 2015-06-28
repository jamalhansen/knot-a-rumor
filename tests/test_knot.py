import pytest
from knot_a_rumor.knot_a_rumor import Knot
from knot_a_rumor.story import Story
from os import getcwd
from os.path import join

@pytest.mark.usefixtures("prepare_knot")
class TestKnot:
    @pytest.fixture()
    def prepare_knot(self):
        self.path = join(getcwd(), "tests", "fixtures", "library")
        self.library = Knot(self.path)
 
    def test_knot_will_accept_story_path(self):
        assert self.library.path == self.path

    def test_knot_will_list_available_stories(self):
        stories = self.library.stories()
        assert "basic" in stories
        assert "test" in stories

    def test_knot_get_story_returns_story(self):
        story = self.library.get_story("basic")
        assert type(story) is Story

    def test_build_story_path_includes_story_name(self):
        path = self.library.build_story_path("wonky")
        assert "wonky" in path
