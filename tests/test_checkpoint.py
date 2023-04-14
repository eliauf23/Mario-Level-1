import unittest
import pygame as pg
from .. import constants as c
from data.components.checkpoint import Checkpoint
from parameterized import parameterized


class TestCheckpoint(unittest.TestCase):
    def test_default_setup(self):
        pg.init()
        checkpoint = Checkpoint(0, "default")
        self.assertEqual(checkpoint.rect.x,  0)
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
        checkpoint = Checkpoint(x, "position", y = y)
        self.assertEqual(checkpoint.rect.x, x)
        self.assertEqual(checkpoint.rect.y, y)

    # Should i assume invalid rect positions are handled because extends sprite?
    def tearDown(self):
        pg.quit()

    