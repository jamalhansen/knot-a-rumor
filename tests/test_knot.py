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
 
    def set_location(self, state, x, y):
        state["location"]["x"] = x
        state["location"]["y"] = y
        return state

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
        state = self.library.init_story("basic")
        assert type(state) is dict

    def test_play_accepts_and_returns_a_dict(self):
        state = self.library.init_story("basic")
        state = self.library.play(state)
        assert type(state) is dict

    def test_narrate_returns_a_description_of_the_scene(self):
        state = self.library.init_story("basic")
        description = self.library.narrate(state)
        assert "This is a basic description of a basic scene" == description

    def test_narrate_returns_a_positional_description_of_the_scene(self):
        state = self.library.init_story("basic")
        state = self.set_location(state, 3, 2)
        description = self.library.narrate(state)
        assert "You are at the upper right." == description

    def test_state_contains_the_current_scene(self):
        state = self.library.init_story("basic")
        assert "flourescent" == state["current_scene"]

    def test_state_contains_things_seen(self):
        state = self.library.init_story("basic")
        assert "seen" in state.keys()

    def test_state_contains_the_inventory(self):
        state = self.library.init_story("basic")
        assert "inventory" in state.keys()

    def test_state_contains_location(self):
        state = self.library.init_story("basic")
        assert "location" in state.keys()
        assert "x" in state["location"].keys()
        assert "y" in state["location"].keys()

    def test_state_contains_the_current_story(self):
        state = self.library.init_story("basic")
        assert "basic" == state["story"]

    def test_state_contains_the_number_of_turns_played(self):
        state = self.library.init_story("basic")
        assert 0 == state["turn"]
        state = self.library.move(state, "e")
        assert 1 == state["turn"]
        state = self.library.move(state, "e")
        assert 2 == state["turn"]

    def test_load_scene_returns_scene(self):
        state = self.library.init_story("basic")
        assert type(self.library.load_scene(state)) == Scene

    def test_can_return_scene_map(self):
        state = self.library.init_story("basic")
        state = self.library.play(state)
        scene_map = self.library.scene_map(state)
        assert "####" in scene_map

    def test_play_will_update_the_starting_location(self):
        state = self.library.init_story("basic")
        old_x = state["location"]["x"]
        old_y = state["location"]["y"]

        state = self.library.play(state)
        new_x = state["location"]["x"]
        new_y = state["location"]["y"]

        assert new_x != old_x
        assert new_y != old_y

    def test_move_will_move_a_player_north(self):
        state = self.library.init_story("basic")
        old_x = state["location"]["x"]
        old_y = state["location"]["y"]

        state = self.library.move(state, "n")
        new_x = state["location"]["x"]
        new_y = state["location"]["y"]

        assert new_x == old_x
        assert new_y == old_y + 1

    def test_move_will_move_a_player_south(self):
        state = self.library.init_story("basic")
        state["location"]["x"] = 3
        state["location"]["y"] = 2

        state = self.library.move(state, "s")
        new_x = state["location"]["x"]
        new_y = state["location"]["y"]

        assert new_x == 3
        assert new_y == 1

    def test_move_will_move_a_player_east(self):
        state = self.library.init_story("basic")
        old_x = state["location"]["x"]
        old_y = state["location"]["y"]

        state = self.library.move(state, "e")
        new_x = state["location"]["x"]
        new_y = state["location"]["y"]

        assert new_x == old_x + 1
        assert new_y == old_y

    def test_move_will_move_a_player_west(self):
        state = self.library.init_story("basic")
        state["location"]["x"] = 3
        state["location"]["y"] = 0

        state = self.library.move(state, "w")
        new_x = state["location"]["x"]
        new_y = state["location"]["y"]

        assert new_x == 2
        assert new_y == 0

    def test_move_accepts_an_optional_repetiton(self):
        state = self.library.init_story("basic")
        old_x = state["location"]["x"]
        old_y = state["location"]["y"]

        state = self.library.move(state, "e", 2)
        new_x = state["location"]["x"]
        new_y = state["location"]["y"]

        assert new_x == old_x + 2
        assert new_y == old_y    

    def test_player_can_look_to_see_items_on_map(self):
        state = self.library.init_story("basic")
        state = self.library.play(state)
        scene_map = self.library.scene_map(state)
        assert "#@d#" not in scene_map
        assert 1 not in state["seen"]

        state, seen = self.library.look(state)
        assert "dog" in seen
        assert 1 in state["seen"]

        scene_map = self.library.scene_map(state)
        assert "#@d#" in scene_map

    def test_player_cannot_take_an_item_they_do_not_share_a_space_with(self):
        state = self.library.init_story("basic")
        state = self.library.play(state)
        state, seen = self.library.look(state)
        state, success = self.library.take(state)
        assert success == False
        assert "dog" not in state["inventory"]

    def test_player_cannot_take_an_item_they_have_not_seen(self):
        state = self.library.init_story("basic")
        state = self.library.play(state)
        state = self.library.move(state, "e")
        state, success = self.library.take(state)
        assert success == False
        assert "dog" not in state["inventory"]

    def test_player_can_take_an_item_they_have_seen_and_share_a_space_with(self):
        state = self.library.init_story("basic")
        state = self.library.play(state)
        state, seen = self.library.look(state)
        assert "dog" in seen
        self.set_location(state, 2, 2)
        state, success = self.library.take(state)
        assert success == True
        assert "dog" in state["inventory"]


