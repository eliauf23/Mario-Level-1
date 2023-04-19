from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock
import pygame as pg
from SuperMarioLevel1.data.components.coin_box import Coin_box
import SuperMarioLevel1.data.constants as c


class TestCoinBox(TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
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

    def test_get_image(self):
        image = self.coin_box.get_image(384, 0, 16, 16)
        self.assertIsInstance(image, pg.Surface)
        self.assertEqual(image.get_width(), int(16 * c.BRICK_SIZE_MULTIPLIER))
        self.assertEqual(image.get_height(), int(16 * c.BRICK_SIZE_MULTIPLIER))

    def test_setup_frames(self):
        self.coin_box.frames = []
        self.coin_box.setup_frames()
        self.assertEqual(len(self.coin_box.frames), 4)
        for frame in self.coin_box.frames:
            self.assertIsInstance(frame, pg.Surface)

    # TODO: check on this setup_timers test
    def test_setup_timers(self):
        self.coin_box.current_time = 0
        self.coin_box.setup_timers()
        self.assertEqual(self.coin_box.animation_timer, 0)
        self.assertEqual(self.coin_box.state_timer, 0)

    def test_bumped_with_mushroom(self):
        coin_box = Coin_box(100, 100, contents='mushroom', group=self.group)
        coin_box.state = c.BUMPED
        coin_box.y_vel = -1
        coin_box.gravity = 1.2
        self.assertEqual(len(coin_box.group), 0)
        coin_box.rect.y = 110
        self.assertEqual(coin_box.rect.y, 110)
        self.assertGreater(coin_box.rect.y, coin_box.rest_height + 5)
        coin_box.bumped()
        self.assertEqual(len(coin_box.group), 1)
        self.assertNotEqual(coin_box.rect.y, 110)  # coin_box should have fallen
        self.assertEqual(coin_box.state, c.OPENED)

    def test_bumped_with_fireflower(self):
        coin_box = Coin_box(100, 100, contents='fireflower', group=self.group)
        coin_box.state = c.BUMPED
        coin_box.y_vel = -1
        coin_box.gravity = 1.2
        self.assertEqual(len(coin_box.group), 0)
        coin_box.rect.y = 110
        self.assertEqual(coin_box.rect.y, 110)
        self.assertGreater(coin_box.rect.y, coin_box.rest_height + 5)
        coin_box.bumped()
        self.assertEqual(len(coin_box.group), 1)
        self.assertNotEqual(coin_box.rect.y, 110)  # coin_box should have fallen
        self.assertEqual(coin_box.state, c.OPENED)

    def test_bumped_with_1up_mushroom(self):
        coin_box = Coin_box(100, 100, contents='1up_mushroom', group=self.group)
        coin_box.state = c.BUMPED
        coin_box.y_vel = -1
        coin_box.gravity = 1.2
        self.assertEqual(len(coin_box.group), 0)
        coin_box.rect.y = 110
        self.assertEqual(coin_box.rect.y, 110)
        self.assertGreater(coin_box.rect.y, coin_box.rest_height + 5)
        coin_box.bumped()
        self.assertEqual(len(coin_box.group), 1)
        self.assertNotEqual(coin_box.rect.y, 110)  # coin_box should have fallen
        self.assertEqual(coin_box.state, c.OPENED)

    def test_handle_states_resting(self):
        game_info = {c.CURRENT_TIME: 10}
        self.coin_box.state = c.RESTING
        self.coin_box.update(game_info)

    def test_handle_states_bumped(self):
        game_info = {c.CURRENT_TIME: 10}
        self.coin_box.state = c.BUMPED
        self.coin_box.update(game_info)

    def test_handle_states_opened(self):
        game_info = {c.CURRENT_TIME: 10}
        self.coin_box.state = c.OPENED
        self.coin_box.update(game_info)

    def test_resting_animation(self):
        game_info = {c.CURRENT_TIME: 10}
        self.coin_box.update(game_info)
        self.coin_box.animation_timer = self.coin_box.current_time - 500
        self.coin_box.resting()
        self.assertEqual(self.coin_box.frame_index, 1)

        self.coin_box.animation_timer = self.coin_box.current_time - 200
        self.coin_box.resting()
        self.assertEqual(self.coin_box.frame_index, 2)

        self.coin_box.animation_timer = self.coin_box.current_time - 200
        self.coin_box.resting()
        self.assertEqual(self.coin_box.frame_index, 1)

    def test_resting_animation_second_half(self):
        coin_box = Coin_box(100, 100, contents='coin', group=self.group)

        # Set the necessary properties
        coin_box.first_half = False
        coin_box.frame_index = 1
        coin_box.current_time = 1000
        coin_box.animation_timer = 0

        # Call the resting method and check the result
        coin_box.resting()
        self.assertEqual(coin_box.frame_index, 0)
        self.assertTrue(coin_box.first_half)
        self.assertEqual(coin_box.animation_timer, 1000)

    def test_start_bump_non_coin(self):
        non_coin_contents = ['mushroom', 'fireflower', '1up_mushroom']
        for content in non_coin_contents:
            with self.subTest(content=content):
                coin_box = Coin_box(100, 100, contents=content, group=self.group)
                with patch('SuperMarioLevel1.data.setup.SFX') as mock_sfx:
                    mock_sfx['coin'] = MagicMock()
                    mock_sfx['powerup_appears'] = MagicMock()
                    score_group = []
                    coin_box.start_bump(score_group)
                    self.assertEqual(coin_box.state, c.BUMPED)
                    self.assertEqual(coin_box.y_vel, -6)
                    mock_sfx['powerup_appears'].play.assert_called_once()
