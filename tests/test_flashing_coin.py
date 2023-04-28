from unittest import TestCase
from unittest.mock import Mock

import pygame as pg

import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.components.flashing_coin import Coin


# This is a test class for the Coin class in /data/components/flashing_coin.py.
# This class represents the Flashing coin next to coin total info.
# There is at least one test for each Coin method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestFlashingCoin(TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        # pg.display.set_mode((640, 480), 0, 32)
        setup = Mock()
        setup.GFX = {'item_objects': pg.Surface((10, 10))}
        self.coin = Coin(0, 0)

    def test_create_frames(self):
        self.assertEqual(len(self.coin.frames), 3)

    def test_get_image(self):
        image = self.coin.get_image(1, 160, 5, 8)
        self.assertIsInstance(image, pg.Surface)
        self.assertEqual(image.get_size(), (13, 21))

    def test_update_first_half(self):
        self.clock = pg.time.Clock()
        self.current_time = 0
        self.coin_flashing = Coin(0, 0)

        self.coin_flashing.first_half = True
        self.coin_flashing.frame_index = 0
        # mock the timer
        self.coin_flashing.timer = pg.time.get_ticks()
        self.current_time = self.coin_flashing.timer + 400
        self.assertEqual(self.coin_flashing.frame_index, 0)
        self.coin_flashing.update(self.current_time)
        self.assertEqual(self.coin_flashing.frame_index, 1)
        self.current_time += 150
        self.coin_flashing.update(self.current_time)
        self.assertEqual(self.coin_flashing.frame_index, 2)
        self.current_time += 150
        self.coin_flashing.update(self.current_time)
        self.assertEqual(self.coin_flashing.frame_index, 1)
        self.assertFalse(self.coin_flashing.first_half)

    def test_update_second_half(self):
        self.clock = pg.time.Clock()
        self.current_time = 0
        self.coin_flashing = Coin(0, 0)

        self.coin_flashing.first_half = False
        self.coin_flashing.frame_index = 1
        self.coin_flashing.timer = 0

        self.current_time = 1000

        self.coin_flashing.update(self.current_time)
        self.assertEqual(self.coin_flashing.frame_index, 0)
        self.assertTrue(self.coin_flashing.first_half)
