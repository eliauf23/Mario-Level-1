from SuperMarioLevel1.data.components.bricks import Brick, BrickPiece
import SuperMarioLevel1.data.constants as c
from unittest import TestCase
from unittest.mock import patch
import pygame as pg

class TestBrick(TestCase):

    def test_brick_init(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='6coins')
            self.assertEqual(brick.rect.x, 50)
            self.assertEqual(brick.rect.y, 50)
            self.assertEqual(brick.contents, '6coins')
            self.assertEqual(brick.coin_total, 6)
            self.assertEqual(brick.state, c.RESTING)

    def test_brick_bump(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            powerup_group = pg.sprite.Group()
            brick = Brick(50, 50, contents='6coins', powerup_group=powerup_group)
            brick.start_bump(None)
            self.assertEqual(brick.state, c.BUMPED)
            self.assertEqual(brick.y_vel, -6)

    def test_brick_opened(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            powerup_group = pg.sprite.Group()
            brick = Brick(50, 50, contents='star', powerup_group=powerup_group)
            brick.state = c.OPENED
            brick.update()
            self.assertEqual(brick.powerup_in_box, False)
            self.assertEqual(brick.frame_index, 1)
            self.assertEqual(len(powerup_group), 1)

    def test_brick_resting(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='6coins')
            brick.state = c.RESTING
            brick.update()
            self.assertEqual(brick.frame_index, 0)

class TestBrickPiece(TestCase):
    def test_brick_piece_init(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick_piece = BrickPiece(100, 100, 2, -4)
            self.assertEqual(brick_piece.rect.x, 100)
            self.assertEqual(brick_piece.rect.y, 100)
            self.assertEqual(brick_piece.x_vel, 2)
            self.assertEqual(brick_piece.y_vel, -4)
            self.assertEqual(brick_piece.gravity, .8)

    def test_brick_piece_update_off_screen(self):
        # TODO: not sure if update brick piece is broken or I'm not setting up the test correctly
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick_piece = BrickPiece(100, 100, 2, -4)
            brick_piece.rect.y = 0
            brick_piece.update()
            self.assertEqual(brick_piece.y_vel, 0)
            self.assertEqual(brick_piece.gravity, 0)
            self.assertEqual(brick_piece.rect.y, 0)

    def test_brick_piece_update(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick_piece = BrickPiece(100, 100, 2, -4)
            self.assertEqual(brick_piece.rect.x, 100)
            self.assertEqual(brick_piece.rect.y, 100)
            self.assertEqual(brick_piece.x_vel, 2)
            self.assertEqual(brick_piece.y_vel, -4)
            brick_piece.update()
            self.assertEqual(brick_piece.rect.x, 102)
            self.assertEqual(brick_piece.rect.y, 96)
            self.assertEqual(brick_piece.x_vel, 2)
            # TODO: check if this is a bug or I'm not setting up the test correctly
            self.assertEqual(brick_piece.y_vel, brick_piece.y_vel + brick_piece.gravity)

    def test_check_if_off_screen(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick_piece = BrickPiece(100, 100, 2, c.SCREEN_HEIGHT)
            brick_piece.update()
            brick_piece.check_if_off_screen()
            self.assertFalse(brick_piece.alive())

    def test_brick_contents_star_start_bump(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='star')
            self.assertEqual(brick.contents, 'star')
            brick.start_bump(None)
            self.assertEqual(brick.state, c.BUMPED)
    #
    # def test_bumped(self):
    #     with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
    #         brick_star = Brick(50, 50, contents='star')
    #         brick_star.state = c.BUMPED
    #         brick_star.update()
    #         self.assertEqual(brick_star.state, c.OPENED)
    #         self.assertEqual(brick.state, c.OPENED)
    #

"""
TODO:
add more tests to cover different scenarios, such as:
 - the behavior of the Brick class when its contents are 'star' or when its state is c.c.RESTING. 
 You can also test the behavior of the BrickPiece class by checking if it gets removed from sprite groups when it goes off screen. 
"""
