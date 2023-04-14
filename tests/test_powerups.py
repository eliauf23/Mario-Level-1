import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.components.powerups import Powerup, Mushroom, Star, FireFlower, LifeMushroom, FireBall
import SuperMarioLevel1.data.setup as setup


class TestPowerup(TestCase):
    def setUp(self):
        pg.init()
        self.powerup = Powerup(0, 0)

    def tearDown(self):
        pg.quit()

    def test_setup_powerup(self):
        pass

class TestMushroom(TestCase):
    def setUp(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.mushroom = Mushroom(0, 0)

    def tearDown(self):
        pg.quit()

    def test_setup_frames(self):
        self.assertEqual(len(self.mushroom.frames), 1)

    def test_handle_state(self):
        self.mushroom.state = c.REVEAL
        self.mushroom.handle_state()
        self.assertEqual(self.mushroom.y_vel, -1)

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


class TestLifeMushroom(TestCase):
    def setUp(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.life_mushroom = LifeMushroom(0, 0)

    def tearDown(self):
        pg.quit()

    def test_setup_frames(self):
        # TODO: check if this should start at 1
        self.assertEqual(len(self.life_mushroom.frames), 1)
        self.life_mushroom.setup_frames()
        self.assertEqual(len(self.life_mushroom.frames), 2)

    def test_handle_state(self):
        self.life_mushroom.handle_state()
        self.assertIsNotNone(self.life_mushroom.state)

    def test_revealing(self):
        self.life_mushroom.state = c.REVEAL
        self.life_mushroom.revealing()
        self.assertEqual(self.life_mushroom.y_vel, -1)
        self.assertEqual(self.life_mushroom.state, c.REVEAL)

    def test_sliding(self):
        self.life_mushroom.direction = c.LEFT
        self.life_mushroom.sliding()
        self.assertEqual(self.life_mushroom.x_vel, -3)
        self.life_mushroom.direction = c.RIGHT
        self.life_mushroom.sliding()
        self.assertEqual(self.life_mushroom.x_vel, 3)

    def test_falling(self):
        self.life_mushroom.y_vel = 7
        self.life_mushroom.falling()
        self.assertEqual(self.life_mushroom.y_vel, 8)
        self.life_mushroom.y_vel = 8
        self.life_mushroom.falling()
        self.assertEqual(self.life_mushroom.y_vel, 8)

class TestFireFlower(TestCase):
    def setUp(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.fire_flower = FireFlower(0, 0)
        self.fire_flower.update({c.CURRENT_TIME: 0})

    def tearDown(self):
        pg.quit()

    def test_setup_frames(self):
        self.assertEqual(len(self.fire_flower.frames), 4)

    def test_handle_state(self):
        self.fire_flower.update({c.CURRENT_TIME: 0})
        self.fire_flower.handle_state()
        self.assertIsNotNone(self.fire_flower.state)

    def test_revealing(self):
        self.fire_flower.state = c.REVEAL
        self.fire_flower.revealing()
        self.assertEqual(self.fire_flower.state, c.REVEAL)

    def test_falling(self):
        self.fire_flower.y_vel = 7
        self.fire_flower.falling()
        self.assertEqual(self.fire_flower.y_vel, 8)
        self.fire_flower.y_vel = 8
        self.fire_flower.falling()
        self.assertEqual(self.fire_flower.y_vel, 8)

class TestStar(TestCase):
    def setUp(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.star = Star(0, 0)

    def tearDown(self):
        pg.quit()

    def test_setup_frames(self):
        self.assertEqual(len(self.star.frames), 4)

    def test_handle_state(self):
        self.star.update({c.CURRENT_TIME: 0})
        self.star.handle_state()
        self.assertIsNotNone(self.star.state)

    def test_revealing(self):
        self.star.update({c.CURRENT_TIME: 0})
        self.star.state = c.REVEAL
        self.star.revealing()
        self.assertEqual(self.star.state, c.REVEAL)

    def test_falling(self):
        self.star.y_vel = 7
        self.star.falling()
        self.assertEqual(self.star.y_vel, 7.4)
        self.star.y_vel = 8
        self.star.falling()
        self.assertEqual(self.star.y_vel, 8)


    def test_sliding(self):
        self.star.direction = c.LEFT
        self.star.sliding()
        self.assertEqual(self.star.x_vel, -3)
        self.star.direction = c.RIGHT
        self.star.sliding()
        self.assertEqual(self.star.x_vel, 3)


class TestFireBall(TestCase):
    def setUp(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.fire_ball = FireBall(0, 0, True)
        self.fire_ball.update({c.CURRENT_TIME: 0}, viewport=pg.Rect(0, 0, 800, 600))

    def tearDown(self):
        pg.quit()

    def test_setup_frames(self):
        self.fire_ball.setup_frames()
        self.assertEqual(len(self.fire_ball.frames), 7)

    def test_handle_state(self):
        self.fire_ball.handle_state()
        self.assertIsNotNone(self.fire_ball.state)

    def test_explode_transition(self):
        self.fire_ball.explode_transition()
        self.assertEqual(self.fire_ball.state, c.EXPLODING)


