from unittest import TestCase
import pygame as pg
from SuperMarioLevel1.data.components.checkpoint import Checkpoint

class TestCheckpoint(TestCase):
    def setUp(self):
        self.checkpoint = Checkpoint(100, 'test_checkpoint', y=50, width=20, height=400)

    def test_checkpoint_init(self):
        self.assertIsInstance(self.checkpoint.image, pg.Surface)
        self.assertEqual(self.checkpoint.rect.x, 100)
        self.assertEqual(self.checkpoint.rect.y, 50)
        self.assertEqual(self.checkpoint.rect.width, 20)
        self.assertEqual(self.checkpoint.rect.height, 400)
        self.assertEqual(self.checkpoint.name, 'test_checkpoint')

