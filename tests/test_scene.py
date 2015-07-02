import pytest
from knot_a_rumor.story import Scene 
from os import getcwd
from os.path import join

@pytest.mark.usefixtures("load_scene")
class TestScene:

    @pytest.fixture()
    def load_scene(self, story_name, scene_name):
        self.path = join(getcwd(), "tests", "fixtures", "library", story_name)
        self.scene = Scene(self.path, scene_name)

    @pytest.fixture()
    def story_name(self):
        return "basic"

    @pytest.fixture()
    def scene_name(self):
        return "flourescent"
   
    def test_scene_has_a_name(self):
        assert "Flourescent" == self.scene.name

    def test_scene_filename_adds_dot_yaml(self):
        assert ".yaml" in self.scene.filename("foo", "bar")

    def test_scene_has_a_narration(self):
        narration = "This is a basic description of a basic scene"
        assert narration == self.scene.narration

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
        assert scene_map == self.scene.build_map(1, 2)

    def test_can_move_will_validate_move_north_when_invalid(self):
        assert False == self.scene.valid_move(1, 2, "n", 1)

    def test_valid_move_doesnt_accept_invalid_directions(self):
        assert False == self.scene.valid_move(1, 2, "ewio", 1)
        assert False == self.scene.valid_move(1, 2, False, 1)
        assert False == self.scene.valid_move(1, 2, "o", 1)
        assert False == self.scene.valid_move(1, 2, 1, 1)

    def test_valid_move_doesnt_accept_invalid_times(self):
        assert False == self.scene.valid_move(1, 2, "n", 0)
        assert False == self.scene.valid_move(1, 2, "n", -1)
        assert False == self.scene.valid_move(1, 2, "n", "n")
        assert False == self.scene.valid_move(1, 2, "n", 101)

    def test_valid_move_accepts_valid_moves(self):
        assert self.scene.valid_move(1, 2, "w", 1)
        assert self.scene.valid_move(1, 2, "e", 1)
        assert self.scene.valid_move(0, 2, "s", 1)
        assert self.scene.valid_move(0, 1, "n", 1)
        assert self.scene.valid_move(0, 2, "s", 3)
        assert self.scene.valid_move(0, 0, "e", 3)
        assert self.scene.valid_move(3, 0, "n", 3)
        assert self.scene.valid_move(3, 2, "w", 3)

    # next prevent going through walls
