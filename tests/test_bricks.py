from SuperMarioLevel1.data.components.bricks import Brick, BrickPiece
import SuperMarioLevel1.data.constants as c
from unittest import TestCase
from unittest.mock import patch
import pygame as pg

class TestBrick(TestCase):

    def test_brick_init(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='6coins')
            assert brick.rect.x == 50
            assert brick.rect.y == 50
            assert brick.contents == '6coins'
            assert brick.coin_total == 6
            assert brick.state == c.RESTING


    def test_brick_bump(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            powerup_group = pg.sprite.Group()
            brick = Brick(50, 50, contents='6coins', powerup_group=powerup_group)
            brick.start_bump(None)
            assert brick.state == c.BUMPED
            assert brick.y_vel == -6
    def test_brick_opened(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            powerup_group = pg.sprite.Group()
            brick = Brick(50, 50, contents='star', powerup_group=powerup_group)
            brick.state = c.OPENED
            brick.update()
            assert brick.powerup_in_box is False
            assert brick.frame_index == 1
            assert len(powerup_group) == 1
    def test_brick_resting(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='6coins')
            brick.state = c.RESTING
            brick.update()
            assert brick.frame_index == 0


class TestBrickPiece(TestCase):
    def test_brick_piece_init(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick_piece = BrickPiece(100, 100, 2, -4)
            assert brick_piece.rect.x == 100
            assert brick_piece.rect.y == 100
            assert brick_piece.x_vel == 2
            assert brick_piece.y_vel == -4
            assert brick_piece.gravity == .8

    def test_brick_piece_update_off_screen(self):
        # TODO: not sure if update brick piece is broken or I'm not setting up the test correctly
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick_piece = BrickPiece(100, 100, 2, -4)
            brick_piece.rect.y = 0
            brick_piece.update()
            assert brick_piece.y_vel == 0
            assert brick_piece.gravity == 0
            assert brick_piece.rect.y == 0

    def test_brick_piece_update(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick_piece = BrickPiece(100, 100, 2, -4)
            brick_piece.update()
            assert brick_piece.rect.x == 102
            assert brick_piece.rect.y == 96
            assert brick_piece.y_vel == -3.2



"""
TODO:
add more tests to cover different scenarios, such as:
 - the behavior of the Brick class when its contents are 'star' or when its state is c.c.RESTING. 
 You can also test the behavior of the BrickPiece class by checking if it gets removed from sprite groups when it goes off screen. 
"""
