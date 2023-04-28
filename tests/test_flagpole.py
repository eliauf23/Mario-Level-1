from unittest import TestCase
from unittest.mock import MagicMock, patch

import pygame as pg

import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.components.flagpole import Flag, Pole, Finial


# This is a test class for the Flag class in /data/components/flagpole.py.
# This class represents the Flag on top of the flag pole at the end of the level.
# There is at least one test for each Flag method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestFlag(TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.flag = Flag(0, 0)

    def test_initialization(self):
        assert self.flag.rect.right == 0
        assert self.flag.rect.y == 0
        assert self.flag.state == c.TOP_OF_POLE

    def test_setup_images(self):
        self.flag.frames = []
        self.flag.setup_images()
        assert len(self.flag.frames) == 1

    def test_get_image(self):
        image = self.flag.get_image(128, 32, 16, 16)
        assert isinstance(image, pg.Surface)

    def test_handle_state_top_of_pole(self):
        self.flag.state = c.TOP_OF_POLE
        self.flag.handle_state()
        assert self.flag.image == self.flag.frames[0]

    def test_handle_state_slide_down(self):
        self.flag.state = c.SLIDE_DOWN
        self.flag.sliding_down = MagicMock()
        self.flag.handle_state()
        self.flag.sliding_down.assert_called_once()

    def test_handle_state_bottom_of_pole(self):
        self.flag.state = c.BOTTOM_OF_POLE
        self.flag.handle_state()
        assert self.flag.image == self.flag.frames[0]

    def test_sliding_down(self):
        self.flag.state = c.SLIDE_DOWN
        initial_y = self.flag.rect.y
        self.flag.sliding_down()
        self.assertEqual(self.flag.rect.y, initial_y + 5)
        self.assertEqual(self.flag.y_vel, 5)

        self.flag.rect.y = 480
        self.flag.sliding_down()
        self.assertEqual(self.flag.state, c.BOTTOM_OF_POLE)

    def test_update(self):
        with patch.object(self.flag, 'handle_state') as mock_handle_state:
            self.flag.update()
            mock_handle_state.assert_called_once()


# This is a test class for the Pole class in /data/components/flagpole.py.
# This class represents the Pole that the flag is on top of.
# There is at least one test for each Pole method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestPole(TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.pole = Pole(0, 0)

    def test_initialization(self):
        assert self.pole.rect.x == 0
        assert self.pole.rect.y == 0

    def test_setup_frames(self):
        self.pole.frames = []
        self.pole.setup_frames()
        assert len(self.pole.frames) == 1

    def test_get_image(self):
        image = self.pole.get_image(263, 144, 2, 16)
        assert isinstance(image, pg.Surface)

    def test_update(self):
        initial_rect = self.pole.rect.copy()
        self.pole.update()
        self.assertEqual(self.pole.rect, initial_rect)


# This is a test class for the Finial class in /data/components/flagpole.py.
# This class represents the top of the flag pole.
# There is at least one test for each Finial method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestFinial(TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.finial = Finial(0, 0)

    def test_initialization(self):
        assert self.finial.rect.centerx == 0
        assert self.finial.rect.bottom == 0

    def test_setup_frames(self):
        self.finial.frames = []
        self.finial.setup_frames()
        assert len(self.finial.frames) == 1

    def test_get_image(self):
        image = self.finial.get_image(228, 120, 8, 8)
        assert isinstance(image, pg.Surface)

    def test_update(self):
        initial_rect = self.finial.rect.copy()
        self.finial.update()
        self.assertEqual(self.finial.rect, initial_rect)
