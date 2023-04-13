import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch
from SuperMarioLevel1.data.components.flagpole import Flag, Pole, Finial
import SuperMarioLevel1.data.constants as c

class TestFlag(TestCase):
    def setUp(self):
        pg.init()
        self.flag = Flag(0, 0)

    def tearDown(self):
        pg.quit()

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

class TestPole(TestCase):
    def setUp(self):
        pg.init()
        self.pole = Pole(0, 0)

    def tearDown(self):
        pg.quit()

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

class TestFinial(TestCase):
    def setUp(self):
        pg.init()
        self.finial = Finial(0, 0)

    def tearDown(self):
        pg.quit()

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
