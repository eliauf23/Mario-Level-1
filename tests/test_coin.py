from unittest import TestCase
from unittest.mock import MagicMock, patch
import pygame as pg
from SuperMarioLevel1.data.components.coin import Coin
from SuperMarioLevel1.data import constants as c


class TestCoin(TestCase):
    def setUp(self):
        pg.init()
        self.score_group = []
        self.coin = Coin(100, 100, self.score_group)

    def test_coin_init(self):
        self.assertIsInstance(self.coin.image, pg.Surface)
        self.assertIsInstance(self.coin.rect, pg.Rect)
        self.assertEqual(self.coin.rect.centerx, 100)
        self.assertEqual(self.coin.rect.bottom, 95)
        self.assertEqual(self.coin.y_vel, -15)
        self.assertEqual(self.coin.state, c.SPIN)
        self.assertEqual(self.coin.score_group, self.score_group)

    def test_coin_update(self):
        with patch('SuperMarioLevel1.data.components.coin.Coin.spinning') as mock_spinning:
            game_info = {c.CURRENT_TIME: 10}
            viewport = MagicMock()
            self.coin.update(game_info, viewport)
            mock_spinning.assert_called_once()

    def test_spinning(self):
        initial_rect_bottom = self.coin.rect.bottom
        self.coin.current_time = 100
        self.coin.animation_timer = 0
        self.coin.spinning()
        self.assertNotEqual(self.coin.rect.bottom, initial_rect_bottom)
        # TODO: check this
        self.assertGreater(self.coin.rect.bottom, initial_rect_bottom - 15)

