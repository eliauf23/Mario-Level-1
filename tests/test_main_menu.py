from unittest import TestCase
from unittest.mock import MagicMock, patch

import pygame as pg

import SuperMarioLevel1.data.constants as c
import SuperMarioLevel1.data.setup as setup
import SuperMarioLevel1.data.tools as tools
from SuperMarioLevel1.data.states.main_menu import Menu


# This is a test class for the Menu class in /data/states/main_menu.py.
# This class represents the main menu of the game.
# There is at least one test for each Menu method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
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
            self.menu.update(surface, keys, 0)
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
