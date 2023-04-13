import pygame as pg
from unittest.mock import MagicMock, patch, Mock
from SuperMarioLevel1.data.components.info import OverheadInfo
import SuperMarioLevel1.data.constants as c
from unittest import TestCase

class TestOverheadInfo(TestCase):
    def setUp(self):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.game_info = {c.COIN_TOTAL: 0, c.LIVES: 3, c.TOP_SCORE: 0}
        self.overhead_info = OverheadInfo(self.game_info, state=c.MAIN_MENU)

    def tearDown(self) -> None:
        pg.quit()

    def test_init(self):
        self.assertEqual(self.overhead_info.state, c.MAIN_MENU)
        self.assertEqual(self.overhead_info.game_info, self.game_info)
        self.assertEqual(self.overhead_info.coin_total, 0)
        self.assertEqual(self.overhead_info.top_score, 0)
        self.assertEqual(self.overhead_info.total_lives, self.game_info[c.LIVES])
        self.assertEqual(self.overhead_info.time, 401)
        self.assertEqual(self.overhead_info.state, c.MAIN_MENU)
