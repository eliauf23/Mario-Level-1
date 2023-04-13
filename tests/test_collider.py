from unittest import TestCase
import pygame as pg
from SuperMarioLevel1.data.components.collider import Collider

class TestCollider(TestCase):
    def setUp(self):
        pg.init()
        pg.display.set_mode((1280, 720))  # screen width & height
        self.test_collider = Collider(50, 50, 100, 100)

    def tearDown(self) -> None:
        pg.quit()

    def test_collider_init(self):
        self.assertIsInstance(self.test_collider.image, pg.Surface)
        self.assertIsInstance(self.test_collider.rect, pg.Rect)
        self.assertEqual(self.test_collider.rect.x, 50)
        self.assertEqual(self.test_collider.rect.y, 50)
        self.assertEqual(self.test_collider.rect.width, 100)
        self.assertEqual(self.test_collider.rect.height, 100)