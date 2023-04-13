import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch
from SuperMarioLevel1.data.components.castle_flag import Flag
import SuperMarioLevel1.data.constants as c
class TestCastleFlag(TestCase):

    def test_flag_init(self):
        with patch('SuperMarioLevel1.data.components.castle_flag.Flag.get_image', return_value=pg.Surface((28, 28))):
            flag = Flag(200, 400)
            assert flag.rect.x == 200
            assert flag.rect.y == 400
            assert flag.state == 'rising'
            assert flag.y_vel == -2
            assert flag.target_height == 400

    def test_flag_rising(self):
        with patch('SuperMarioLevel1.data.components.castle_flag.Flag.get_image', return_value=pg.Surface((28, 28))):
            flag = Flag(200, 400)
            flag.target_height = 398
            flag.update()
            assert flag.rect.y == 398
            assert flag.state == 'rising'

    def test_flag_resting(self):
        with patch('SuperMarioLevel1.data.components.castle_flag.Flag.get_image', return_value=pg.Surface((28, 28))):
            flag = Flag(200, 400)
            flag.state = 'resting'
            flag.update()
            assert flag.rect.y == 400
            assert flag.state == 'resting'
