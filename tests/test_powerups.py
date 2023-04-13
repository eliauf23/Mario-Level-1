import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.components.powerups import Powerup, Mushroom
import SuperMarioLevel1.data.setup as setup


# class TestPowerup(TestCase):
    # def setUp(self):
    #     pg.init()
    #     self.screen = pg.display.set_mode((800, 600))
    #     self.clock = pg.time.Clock()
    #     # self.powerup = Powerup(0, 0)
    #
    # def tearDown(self):
    #     pg.quit()
    #
    # def test_setup_powerup(self):
    #     p = Powerup(100, 200)
    #     p.setup_powerup(100, 200, "test", lambda: None)
    #     self.assertIsNotNone(p.sprite_sheet)
    #     self.assertIsNotNone(p.frames)
    #     self.assertEqual(p.frame_index, 0)
    #     self.assertIsNotNone(p.image)
    #     self.assertIsNotNone(p.rect)
    #     self.assertEqual(p.rect.centerx, 100)
    #     self.assertEqual(p.rect.y, 200)
    #     self.assertEqual(p.state, c.REVEAL)
    #     self.assertEqual(p.y_vel, -1)
    #     self.assertEqual(p.x_vel, 0)
    #     self.assertEqual(p.direction, c.RIGHT)
    #     self.assertEqual(p.box_height, 200)
    #     self.assertEqual(p.gravity, 1)
    #     self.assertEqual(p.max_y_vel, 8)
    #     self.assertEqual(p.animate_timer, 0)
    #     self.assertEqual(p.name, "test")
    #
    # def test_get_image(self):
    #     p = Powerup(0, 0)
    #     image = p.get_image(0, 0, 16, 16)
    #     self.assertIsInstance(image, pg.Surface)
    #     self.assertEqual(image.get_width(), 16 * c.SIZE_MULTIPLIER)
    #     self.assertEqual(image.get_height(), 16 * c.SIZE_MULTIPLIER)
    #     self.assertEqual(image.get_at((0, 0)), c.BLACK)
    #
    # def test_revealing(self):
    #     p = Powerup(0, 0)
    #     p.box_height = 100
    #     p.revealing()
    #     self.assertEqual(p.rect.y, -1)
    #     p.box_height = 0
    #     p.revealing()
    #     self.assertEqual(p.rect.bottom, 0)
    #     self.assertEqual(p.y_vel, 0)
    #     self.assertEqual(p.state, c.SLIDE)
    #
    # def test_sliding(self):
    #     p = Powerup(0, 0)
    #     p.direction = c.RIGHT
    #     p.sliding()
    #     self.assertEqual(p.x_vel, 3)
    #     p.direction = c.LEFT
    #     p.sliding()
    #     self.assertEqual(p.x_vel, -3)
    #
    # def test_falling(self):
    #     p = Powerup(0, 0)
    #     p.y_vel = 0
    #     p.falling()
    #     self.assertEqual(p.y_vel, 1)
    #     self.assertEqual(p.max_y_vel, 8)


class TestMushroom(TestCase):
    def setUp(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.mushroom = Mushroom(0, 0)

    def tearDown(self):
        pg.quit()

    def test_setup_powerup(self):
        self.mushroom.setup_powerup(0, 0, 'mushroom', self.mushroom.setup_frames)
        self.assertEqual(self.mushroom.state, c.REVEAL)
        self.assertEqual(self.mushroom.direction, c.RIGHT)
        self.assertEqual(self.mushroom.name, 'mushroom')

    def test_get_image(self):
        sprite_sheet = setup.GFX['item_objects']
        image = self.mushroom.get_image(0, 0, 16, 16)
        self.assertEqual(image.get_rect().size, (16 * c.SIZE_MULTIPLIER, 16 * c.SIZE_MULTIPLIER))
        # TODO: bruh
        self.assertEqual(image.get_at((0, 0)), c.BLACK)
        self.assertEqual(sprite_sheet.get_at((0, 0)), image.get_at((1, 1)))

    def test_update(self):
        self.mushroom.update({c.CURRENT_TIME: 0})
        self.assertEqual(self.mushroom.state, c.REVEAL)
        self.mushroom.state = c.SLIDE
        self.mushroom.update({c.CURRENT_TIME: 0})
        self.assertEqual(self.mushroom.state, c.SLIDE)
        self.mushroom.state = c.FALL
        self.mushroom.update({c.CURRENT_TIME: 0})
        self.assertEqual(self.mushroom.state, c.FALL)

    def test_revealing(self):
        self.mushroom.setup_powerup(0, 0, 'mushroom', self.mushroom.setup_frames)
        self.mushroom.revealing()
        self.assertEqual(self.mushroom.state, c.REVEAL)
        self.assertEqual(self.mushroom.y_vel, -1)

    def test_sliding(self):
        self.mushroom.direction = c.LEFT
        self.mushroom.sliding()
        self.assertEqual(self.mushroom.x_vel, -3)
        self.mushroom.direction = c.RIGHT
        self.mushroom.sliding()
        self.assertEqual(self.mushroom.x_vel, 3)

    def test_falling(self):
        self.mushroom.y_vel = 7
        self.mushroom.falling()
        self.assertEqual(self.mushroom.y_vel, 8)
        self.mushroom.y_vel = 8
        self.mushroom.falling()
        self.assertEqual(self.mushroom.y_vel, 8)