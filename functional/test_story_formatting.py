import pytest
from knot_a_rumor.knot import Knot
from os import getcwd
from os.path import join

@pytest.mark.usefixtures("load_library")
class TestPennyCanInspectAStory:

    @pytest.fixture()
    def load_library(self):
        self.library_path =  join(getcwd(), "tests", "fixtures", "library")
        self.pennys_story = "penny-pinnacle-pennyslvania"
        self.library = Knot(self.library_path)
        self.stories = self.library.stories()

    def library_path(self):
        return join(getcwd(), "tests", "fixtures", "library")
    
    def test_penny_can_load_story_info(self):
        # Penny loads up the library
        # Penny lists the stories available(self):
        assert self.pennys_story in self.stories

        # She loads the story
        story = self.library.get_story(self.pennys_story)

        # She checks the author
        assert "Penny Pennington" == story.author

        # She checks the title
        assert "Pen's Pennyslvanian Pinnacle" == story.title

        # She checks the filename for the first scene
        assert "Runaway Train Showdown" == story.scene

        # She checks the story synopsis
        assert "Lorem ipsum" in story.synopsis

        # Satisfied, she goes on her way

    def check_location(self, x, y):
        assert x == self.player_state["location"]["x"]
        assert y == self.player_state["location"]["y"]

    def test_penny_can_view_enter_and_move_around_a_map_stored_in_the_scene(self):
        # Penny returns within minutes, she has not been able to stop thinking about the 
        # possibilities presented by the first scene the Runaway Train Showdown. 
        # Starts the story
        self.player_state = self.library.init_story(self.pennys_story)
        self.player_state = self.library.play(self.player_state)

        # Penny receives a description of the scene.  She is on a railway platform in 
        # Pennyslvania awaiting the arrival of her friend who will be on a train
        setting = self.library.narrate(self.player_state)
        assert "awaiting the arrival of your friend" in setting
        assert "train" in setting

        # Penny asks for and recieves a map from the story.
        scene_map = self.library.scene_map(self.player_state)
        rows = [
            "###############",
            "###############",
            "      #@       "
            ]

        expected = "\n".join(rows)

        self.check_location(7,0)
        assert expected == scene_map

        # Penny moves north once and asks for another map
        self.player_state = self.library.move(self.player_state, 'n')

        scene_map = self.library.scene_map(self.player_state)
        rows = [
            "###############",
            "#######@#######",
            "      ##       "
            ]

        expected = "\n".join(rows)

        self.check_location(7,1)
        assert expected == scene_map

        # Penny moves east seven times and asks for another map
        self.player_state = self.library.move(self.player_state, 'e', 7)

        scene_map = self.library.scene_map(self.player_state)
        rows = [
            "###############",
            "##############@",
            "      ##       "
            ]

        expected = "\n".join(rows)

        self.check_location(14,1)
        assert expected == scene_map

        # Penny tries to move east again but cannot and asks for another map
        self.player_state = self.library.move(self.player_state, 'e')

        scene_map = self.library.scene_map(self.player_state)
        rows = [
            "###############",
            "##############@",
            "      ##       "
            ]

        expected = "\n".join(rows)

        self.check_location(14,1)
        assert expected == scene_map

        # Penny moves north once and asks for another description of the scene 
        self.player_state = self.library.move(self.player_state, 'n')

        scene_map = self.library.scene_map(self.player_state)
        rows = [
            "##############@",
            "###############",
            "      ##       "
            ]

        expected = "\n".join(rows)

        self.check_location(14,2)
        assert expected == scene_map
        setting = self.library.narrate(self.player_state)

        # Penny reads the scene setting and sees that there is a train approaching from western horizon
        assert "western horizon" in setting

        # Penny runs to the western end of the platform and asks for another description
        self.player_state = self.library.move(self.player_state, 'w', 14)

        scene_map = self.library.scene_map(self.player_state)
        rows = [
            "@##############",
            "###############",
            "      ##       "
            ]

        expected = "\n".join(rows)

        self.check_location(0,2)
        assert expected == scene_map
        setting = self.library.narrate(self.player_state)

        # Penny reads in the description that the train with a full head of steam wizzes past her
        # going much faster than it should be
        assert "full head of steam" in setting
        assert "much faster than it should be" in setting

    def test_penny_finds_items_in_the_scene(self):
        # Penny again returns within minutes, she has not been able to stop 
        # thinking about the interactive experience that she has had with the 
        # story.  This time she has decided to stop and look around and examine
        # the platform more closely.

        # Starts the story
        self.player_state = self.library.init_story(self.pennys_story)
        self.player_state = self.library.play(self.player_state)

        # Penny starts the story and uses the 'look' action to view what is 
        # around her.
        self.player_state, seen = self.library.look(self.player_state)

        # She sees a newspaper on the ground.  It is dated today and it 
        # announces that the Governor will be stopping in town today to
        # announce her new controversial policy
        assert "newspaper" in seen


        self.player_state, description = self.library.describe(self.player_state, "n")
        assert "Governor" in description
        assert "policy" in description

        # She now sees the newspaper on the map
        # Looking at the map she also sees something else
        scene_map = self.library.scene_map(self.player_state)
        rows = [
            "###############",
            "##########b####",
            "      n@       "
            ]

        expected = "\n".join(rows)
        assert expected == scene_map

        # She asks for more detail about the item and it informs her that 
        # the location contains a small box, labeled "penny"
        self.player_state, description = self.library.describe(self.player_state, "b")

        assert "small box" in description
        assert "penny" in description
        # Penny quits the game ot ponder the possibilities
