from unittest import TestCase
import pygame as pg
from unittest.mock import MagicMock, patch
from SuperMarioLevel1.data.components.enemies import Enemy, Goomba, Koopa
import SuperMarioLevel1.data.constants as c

class TestEnemy(TestCase):

    def setUp(self):
        pg.init()
        pg.display.set_mode((1280, 720))  # screen width & height
        self.enemy = Enemy()

    def tearDown(self) -> None:
        pg.quit()

    def test_init(self):
        self.assertIsInstance(self.enemy, pg.sprite.Sprite)
    #
    # @patch('SuperMarioLevel1.data.components.enemies.Enemy.setup_frames')
    # def test_setup_enemy(self, mock_setup_frames):
    #     self.enemy.setup_enemy(10, 20, c.LEFT, 'test_enemy', mock_setup_frames)
    #     self.assertEqual(self.enemy.rect.x, 10)
    #     self.assertEqual(self.enemy.rect.bottom, 20)
    #     self.assertEqual(self.enemy.x_vel, -2)
    #     self.assertEqual(self.enemy.y_vel, 0)
    #     self.assertEqual(self.enemy.state, c.WALK)
    #     self.assertEqual(self.enemy.direction, c.LEFT)
    #     mock_setup_frames.assert_called_once()
    #
    # @patch('SuperMarioLevel1.data.components.enemies.Enemy.setup_frames')
    # def test_set_velocity(self,mock_setup_frames):
    #     self.enemy = Enemy()
    #     self.enemy.setup_enemy(10, 20, c.RIGHT, 'test_enemy', mock_setup_frames)
    #
    #     self.enemy.direction = MagicMock()  # Mock the direction attribute
    #     self.enemy.direction.return_value = c.LEFT  # Set the return value for the mock
    #
    #     self.enemy.set_velocity()
    #
    #
    #     self.assertEqual(self.enemy.x_vel, 2)
    #     self.assertEqual(self.enemy.y_vel, 0)
    #     # self.enemy.direction = MagicMock()  # Mock the direction attribute
    #     # self.enemy.direction.return_value = c.LEFT
    #     # self.enemy.set_velocity()
    #     # self.assertEqual(self.enemy.x_vel, -2)
    #     # self.assertEqual(self.enemy.y_vel, 0)



class TestGoomba(TestCase):

    def setUp(self):
        pg.init()
        pg.display.set_mode((1280, 720))  # screen width & height
        self.goomba = Goomba()

    def tearDown(self):
        pg.quit()
    def test_init(self):
        self.assertIsInstance(self.goomba, Enemy)
        self.assertEqual(self.goomba.name, 'goomba')

    def test_setup_frames(self):
        self.assertEqual(len(self.goomba.frames), 4)

    def test_jumped_on(self):
        self.goomba.death_timer = 0
        self.goomba.current_time = 501
        with patch.object(self.goomba, 'kill', side_effect=lambda: setattr(self.goomba, 'kill_called', True)):
            self.goomba.jumped_on()
            self.assertEqual(self.goomba.frame_index, 2)
            self.assertTrue(getattr(self.goomba, 'kill_called', False))


class TestKoopa(TestCase):

    def setUp(self):
        pg.init()
        pg.display.set_mode((1280, 720))  # screen width & height
        self.koopa = Koopa()

    def tearDown(self):
        pg.quit()

    def test_init(self):
        self.assertIsInstance(self.koopa, Enemy)
        self.assertEqual(self.koopa.name, 'koopa')

    def test_setup_frames(self):
        self.assertEqual(len(self.koopa.frames), 4)

    def test_jumped_on(self):
        initial_x = self.koopa.rect.x
        initial_bottom = self.koopa.rect.bottom
        self.koopa.jumped_on()
        self.assertEqual(self.koopa.x_vel, 0)
        self.assertEqual(self.koopa.frame_index, 2)
        self.assertEqual(self.koopa.rect.x, initial_x)
        self.assertEqual(self.koopa.rect.bottom, initial_bottom)

    def test_shell_sliding(self):
        self.koopa.direction = c.RIGHT
        self.koopa.shell_sliding()
        self.assertEqual(self.koopa.x_vel, 10)

        self.koopa.direction = c.LEFT
        self.koopa.shell_sliding()
        self.assertEqual(self.koopa.x_vel, -10)

