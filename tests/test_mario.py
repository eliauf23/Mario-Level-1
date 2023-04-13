import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
from SuperMarioLevel1.data.components.mario import Mario
import SuperMarioLevel1.data.constants as c

class TestMario(TestCase):
    def setUp(self) -> None:
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.mario = Mario()

    def tearDown(self) -> None:
        pg.quit()

    def test_init(self):
        # assert that the mario object is an instance of the Mario class
        self.assertIsInstance(self.mario, Mario)
        # assert setup timers are all 0
        self.assertEqual(self.mario.walking_timer, 0)
        self.assertEqual(self.mario.invincible_animation_timer, 0)
        self.assertEqual(self.mario.invincible_start_timer, 0)
        self.assertEqual(self.mario.fire_transition_timer, 0)
        self.assertEqual(self.mario.death_timer, 0)
        self.assertEqual(self.mario.transition_timer, 0)
        self.assertEqual(self.mario.last_fireball_time, 0)
        self.assertEqual(self.mario.hurt_invisible_timer, 0)
        self.assertEqual(self.mario.hurt_invisible_timer2, 0)
        self.assertEqual(self.mario.flag_pole_timer, 0)

        # assert setup state booleans are correct - still TODO are the following

        # self.setup_forces()
        # self.setup_counters()
        # self.load_images_from_sheet()
        # self.image = self.right_frames[self.frame_index]
        # self.rect = self.image.get_rect()
        # self.mask = pg.mask.from_surface(self.image)

        assert(self.mario.key_timer == 0)
        assert(self.mario.state == c.WALK)

