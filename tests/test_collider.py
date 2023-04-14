import unittest
import pygame as pg
from .. import constants as c
from data.components.collider import Collider

class TestCollider(unittest.TestCase):

    def setUp(self):
        pg.init()
        pg.display.set_mode(c.SCREEN_SIZE)
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

    def tearDown(self):
        pg.quit()

