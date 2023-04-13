from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock
import pygame as pg
from SuperMarioLevel1.data.components.coin_box import Coin_box
import SuperMarioLevel1.data.constants as c


class TestCoinBox(TestCase):
    def setUp(self):
        pg.init()
        self.group = pg.sprite.Group()
        self.coin_box = Coin_box(100, 100, contents='coin', group=self.group)




    def test_coin_box_init(self):
        self.assertIsInstance(self.coin_box.image, pg.Surface)
        self.assertIsInstance(self.coin_box.rect, pg.Rect)
        self.assertEqual(self.coin_box.rect.x, 100)
        self.assertEqual(self.coin_box.rect.y, 100)
        self.assertEqual(self.coin_box.contents, 'coin')
        self.assertEqual(self.coin_box.state, c.RESTING)

    def test_coin_box_update(self):
        with patch('SuperMarioLevel1.data.components.coin_box.Coin_box.handle_states') as mock_handle_states:
            game_info = {c.CURRENT_TIME: 10}
            self.coin_box.update(game_info)
            mock_handle_states.assert_called_once()

    def test_resting(self):
        # call update to set current time
        game_info = {c.CURRENT_TIME: 10}
        self.coin_box.update(game_info)
        # test resting
        self.coin_box.resting()
        self.assertIn(self.coin_box.frame_index, [0, 1, 2])

    def test_start_bump(self):
        with patch('SuperMarioLevel1.data.setup.SFX') as mock_sfx:
            mock_sfx['coin'] = MagicMock()
            mock_sfx['powerup_appears'] = MagicMock()
            score_group = []
            self.coin_box.start_bump(score_group)
            self.assertEqual(self.coin_box.state, c.BUMPED)
            self.assertEqual(self.coin_box.y_vel, -6)
            mock_sfx['coin'].play.assert_called_once()

    def test_bumped(self):
        self.coin_box.state = c.BUMPED
        self.coin_box.y_vel = -6
        self.coin_box.gravity = 1.2
        self.coin_box.bumped()
        self.assertNotEqual(self.coin_box.rect.y, 100)

    def test_opened(self):
        # Placeholder for OPENED state, nothing to test
        pass