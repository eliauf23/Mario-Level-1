import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch
from SuperMarioLevel1.data.components.castle_flag import Flag
import SuperMarioLevel1.data.constants as c

# This is a test class for the Flag class in /data/components/castle_flag.py.
# This class represents Flag on the castle.
# There is at least one test for each Flag method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
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


    def test_rising(self):
        flag = Flag(200, 400)
        flag.rect.bottom = flag.target_height - 50
        flag.rising()
        self.assertTrue(flag.state, "resting")

    def test_flag_resting(self):
        with patch('SuperMarioLevel1.data.components.castle_flag.Flag.get_image', return_value=pg.Surface((28, 28))):
            flag = Flag(200, 400)
            flag.state = 'resting'
            flag.update()
            assert flag.rect.y == 400
            assert flag.state == 'resting'

    def test_get_image(self):
        with patch('SuperMarioLevel1.data.components.castle_flag.pg.Surface', return_value=pg.Surface((28, 28))):
            with patch('SuperMarioLevel1.data.components.castle_flag.pg.transform.scale',
                       return_value=pg.Surface((28, 28))):
                flag = Flag(200, 400)
                flag.sprite_sheet = pg.Surface((28, 28))
                flag.get_image(0, 0, 28, 28)
                assert flag.sprite_sheet.get_rect().width == 28
                assert flag.sprite_sheet.get_rect().height == 28
                assert flag.sprite_sheet.get_rect().x == 0
                assert flag.sprite_sheet.get_rect().y == 0
