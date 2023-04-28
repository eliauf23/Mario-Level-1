import unittest

import pygame as pg
from parameterized import parameterized

import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.components.checkpoint import Checkpoint


# This is a test class for the Checkpoint class in /data/components/checkpoint.py.
# This class represents an Invisible sprite used to add enemies, special boxes
#     and trigger sliding down the flag pole.
# There is at least one test for each Checkpoint method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestCheckpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def test_default_setup(self):
        checkpoint = Checkpoint(0, "default")
        self.assertEqual(checkpoint.rect.x, 0)
        self.assertEqual(checkpoint.name, "default")
        self.assertEqual(checkpoint.rect.y, 0)
        self.assertEqual(checkpoint.image.get_size(), (10, 600))

    def test_image_is_black_surface(self):
        checkpoint = Checkpoint(50, "surface")
        self.assertIsInstance(checkpoint.image, pg.Surface)
        self.assertEqual(checkpoint.image.get_size(), (10, 600))
        self.assertEqual(checkpoint.image.get_at((0, 0)), c.BLACK)

    @parameterized.expand([[0, 0], [300, 500]])
    def test_rect_position(self, x, y):
        checkpoint = Checkpoint(x, "position", y=y)
        self.assertEqual(checkpoint.rect.x, x)
        self.assertEqual(checkpoint.rect.y, y)

    # Should i assume invalid rect positions are handled because extends sprite?
