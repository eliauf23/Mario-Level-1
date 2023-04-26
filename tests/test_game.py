import os
import unittest
from unittest import TestCase
import pygame as pg
from unittest.mock import MagicMock, patch
from SuperMarioLevel1.data.tools import Control, _State, keybinding, load_all_gfx, load_all_music, load_all_fonts, load_all_sfx
import SuperMarioLevel1.data.constants as c

# This is a test class for the Control class in /data/tools.py.
# This class represents the Control class for entire project. Contains the game loop, and contains
#     the event_loop which passes events to States as needed. Logic for flipping
#     states is also found here.
# There is at least one test for each Control method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestControl(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((800, 600))

    def setUp(self):
        self.control = Control("Test Caption")

    def test_init(self):
        self.assertFalse(self.control.done)
        self.assertEqual(self.control.caption, "Test Caption")
        self.assertEqual(self.control.fps, 60)
        self.assertFalse(self.control.show_fps)
        self.assertEqual(self.control.current_time, 0.0)

    def test_setup_states(self):
        state_dict = {'example_state': _State()}
        self.control.setup_states(state_dict, 'example_state')
        self.assertEqual(self.control.state_dict, state_dict)
        self.assertEqual(self.control.state_name, 'example_state')
        self.assertEqual(self.control.state, state_dict['example_state'])

    def test_flip_state(self):
        state_dict = {'state1': _State(), 'state2': _State()}
        self.control.setup_states(state_dict, 'state1')
        self.control.state.done = True
        self.control.state.next = 'state2'
        self.control.flip_state()
        self.assertEqual(self.control.state_name, 'state2')
        self.assertEqual(self.control.state, state_dict['state2'])

    def test_toggle_show_fps(self):
        self.control.toggle_show_fps(pg.K_F5)
        self.assertTrue(self.control.show_fps)
        self.control.toggle_show_fps(pg.K_F5)
        self.assertFalse(self.control.show_fps)

# This is a test class for the _State class in /data/tools.py.
# This class represents the state of the game at the current time.
# There is at least one test for each _State method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestState(TestCase):
    def setUp(self):
        self.state = _State()

    def test_init(self):
        self.assertEqual(self.state.start_time, 0.0)
        self.assertEqual(self.state.current_time, 0.0)
        self.assertFalse(self.state.done)
        self.assertFalse(self.state.quit)
        self.assertIsNone(self.state.next)
        self.assertIsNone(self.state.previous)
        self.assertEqual(self.state.persist, {})

    def test_cleanup(self):
        self.state.done = True
        result = self.state.cleanup()
        self.assertFalse(self.state.done)
        self.assertEqual(result, self.state.persist)

    def test_get_event(self):
        self.state.get_event(pg.event.Event(pg.QUIT))
        # TODO: how is this broken lol
        self.assertTrue(self.state.quit)

    def test_update(self):
        self.state.update(None, None, None)

    def test_cleanup(self):
        self.assertEqual(self.state.cleanup(), {})

    def test_startup(self):
        self.state.startup(None, None)

# This is a test class for the various load functions in /data/tools.py.
# These load functions load gfx, sfx, fonts, and music.
# There is at least one test for each of these methods, asserting that the correct values were modified and the correct
# methods were called.
class TestLoadFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    def setUp(self):
        self.control = Control("Test Caption")
    @patch('os.listdir')
    @patch('pygame.image.load')
    def test_load_all_gfx(self, mock_pg_image_load, mock_os_listdir):
        mock_os_listdir.return_value = ['image.png']
        mock_pg_image_load.return_value = pg.Surface((2, 2))

        result = load_all_gfx('path/to/gfx')
        self.assertIn('image', result)
        self.assertIsInstance(result['image'], pg.Surface)

    @patch('os.listdir')
    def test_load_all_music(self, mock_os_listdir):
        mock_os_listdir.return_value = ['song.mp3']

        result = load_all_music('path/to/music')
        self.assertIn('song', result)
        self.assertEqual(result['song'], 'path/to/music/song.mp3')

    @patch('os.listdir')
    def test_load_all_fonts(self, mock_os_listdir):
        mock_os_listdir.return_value = ['font.ttf']

        result = load_all_fonts('path/to/fonts')
        self.assertIn('font', result)
        self.assertEqual(result['font'], 'path/to/fonts/font.ttf')

    @patch('os.listdir')
    @patch('pygame.mixer.Sound')
    def test_load_all_sfx(self, mock_pg_mixer_sound, mock_os_listdir):
        mock_os_listdir.return_value = ['effect.wav']
        sound_instance = MagicMock(spec=pg.mixer.Sound)
        mock_pg_mixer_sound.return_value = sound_instance

        result = load_all_sfx('path/to/sfx')
        self.assertIn('effect', result)
        self.assertIsInstance(result['effect'], MagicMock)