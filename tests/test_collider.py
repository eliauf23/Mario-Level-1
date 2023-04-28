import unittest

import pygame as pg

import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.components.collider import Collider


# This is a test class for the Collider class in /data/components/collider.py.
# This class represents Invisible sprites placed overtop background parts
#     that can be collided with (pipes, steps, ground, etc.
# There is at least one test for each Collider method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestCollider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.collider = Collider(0, 0, 100, 100)

    def test_collider_attributes(self):
        self.assertEqual(self.collider.rect.x, 0)
        self.assertEqual(self.collider.rect.y, 0)
        self.assertEqual(self.collider.rect.width, 100)
        self.assertEqual(self.collider.rect.height, 100)
        self.assertEqual(self.collider.state, None)
        self.assertIsInstance(self.collider.image, pg.Surface)
        self.assertEqual(self.collider.image.get_size(), (100, 100))

    def test_collider_collide(self):
        collider1 = Collider(0, 0, 50, 50)
        collider2 = Collider(25, 25, 50, 50)
        self.assertTrue(pg.sprite.collide_rect(collider1, collider2))
