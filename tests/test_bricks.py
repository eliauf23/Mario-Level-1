from SuperMarioLevel1.data.components.bricks import Brick, BrickPiece
import SuperMarioLevel1.data.constants as c
from unittest import TestCase
from unittest.mock import patch
import pygame as pg


# This is a test class for the Brick class in /data/components/bricks.py.
# This class represents Bricks that can be destroyed.
# There is at least one test for each Brick method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestBrick(TestCase):
    
    def test_brick_init(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='6coins')
            self.assertEqual(brick.rect.x, 50)
            self.assertEqual(brick.rect.y, 50)
            self.assertEqual(brick.contents, '6coins')
            self.assertEqual(brick.coin_total, 6)
            self.assertEqual(brick.state, c.RESTING)



    def test_bumped_star(self):
        brick = Brick(50, 50, contents='star')
        brick.rect.y = brick.rest_height + 10
        brick.bumped()
        self.assertEqual(brick.rect.y, brick.rest_height)
        self.assertEqual(brick.state, c.OPENED)

    def test_bumped_coins(self):
        brick = Brick(50, 50, contents='6coins')
        brick.rect.y = brick.rest_height + 10
        brick.coin_total = 0
        brick.bumped()
        self.assertEqual(brick.rect.y, brick.rest_height)
        self.assertEqual(brick.state, c.OPENED)
        brick.coin_total = 6
        brick.rect.y = brick.rest_height + 10
        brick.bumped()
        self.assertEqual(brick.state, c.RESTING)

    def test_bumped_other(self):
        brick = Brick(50, 50)
        brick.rect.y = brick.rest_height + 10
        brick.bumped()
        self.assertEqual(brick.rect.y, brick.rest_height)
        self.assertEqual(brick.state, c.RESTING)



    def test_get_image_1(self):
        """Test get_image method"""
        test_brick = Brick(0, 0, contents='6coins')
        test_image = test_brick.get_image(16, 0, 16, 16)

        self.assertIsInstance(test_image, pg.Surface)
        self.assertEqual(test_image.get_width(), 16 * c.SIZE_MULTIPLIER)
        self.assertEqual(test_image.get_height(), 16 * c.SIZE_MULTIPLIER)
        self.assertEqual(test_image.get_at((0, 0)), c.TRANSPARENT)

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

    def test_brick_contents_6coins_start_bump(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            powerup_group = pg.sprite.Group()
            brick = Brick(50, 50, contents='6coins', powerup_group=powerup_group)
            brick.coin_total = 0
            brick.start_bump(None)
            self.assertEqual(brick.state, c.BUMPED)
            self.assertEqual(brick.y_vel, -6)
            brick.coin_total = 1
            brick.start_bump(None)
            self.assertEqual(brick.state, c.BUMPED)
            self.assertEqual(brick.y_vel, -6)
            self.assertEqual(brick.coin_total, 0)
            self.assertEqual(brick.frame_index, 1)




    def test_brick_resting_coin_total_is_zero(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='6coins')
            brick.state = c.RESTING
            for i in range(6):
                self.start_bump([])
            brick.update()
            self.assertEqual(brick.coin_total, 0)
            self.assertEqual(brick.frame_index, 0)
            self.assertEqual(brick.state, c.OPENED)



    def test_brick_contents_star_start_bump(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='star')
            brick.start_bump(None)
            self.assertEqual(brick.frame_index, 1)
            self.assertEqual(brick.y_vel, -6)
            self.assertEqual(brick.state, c.BUMPED)


    def test_brick_bumped_coins(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='6coins')
            brick.state = c.BUMPED
            brick.update()
            self.assertEqual(brick.frame_index, 0)

    def test_brick_bumped_star(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='star')
            brick.state = c.BUMPED
            brick.update()
            self.assertEqual(brick.frame_index, 0)



    def test_get_image(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            with patch('SuperMarioLevel1.data.components.bricks.pg.transform.scale',
                       return_value=pg.Surface((16, 16))):
                brick = Brick(50, 50, contents='star')
                brick.sprite_sheet = pg.Surface((16, 16))
                brick.get_image(0, 0, 16, 16)
                assert brick.sprite_sheet.get_rect().width == 16
                assert brick.sprite_sheet.get_rect().height == 16
                assert brick.sprite_sheet.get_rect().x == 0
                assert brick.sprite_sheet.get_rect().y == 0

    def test_brick_resting_coin_total_is_zero_1(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='6coins')
            brick.state = c.RESTING
            brick.coin_total = 0
            brick.update()
            # state doesn't change to opened!
            self.assertEqual(brick.state, c.OPENED)

    def test_brick_bumped_star_1(self):
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
            brick = Brick(50, 50, contents='star')
            brick.state = c.BUMPED
            brick.update()
            # state doesn't change to opened!
            self.assertEqual(brick.state, c.OPENED)


# This is a test class for the BrickPiece class in /data/components/bricks.py.
# This class represents Pieces that appear when bricks are broken.
# There is at least one test for each BrickPiece method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
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
        with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((8, 8))):
            brick_piece = BrickPiece(100, 100, 2, -4)
            brick_piece.rect.y = c.SCREEN_HEIGHT + 1
            brick_piece.update()
            brick_piece.check_if_off_screen()
            self.assertFalse(brick_piece.alive())

    # def test_brick_piece_update_off_screen(self):
    #     # TODO: not sure if update brick piece is broken or I'm not setting up the test correctly
    #     with patch('SuperMarioLevel1.data.components.bricks.Brick.get_image', return_value=pg.Surface((16, 16))):
    #         brick_piece = BrickPiece(100, 100, 2, -4)
    #         brick_piece.rect.y = 0
    #         brick_piece.update()
    #         self.assertEqual(brick_piece.y_vel, 0)
    #         self.assertEqual(brick_piece.gravity, 0)
    #         self.assertEqual(brick_piece.rect.y, 0)

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
