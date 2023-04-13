from unittest import TestCase
import pygame as pg
from SuperMarioLevel1.data.components.score import Score
import SuperMarioLevel1.data.constants as c

class TestScore(TestCase):

    def setUp(self):
        pg.init()
        self.screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.score = Score(100, 100, 100)

    def tearDown(self):
        pg.quit()

    def test_create_digit_list(self):
        self.score.create_digit_list()
        self.assertIsInstance(self.score.digit_list[0], pg.sprite.Sprite)

    def test_set_rects_for_images(self):
        self.score.create_digit_list()
        self.score.set_rects_for_images()
        self.assertEqual(self.score.digit_list[0].rect.x, 100)
        self.assertEqual(self.score.digit_list[0].rect.y, 100)

    def test_update(self):
        score_list = [self.score]
        level_info = {'level': 1, 'coin_total': 0, 'time': 400}
        self.score.update(score_list, level_info)
        self.assertEqual(self.score.digit_list[0].rect.y, 97)

    def test_check_to_delete_floating_scores(self):
        score_list = [self.score]
        level_info = {'level': 1, 'coin_total': 0, 'time': 400}
        self.score.update(score_list, level_info)
        self.score.check_to_delete_floating_scores(score_list, level_info)
        self.assertEqual(len(score_list), 1)

