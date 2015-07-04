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
 
    def set_location(self, player_state, x, y):
        player_state["location"]["x"] = x
        player_state["location"]["y"] = y
        return player_state

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
        description = self.library.narrate(player_state)
        assert "This is a basic description of a basic scene" == description

    def test_narrate_returns_a_positional_description_of_the_scene(self):
        player_state = self.library.init_story("basic")
        player_state = self.set_location(player_state, 3, 2)
        description = self.library.narrate(player_state)
        assert "You are at the upper right." == description

    def test_player_state_contains_the_current_scene(self):
        player_state = self.library.init_story("basic")
        assert "flourescent" == player_state["current_scene"]

    def test_player_state_contains_location(self):
        player_state = self.library.init_story("basic")
        assert "location" in player_state.keys()
        assert "x" in player_state["location"].keys()
        assert "y" in player_state["location"].keys()

    def test_player_state_contains_the_current_story(self):
        player_state = self.library.init_story("basic")
        assert "basic" == player_state["story"]

    def test_player_state_contains_the_number_of_turns_played(self):
        player_state = self.library.init_story("basic")
        assert 0 == player_state["turn"]
        player_state = self.library.move(player_state, "e")
        assert 1 == player_state["turn"]
        player_state = self.library.move(player_state, "e")
        assert 2 == player_state["turn"]

    def test_load_scene_returns_scene(self):
        player_state = self.library.init_story("basic")
        assert type(self.library.load_scene(player_state)) == Scene

    def test_can_return_scene_map(self):
        player_state = self.library.init_story("basic")
        player_state = self.library.play(player_state)
        scene_map = self.library.scene_map(player_state)
        assert "####" in scene_map

    def test_play_will_update_the_starting_location(self):
        player_state = self.library.init_story("basic")
        old_x = player_state["location"]["x"]
        old_y = player_state["location"]["y"]

        player_state = self.library.play(player_state)
        new_x = player_state["location"]["x"]
        new_y = player_state["location"]["y"]

        assert new_x != old_x
        assert new_y != old_y

    def test_move_will_move_a_player_north(self):
        player_state = self.library.init_story("basic")
        old_x = player_state["location"]["x"]
        old_y = player_state["location"]["y"]

        player_state = self.library.move(player_state, "n")
        new_x = player_state["location"]["x"]
        new_y = player_state["location"]["y"]

        assert new_x == old_x
        assert new_y == old_y + 1

    def test_move_will_move_a_player_south(self):
        player_state = self.library.init_story("basic")
        player_state["location"]["x"] = 3
        player_state["location"]["y"] = 2

        player_state = self.library.move(player_state, "s")
        new_x = player_state["location"]["x"]
        new_y = player_state["location"]["y"]

        assert new_x == 3
        assert new_y == 1

    def test_move_will_move_a_player_east(self):
        player_state = self.library.init_story("basic")
        old_x = player_state["location"]["x"]
        old_y = player_state["location"]["y"]

        player_state = self.library.move(player_state, "e")
        new_x = player_state["location"]["x"]
        new_y = player_state["location"]["y"]

        assert new_x == old_x + 1
        assert new_y == old_y

    def test_move_will_move_a_player_west(self):
        player_state = self.library.init_story("basic")
        player_state["location"]["x"] = 3
        player_state["location"]["y"] = 0

        player_state = self.library.move(player_state, "w")
        new_x = player_state["location"]["x"]
        new_y = player_state["location"]["y"]

        assert new_x == 2
        assert new_y == 0

    def test_move_accepts_an_optional_repetiton(self):
        player_state = self.library.init_story("basic")
        old_x = player_state["location"]["x"]
        old_y = player_state["location"]["y"]

        player_state = self.library.move(player_state, "e", 2)
        new_x = player_state["location"]["x"]
        new_y = player_state["location"]["y"]

        assert new_x == old_x + 2
        assert new_y == old_y    





