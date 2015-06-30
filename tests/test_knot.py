import pytest
from knot_a_rumor.knot import Knot
from knot_a_rumor.story import Story, Scene
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

    def test_init_story_returns_a_dict(self):
        player_state = self.library.init_story("basic")
        assert type(player_state) is dict

    def test_play_accepts_and_returns_a_dict(self):
        player_state = self.library.init_story("basic")
        player_state = self.library.play(player_state)
        assert type(player_state) is dict

    def test_narrate_returns_a_description_of_the_scene(self):
        player_state = self.library.init_story("basic")
        player_state = self.library.play(player_state)
        description = self.library.narrate()
        assert "This is a basic description of a basic scene" == description

    def test_player_state_contains_the_current_scene(self):
        player_state = self.library.init_story("basic")
        assert "flourescent" == player_state["current_scene"]

    def test_player_state_contains_the_current_story(self):
        player_state = self.library.init_story("basic")
        assert "basic" == player_state["story"]

    def test_player_state_contains_the_number_of_turns_played(self):
        player_state = self.library.init_story("basic")
        assert 0 == player_state["turn"]
        player_state = self.library.play(player_state)
        assert 1 == player_state["turn"]
        player_state = self.library.play(player_state)
        assert 2 == player_state["turn"]

    def test_load_scene_loads_scene(self):
        player_state = self.library.init_story("basic")
        self.library.load_scene("basic", player_state["current_scene"])
        assert type(self.library.scene) == Scene



