from unittest import TestCase
import pygame as pg
from SuperMarioLevel1.data.components.score import Score
import SuperMarioLevel1.data.constants as c
from unittest.mock import MagicMock


# This is a test class for the Score class in /data/components/score.py.
# This class represents the Scores that appear, float up, and disappear.
# There is at least one test for each Score method, asserting that the correct values were modified and the correct
# methods were called. In order to achieve full coverage, some methods require multiple tests to achieve that their
# behavior is correct across all possible cases.
class TestScore(TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        self.score = Score(100, 100, 100)

    def test_score_init(self):
        score1 = Score(100, 100, 100, flag_pole=True)
        self.assertEqual(score1.y_vel, -4)

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

    def test_update_flag_pole_score(self):
        score1 = Score(100, 100, 100, flag_pole=True)
        score_list = [score1]
        level_info = {'level': 1, 'coin_total': 0, 'time': 400}
        score1.update(score_list, level_info)
        self.assertEqual(score1.digit_list[0].rect.y, 96)

    def test_draw(self):
        self.score.create_digit_list()
        self.score.set_rects_for_images()
        screen_mock = MagicMock()
        self.score.draw(screen_mock)
        screen_mock.blit.assert_called()

    def test_check_to_delete_floating_scores(self):
        score_list = [self.score]
        level_info = {'level': 1, 'coin_total': 0, 'time': 400}
        self.score.update(score_list, level_info)
        self.score.check_to_delete_floating_scores(score_list, level_info)
        self.assertEqual(len(score_list), 1)

    def test_check_to_delete_floating_scores_1000(self):
        score1 = Score(100, 100, 200)
        score2 = Score(200, 200, 500)
        score_list = [score1, score2]
        level_info = {'level': 1, 'coin_total': 0, 'time': 400}
        score2.score_string = '100'
        score2.y = score2.digit_list[0].rect.y + 76
        self.assertEqual(len(score_list), 2)
        score2.update(score_list, level_info)
        self.assertEqual(len(score_list), 1)
        self.assertIn(score1, score_list)
        self.assertNotIn(score2, score_list)

    def test_check_to_delete_floating_scores_not1000(self):
        score1 = Score(100, 100, 200)
        score2 = Score(200, 200, 500)
        score_list = [score1, score2]
        level_info = {'level': 1, 'coin_total': 0, 'time': 400}
        score1.score_string = '1000'
        score1.y = score1.digit_list[0].rect.y + 131
        score2.score_string = '100'
        score2.y = score2.digit_list[0].rect.y + 76
        self.assertEqual(len(score_list), 2)
        score1.update(score_list, level_info)
        self.assertEqual(len(score_list), 1)
        self.assertNotIn(score1, score_list)
        self.assertIn(score2, score_list)
