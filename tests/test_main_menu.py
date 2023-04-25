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
from SuperMarioLevel1.data.states.main_menu import Menu

class TestMainMenu(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        setup.SCREEN = MagicMock()  # this is so line 69 in level1.py doesn't cause an error

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self) -> None:
        self.menu = Menu()

    def test_init(self):
        self.assertIsInstance(self.menu, Menu)

    def test_update(self):
        surface = MagicMock()
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }
        with patch.object(self.menu, 'update_cursor') as mock_update_cursor:
            self.menu.update(surface,keys,0)
            mock_update_cursor.assert_called_once_with(keys)
            self.assertEqual(self.menu.current_time, 0)
            self.assertEqual(self.menu.game_info[c.CURRENT_TIME], 0)

    def test_update_cursor_case_1(self):
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False,
            pg.K_DOWN: True,
            pg.K_RETURN: True
        }
        self.menu.cursor.state = c.PLAYER1
        self.menu.update_cursor(keys)
        self.assertEqual(self.menu.cursor.rect.y, 358)
        self.assertEqual(self.menu.cursor.state, c.PLAYER2)
        self.assertTrue(self.menu.done)

    def test_update_cursor_case_2(self):
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False,
            pg.K_UP: True,
            pg.K_RETURN: True
        }
        self.menu.cursor.state = c.PLAYER2
        self.menu.update_cursor(keys)
        self.assertEqual(self.menu.cursor.rect.y, 403)
        self.assertEqual(self.menu.cursor.state, c.PLAYER1)

    def test_reset_game_info(self):
        self.menu.reset_game_info()
        self.assertEqual(self.menu.game_info[c.COIN_TOTAL], self.menu.game_info[c.SCORE], 0)
        self.assertEqual(self.menu.game_info[c.LIVES], 3)
        self.assertEqual(self.menu.game_info[c.CURRENT_TIME], 0.0)
        self.assertEqual(self.menu.persist, self.menu.game_info)