import pytest
from knot_a_rumor.story import Scene 
from os import getcwd
from os.path import join

@pytest.mark.usefixtures("load_scene")
class TestScene:

    @pytest.fixture()
    def load_scene(self, basic_state):
        story_name = basic_state["story"]
        self.path = join(getcwd(), "tests", "fixtures", "library", story_name)
        self.scene = Scene(self.path, basic_state)

    @pytest.fixture()
    def basic_state(self):
        starting_state = {
            "story": "basic",
            "current_scene": "flourescent",
            "seen": []
            }
        return starting_state

    def test_scene_has_a_name(self):
        assert "Flourescent" == self.scene.name

    def test_scene_filename_adds_dot_yaml(self):
        assert ".yaml" in self.scene.filename("foo", "bar")

    def test_scene_has_a_narration(self):
        narration = "This is a basic description of a basic scene"
        assert narration == self.scene.narration

    def test_scene_has_views(self):
        assert len(self.scene.views) > 0

    def test_scene_view_has_name_location_and_narration(self):
        assert "upper right" in self.scene.views.keys()
        assert self.scene.views["upper right"]["x"] == 3
        assert self.scene.views["upper right"]["y"] == 2
        assert "You are at the" in self.scene.views["upper right"]["narration"]

    def test_can_retrieve_locational_view(self):
        narration = self.scene.view({"x":3, "y":2})
        assert "You are at the" in narration

    def test_scene_has_a_map(self):
        rows = [
            "####",
            "#  #",
            "####"
            ]

        scene_map = "\n".join(rows)
        assert scene_map == self.scene.scene_map

    def test_scene_has_initial_location(self):
        assert 1 == self.scene.start["x"]
        assert 2 == self.scene.start["y"]

    def test_scene_will_build_map_with_character(self):
        rows = [
            "#@##",
            "#  #",
            "####"
            ]

        scene_map = "\n".join(rows)
        state = {"location": {"x":1, "y":2}, "seen": []}
        assert scene_map == self.scene.build_map(state)

    def test_can_move_will_validate_move_north_when_invalid(self):
        assert not self.scene.valid_move({"x":1, "y":2}, "n", 1)

    def test_valid_move_doesnt_accept_invalid_directions(self):
        assert not self.scene.valid_move({"x":1, "y":2}, "ewio", 1)
        assert not self.scene.valid_move({"x":1, "y":2}, False, 1)
        assert not self.scene.valid_move({"x":1, "y":2}, "o", 1)
        assert not self.scene.valid_move({"x":1, "y":2}, 1, 1)

    def test_valid_move_doesnt_accept_invalid_times(self):
        assert not self.scene.valid_move({"x":1, "y":2}, "n", 0)
        assert not self.scene.valid_move({"x":1, "y":2}, "n", -1)
        assert not self.scene.valid_move({"x":1, "y":2}, "n", "n")
        assert not self.scene.valid_move({"x":1, "y":2}, "n", 101)

    def test_valid_move_accepts_valid_moves(self):
        assert self.scene.valid_move({"x":1, "y":2}, "w", 1)
        assert self.scene.valid_move({"x":1, "y":2}, "e", 1)
        assert self.scene.valid_move({"x":0, "y":2}, "s", 1)
        assert self.scene.valid_move({"x":0, "y":1}, "n", 1)
        assert self.scene.valid_move({"x":0, "y":2}, "s", 2)
        assert self.scene.valid_move({"x":0, "y":0}, "e", 3)
        assert self.scene.valid_move({"x":3, "y":0}, "n", 2)
        assert self.scene.valid_move({"x":3, "y":2}, "w", 3)

    def test_valid_move_does_not_accept_invalid_moves(self):
        assert not self.scene.valid_move({"x":1, "y":2}, "n", 1)
        assert not self.scene.valid_move({"x":1, "y":2}, "s", 1)
        assert not self.scene.valid_move({"x":0, "y":2}, "w", 1)
        assert not self.scene.valid_move({"x":0, "y":1}, "e", 1)
        assert not self.scene.valid_move({"x":0, "y":2}, "s", 3)
        assert not self.scene.valid_move({"x":0, "y":0}, "e", 4)
        assert not self.scene.valid_move({"x":3, "y":0}, "n", 3)
        assert not self.scene.valid_move({"x":3, "y":2}, "w", 4)

    def test_scene_has_items(self):
        assert len(self.scene.items.keys()) > 0

    def test_scene_has_a_level_number(self):
        assert self.scene.level == 1

    def test_scene_has_a_look_method(self):
        state, view = self.scene.look({"seen": []})
        assert "dog" in view
        assert 1 in state["seen"]

    def test_scene_can_describe_items(self):
        state = {"seen": [1]}
        state, description = self.scene.describe(state, "d")
        assert "A small dog" == description

    def test_scene_cannot_describe_items_before_seen(self):
        state = {"seen": []}
        state, description = self.scene.describe(state, "d")
        assert None == description
        
    def test_items_are_not_taken_when_location_is_empty(self):
        state = {"inventory": [], "location": {"x":1, "y":2}, "seen": []}
        state = self.scene.take(state)
        assert "dog" not in state["inventory"]

    def test_items_are_taken_when_location_is_not_empty_and_item_is_not_seen(self):
        state = {"inventory": [], "location": {"x":2, "y":2}, "seen": []}
        state = self.scene.take(state)
        assert "dog" not in state["inventory"]

    def test_items_are_taken_when_location_is_not_empty_and_item_is_seen(self):
        state = {"inventory": [], "location": {"x":2, "y":2}, "seen": [1]}
        state = self.scene.take(state)
        assert "dog" in state["inventory"]

    def test_returns_no_items_at_empty_location(self):
        items = self.scene.items_at(1,2)
        assert len(items) == 0

    def test_returns_items_at_a_location(self):
        items = self.scene.items_at(2,2)
        assert len(items) == 1

    def test_items_at_returns_key_value_pair(self):
        items = self.scene.items_at(2,2)
        assert items[0][0] == "dog"
        assert items[0][1]["x"] == 2
        assert items[0][1]["y"] == 2
