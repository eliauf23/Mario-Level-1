import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.states.level1 import Level1
import SuperMarioLevel1.data.setup as setup
import SuperMarioLevel1.data.tools as tools
from SuperMarioLevel1.data.states.load_screen import LoadScreen
from SuperMarioLevel1.data.states.load_screen import GameOver
from SuperMarioLevel1.data.states.load_screen import TimeOut
from data.components import score, bricks, castle_flag
from data.components.powerups import LifeMushroom, Mushroom, Star, FireBall
from data.components.score import Score

# This is a test class for the LoadScreen class in /data/states/load_screen.py.
# This class represents the loading screen of the game.
# There is at least one test for each LoadScreen method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestLoadScreen(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        setup.SCREEN = MagicMock()  # this is so line 69 in level1.py doesn't cause an error

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self) -> None:
        self.load_screen = LoadScreen()

    def test_init(self):
        self.assertIsInstance(self.load_screen, LoadScreen)

    def test_startup(self):
        persist = {
            c.COIN_TOTAL: 0,
        c.LIVES: 3,
        c.TOP_SCORE: 0}
        self.load_screen.startup(0, persist)
        self.assertEqual(self.load_screen.start_time, 0)
        self.assertEqual(self.load_screen.persist, persist)
        self.assertEqual(self.load_screen.game_info, persist)
        self.assertEqual(self.load_screen.next, c.LEVEL1)

    def test_update_case_1(self):
        surface = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        persist = {
            c.COIN_TOTAL: 0,
            c.LIVES: 3,
            c.TOP_SCORE: 0}
        self.load_screen.startup(0, persist)
        with patch.object(self.load_screen.overhead_info, 'update') as mock_update:
            self.load_screen.update(surface, keys, 0)
            mock_update.assert_called_once_with(self.load_screen.game_info)

    def test_update_case_2(self):
        surface = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        persist = {
            c.COIN_TOTAL: 0,
            c.LIVES: 3,
            c.TOP_SCORE: 0}
        self.load_screen.startup(0, persist)
        surface.fill = MagicMock()
        self.load_screen.start_time = 1
        with patch.object(surface, 'fill') as mock_fill:
            self.load_screen.update(surface, keys, 2600)
            mock_fill.assert_called_once_with(c.BLACK)

    def test_update_case_3(self):
        surface = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        persist = {
            c.COIN_TOTAL: 0,
            c.LIVES: 3,
            c.TOP_SCORE: 0}
        self.load_screen.startup(0, persist)
        surface.fill = MagicMock()
        self.load_screen.start_time = 1
        with patch.object(surface, 'fill') as mock_fill:
            self.load_screen.update(surface, keys, 2635)
            mock_fill.assert_called_once_with((106, 150, 252))

    def test_update_case_4(self):
        surface = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        persist = {
            c.COIN_TOTAL: 0,
            c.LIVES: 3,
            c.TOP_SCORE: 0}
        self.load_screen.startup(0, persist)
        surface.fill = MagicMock()
        self.load_screen.start_time = 1
        self.load_screen.update(surface, keys, 2636)
        self.assertTrue(self.load_screen.done)

# This is a test class for the GameOver class in /data/states/load_screen.py.
# This class represents A loading screen with Game Over.
# There is at least one test for each GameOver method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestGameOver(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        setup.SCREEN = MagicMock()  # this is so line 69 in level1.py doesn't cause an error

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self) -> None:
        self.game_over = GameOver()

    def test_init(self):
        self.assertIsInstance(self.game_over, GameOver)

    def test_set_next_state(self):
        test = self.game_over.set_next_state()
        self.assertEqual(test, c.MAIN_MENU)

    def test_set_overhead_info_state(self):
        test = self.game_over.set_overhead_info_state()
        self.assertEqual(test, c.GAME_OVER)

    def test_update_case_1(self):
        surface = MagicMock()
        surface.fill = MagicMock()
        self.game_over.sound_manager = MagicMock()
        self.game_over.overhead_info = MagicMock()
        self.game_over.game_info = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        self.game_over.start_time = 1
        with patch.object(surface, 'fill') as mock_fill:
            self.game_over.update(surface, keys, 7000)
            mock_fill.assert_called_once_with(c.BLACK)

    def test_update_case_2(self):
        surface = MagicMock()
        surface.fill = MagicMock()
        self.game_over.sound_manager = MagicMock()
        self.game_over.overhead_info = MagicMock()
        self.game_over.game_info = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        self.game_over.start_time = 1
        with patch.object(surface, 'fill') as mock_fill:
            self.game_over.update(surface, keys, 7200)
            mock_fill.assert_called_once_with(c.BLACK)

    def test_update_case_3(self):
        surface = MagicMock()
        surface.fill = MagicMock()
        self.game_over.sound_manager = MagicMock()
        self.game_over.overhead_info = MagicMock()
        self.game_over.game_info = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        self.game_over.start_time = 1
        with patch.object(surface, 'fill') as mock_fill:
            self.game_over.update(surface, keys, 7235)
            mock_fill.assert_called_once_with((106, 150, 252))

    def test_update_case_4(self):
        surface = MagicMock()
        surface.fill = MagicMock()
        self.game_over.sound_manager = MagicMock()
        self.game_over.overhead_info = MagicMock()
        self.game_over.game_info = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        self.game_over.start_time = 1
        with patch.object(surface, 'fill') as mock_fill:
            self.game_over.update(surface, keys, 8000)
            self.assertTrue(self.game_over.done)

# This is a test class for the TimeOut class in /data/states/load_screen.py.
# This class represents A Loading Screen with Time Out.
# There is at least one test for each TimeOut method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestTimeOut(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        setup.SCREEN = MagicMock()  # this is so line 69 in level1.py doesn't cause an error

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self) -> None:
        self.time_out = TimeOut()

    def test_init(self):
        self.assertIsInstance(self.time_out, TimeOut)

    def test_set_next_state_case_1(self):
        self.time_out.persist[c.LIVES] = 0
        self.assertEqual(self.time_out.set_next_state(), c.GAME_OVER)

    def test_set_next_state_case_2(self):
        self.time_out.persist[c.LIVES] = 1
        self.assertEqual(self.time_out.set_next_state(), c.LOAD_SCREEN)

    def test_set_overhead_info_state(self):
        self.assertEqual(self.time_out.set_overhead_info_state(), c.TIME_OUT)

    def test_update_case_1(self):
        surface = MagicMock()
        surface.fill = MagicMock()
        self.time_out.overhead_info = MagicMock()
        self.time_out.game_info = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        self.time_out.start_time = 1
        with patch.object(surface, 'fill') as mock_fill:
            self.time_out.update(surface, keys, 2400)
            mock_fill.assert_called_once_with(c.BLACK)

    def test_update_case_2(self):
        surface = MagicMock()
        surface.fill = MagicMock()
        self.time_out.overhead_info = MagicMock()
        self.time_out.game_info = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        self.time_out.start_time = 1
        with patch.object(surface, 'fill') as mock_fill:
            self.time_out.update(surface, keys, 2500)
            self.assertTrue(self.time_out.done)