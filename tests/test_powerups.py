import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.components.powerups import Powerup, Mushroom, Star, FireFlower, LifeMushroom, FireBall
import SuperMarioLevel1.data.setup as setup


class TestPowerup(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.powerup = Powerup(0, 0)

    def test_setup_powerup(self):
        pass

    def test_revealing(self):
        powerup = Mushroom(0, 10)
        powerup.rect.bottom = 0
        powerup.revealing()
        self.assertEqual(powerup.rect.bottom, powerup.box_height)
        self.assertEqual(powerup.y_vel, 0)
        self.assertEqual(powerup.state, c.SLIDE)

    def test_handle_state(self):
        self.powerup.state = c.FLYING
        self.powerup.handle_state()
        self.assertTrue(True)


class TestMushroom(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.clock = pg.time.Clock()
        self.mushroom = Mushroom(0, 0)

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
        # TODO: ADD MORE IMAGE TESTING HERE

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
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.clock = pg.time.Clock()
        self.life_mushroom = LifeMushroom(0, 0)

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
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.clock = pg.time.Clock()
        self.fire_flower = FireFlower(0, 0)
        self.fire_flower.update({c.CURRENT_TIME: 0})

    def test_setup_frames(self):
        self.assertEqual(len(self.fire_flower.frames), 4)

    def test_handle_state(self):
        self.fire_flower.update({c.CURRENT_TIME: 0})
        self.fire_flower.handle_state()
        self.assertIsNotNone(self.fire_flower.state)

    def test_handle_state_revealing(self):
        self.fire_flower.state = c.REVEAL
        self.fire_flower.revealing = Mock()
        self.fire_flower.handle_state()
        self.fire_flower.revealing.assert_called_once()

    def test_handle_state_resting(self):
        self.fire_flower.state = c.RESTING
        self.fire_flower.resting = Mock()
        self.fire_flower.handle_state()
        self.fire_flower.resting.assert_called_once()

    def test_revealing(self):
        self.fire_flower.state = c.REVEAL
        self.fire_flower.animation = Mock()
        self.fire_flower.rect.bottom = self.fire_flower.box_height - 1
        self.fire_flower.revealing()
        self.assertEqual(self.fire_flower.rect.bottom, self.fire_flower.box_height)
        self.assertEqual(self.fire_flower.state, c.RESTING)
        self.fire_flower.animation.assert_called_once()

    def test_resting(self):
        self.fire_flower.animation = Mock()
        self.fire_flower.resting()
        self.fire_flower.animation.assert_called_once()

    def test_falling(self):
        self.fire_flower.y_vel = 7
        self.fire_flower.falling()
        self.assertEqual(self.fire_flower.y_vel, 8)
        self.fire_flower.y_vel = 8
        self.fire_flower.falling()
        self.assertEqual(self.fire_flower.y_vel, 8)

    def test_animation(self):
        self.fire_flower.current_time = 1000
        self.fire_flower.animate_timer = 0
        self.fire_flower.frame_index = 0
        self.fire_flower.animation()
        self.assertEqual(self.fire_flower.frame_index, 1)
        self.fire_flower.frame_index = 4
        self.fire_flower.current_time = 1000
        self.fire_flower.animate_timer = 0
        self.fire_flower.animation()
        self.assertEqual(self.fire_flower.frame_index, 0)
        self.assertEqual(self.fire_flower.animate_timer, self.fire_flower.current_time)
        self.assertEqual(self.fire_flower.image, self.fire_flower.frames[self.fire_flower.frame_index])


class TestStar(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.clock = pg.time.Clock()
        self.star = Star(0, 0)

    def test_setup_frames(self):
        self.assertEqual(len(self.star.frames), 4)

    def test_handle_state_reveal(self):
        self.star.update({c.CURRENT_TIME: 0})
        self.state = c.REVEAL
        self.star.revealing = Mock()
        self.star.handle_state()
        self.star.revealing.assert_called_once()

    def test_handle_state_bounce(self):
        self.star.update({c.CURRENT_TIME: 0})
        self.star.state = c.BOUNCE
        self.star.bouncing = Mock()
        self.star.handle_state()
        self.star.bouncing.assert_called_once()

    def test_revealing(self):
        self.star.update({c.CURRENT_TIME: 0})
        self.star.state = c.REVEAL
        self.star.rect.bottom = 0
        self.star.animation = Mock()
        self.star.revealing()
        self.assertEqual(self.star.state, c.BOUNCE)
        self.assertEqual(self.star.y_vel, -2)
        self.star.animation.assert_called_once()

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

    def test_bouncing(self):
        self.star.animation = Mock()
        self.star.direction = c.LEFT
        self.star.bouncing()
        self.star.animation.assert_called_once()
        self.assertEqual(self.star.x_vel, -5)
        self.star.direction = c.RIGHT
        self.star.bouncing()
        self.assertEqual(self.star.x_vel, 5)

    def test_animation(self):
        self.star.animation_timer = 0
        self.star.current_time = 1000
        self.star.frame_index = 0
        self.star.animation()
        self.assertEqual(self.star.frame_index, 1)
        self.assertEqual(self.star.animate_timer, self.star.current_time)
        self.assertEqual(self.star.image, self.star.frames[self.star.frame_index])
        self.star.animation_timer = 0
        self.star.current_time = 1200
        self.star.frame_index = 3
        self.star.animation()
        self.assertEqual(self.star.frame_index, 0)


class TestFireBall(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.clock = pg.time.Clock()
        self.fire_ball = FireBall(0, 0, True)
        self.fire_ball.update({c.CURRENT_TIME: 0}, viewport=pg.Rect(0, 0, 800, 600))

    def test_init_facing_right(self):
        self.assertIsInstance(self.fire_ball, pg.sprite.Sprite)
        self.assertEqual(self.fire_ball.direction, c.RIGHT)
        self.assertEqual(self.fire_ball.x_vel, 12)
        self.assertEqual(self.fire_ball.y_vel, 10)
        self.assertEqual(self.fire_ball.gravity, .9)
        self.assertEqual(self.fire_ball.frame_index, 0)
        self.assertEqual(self.fire_ball.animation_timer, 0)
        self.assertEqual(self.fire_ball.state, c.FLYING)
        self.assertEqual(self.fire_ball.name, c.FIREBALL)

    def test_init_facing_left(self):
        self.fireball2 = FireBall(0, 0, False)
        self.assertIsInstance(self.fireball2, pg.sprite.Sprite)
        self.assertEqual(self.fireball2.direction, c.LEFT)
        self.assertEqual(self.fireball2.x_vel, -12)
        self.assertEqual(self.fireball2.y_vel, 10)
        self.assertEqual(self.fireball2.gravity, .9)
        self.assertEqual(self.fireball2.frame_index, 0)
        self.assertEqual(self.fireball2.animation_timer, 0)
        self.assertEqual(self.fireball2.state, c.FLYING)
        self.assertEqual(self.fireball2.name, c.FIREBALL)

    def test_setup_frames(self):
        self.fire_ball.setup_frames()
        self.assertEqual(len(self.fire_ball.frames), 7)
        self.assertIsInstance(self.fire_ball.frames[0], pg.Surface)

    def test_get_image(self):
        image = self.fire_ball.get_image(0, 0, 16, 16)
        self.assertIsInstance(image, pg.Surface)
        self.assertEqual(image.get_rect().size, (16 * c.SIZE_MULTIPLIER, 16 * c.SIZE_MULTIPLIER))

    def test_update(self):
        game_info = {c.CURRENT_TIME: 0}
        viewport = pg.Rect(0, 0, 800, 600)
        self.fire_ball.handle_state = Mock()
        self.fire_ball.check_if_off_screen = Mock()
        self.fire_ball.update(game_info, viewport)
        self.assertEqual(self.fire_ball.current_time, 0)
        self.fire_ball.handle_state.assert_called_once()
        self.fire_ball.check_if_off_screen.assert_called_once_with(viewport)

    def test_handle_state(self):
        self.fire_ball.animation = Mock()
        self.fire_ball.state = c.FLYING
        self.fire_ball.handle_state()
        self.fire_ball.animation.assert_called()
        self.fire_ball.state = c.BOUNCING
        self.fire_ball.handle_state()
        self.fire_ball.animation.assert_called()
        self.fire_ball.state = c.EXPLODING
        self.fire_ball.handle_state()
        self.fire_ball.animation.assert_called()

    def test_animation_flying(self):
        self.fire_ball.state = c.FLYING
        self.fire_ball.animation_timer = 0
        self.fire_ball.current_time = 1000
        self.fire_ball.frame_index = 0
        self.fire_ball.animation()
        self.assertEqual(self.fire_ball.frame_index, 1)

        self.fire_ball.animation_timer = 0
        self.fire_ball.current_time = 1200
        self.fire_ball.frame_index = 3
        self.fire_ball.animation()
        self.assertEqual(self.fire_ball.frame_index, 0)

    def test_animation_bouncing(self):
        self.fire_ball.state = c.BOUNCING
        self.fire_ball.animation_timer = 0
        self.fire_ball.current_time = 1000
        self.fire_ball.frame_index = 0
        self.fire_ball.animation()
        self.assertEqual(self.fire_ball.frame_index, 1)

        self.fire_ball.animation_timer = 0
        self.fire_ball.current_time = 1200
        self.fire_ball.frame_index = 3
        self.fire_ball.animation()
        self.assertEqual(self.fire_ball.frame_index, 0)

    def test_animation_exploding(self):
        self.fire_ball.state = c.EXPLODING
        self.fire_ball.animation_timer = 0
        self.fire_ball.current_time = 1000
        self.fire_ball.frame_index = 1
        self.fire_ball.animation()
        self.assertEqual(self.fire_ball.frame_index, 2)

        self.fire_ball.animation_timer = 0
        self.fire_ball.current_time = 1200
        self.fire_ball.frame_index = 6
        self.fire_ball.animation()
        self.assertFalse(self.fire_ball.alive())

    def test_explode_transition(self):
        self.fire_ball.explode_transition()
        self.assertEqual(self.fire_ball.frame_index, 4)
        self.assertEqual(self.fire_ball.image, self.fire_ball.frames[4])
        self.assertEqual(self.fire_ball.state, c.EXPLODING)

    def test_check_if_off_screen(self):
        # test left of viewport
        viewport = pg.Rect(0, 0, 800, 600)
        self.fire_ball.rect.right = -1
        self.fire_ball.check_if_off_screen(viewport)
        self.assertFalse(self.fire_ball.alive())
        # test right of viewport
        viewport = pg.Rect(0, 0, 800, 600)
        self.fire_ball.rect.right = 900
        self.fire_ball.check_if_off_screen(viewport)
        self.assertFalse(self.fire_ball.alive())
        # test right of viewport
        viewport = pg.Rect(0, 0, 800, 600)
        self.fire_ball.rect.right = 900
        self.fire_ball.check_if_off_screen(viewport)
        self.assertFalse(self.fire_ball.alive())
