from unittest import TestCase
from unittest.mock import MagicMock, patch
import pygame as pg
from SuperMarioLevel1.data.components.coin import Coin
from SuperMarioLevel1.data import constants as c
from SuperMarioLevel1.data.components.score import Score
import numpy


class TestCoin(TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
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

    #     # TODO: check this
    #     self.assertGreater(self.coin.rect.bottom, initial_rect_bottom - 15)

    def test_spinning_state(self):
        # Save initial values
        initial_height = self.coin.rect.bottom
        initial_frame_index = self.coin.frame_index
        initial_image = self.coin.image.copy()
        # Set up required mocks
        with patch('SuperMarioLevel1.data.components.score.Score') as mock_score:
            # game_info = {c.CURRENT_TIME: 100}
            viewport = MagicMock()
            self.coin.viewport = viewport
            # Test image assignment and frame index increment
            self.coin.current_time = 100
            self.coin.animation_timer = 0
            self.coin.spinning()
            # self.assertEqual(self.coin.frames[initial_frame_index + 1], self.coin.image)
            s1 = self.coin.frames[initial_frame_index + 1]
            s2 = self.coin.image
            self.assertEqual(s1.get_parent(), s2.get_parent())
            self.assertEqual(s1.get_offset(), s2.get_offset())
            self.assertEqual(initial_frame_index + 1, self.coin.frame_index)


    def test_get_image_different_values(self):
        img1 = self.coin.get_image(0, 0, 8, 14)
        img2 = self.coin.get_image(52, 113, 8, 14)
        self.assertFalse((pg.surfarray.array3d(img1) == pg.surfarray.array3d(img2)).all())

    def test_setup_frames_all_different(self):
        unique_frames = len(
            {
                tuple(pg.surfarray.array3d(frame).flatten())
                for frame in self.coin.frames
            }
        )
        self.assertEqual(unique_frames, len(self.coin.frames))

    def test_update_different_game_info_viewport(self):
        game_info1 = {c.CURRENT_TIME: 10}
        game_info2 = {c.CURRENT_TIME: 20}
        viewport1 = pg.Rect(0, 0, 800, 600)
        viewport2 = pg.Rect(0, 0, 1600, 1200)
        with patch('SuperMarioLevel1.data.components.coin.Coin.spinning') as mock_spinning:
            self.coin.update(game_info1, viewport1)
            mock_spinning.assert_called_once()
            mock_spinning.reset_mock()
            self.coin.update(game_info2, viewport2)
            mock_spinning.assert_called_once()

    def test_spinning_kill_and_append_score(self):
        # Set rect.bottom to be greater than initial_height
        self.coin.initial_height = 100
        self.coin.rect.bottom = self.coin.initial_height + 50
        with patch('SuperMarioLevel1.data.components.coin.Coin.kill') as mock_kill:
            with patch('SuperMarioLevel1.data.components.score.Score') as mock_score:
                # Set required attributes
                self.coin.current_time = 100
                self.coin.animation_timer = 0
                viewport = MagicMock()
                self.coin.viewport = viewport
                # Call spinning method
                self.coin.spinning()
                # Check if kill method was called and a score was appended to the score_group
                mock_kill.assert_called_once()
                mock_score.assert_called_once_with(
                    self.coin.rect.centerx - self.coin.viewport.x,
                    self.coin.rect.y,
                    200
                )
                self.assertIn(mock_score.return_value, self.score_group)

    def test_spinning_frame_index_not_updated(self):
        self.coin.frames = [1, 2, 3, 4, 5]
        self.coin.frame_index = 4
        self.coin.current_time = 120
        self.coin.animation_timer = 30
        self.assertGreater((self.coin.current_time - self.coin.animation_timer), 80)
        self.assertFalse(self.coin.frame_index < 3)
        self.coin.spinning()
        self.assertEqual(self.coin.frame_index, 0)
