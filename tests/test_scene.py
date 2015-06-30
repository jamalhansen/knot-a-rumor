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
