import pygame as pg
from unittest.mock import MagicMock, patch, Mock, ANY
from SuperMarioLevel1.data.components.info import OverheadInfo
import SuperMarioLevel1.data.constants as c
from unittest import TestCase


class TestOverheadInfo(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):

        self.game_info = {c.COIN_TOTAL: 0, c.LIVES: 3, c.TOP_SCORE: 0}
        self.overhead_info = OverheadInfo(self.game_info, state=c.MAIN_MENU)

    def test_init(self):
        self.assertEqual(self.overhead_info.state, c.MAIN_MENU)
        self.assertEqual(self.overhead_info.game_info, self.game_info)
        self.assertEqual(self.overhead_info.coin_total, 0)
        self.assertEqual(self.overhead_info.top_score, 0)
        self.assertEqual(self.overhead_info.total_lives, self.game_info[c.LIVES])
        self.assertEqual(self.overhead_info.time, 401)
        self.assertEqual(self.overhead_info.state, c.MAIN_MENU)

    def test_update(self):
        level_info = {
            c.SCORE: 0,
            c.COIN_TOTAL: 0,
            c.LIVES: 3,
            c.TOP_SCORE: 0,
            c.CURRENT_TIME: 0,
            c.LEVEL_STATE: None,
        }

        # Test with MAIN_MENU state
        self.overhead_info.state = c.MAIN_MENU
        with patch.object(self.overhead_info, 'handle_level_state') as mock_handle_level_state:
            self.overhead_info.update(level_info)
            mock_handle_level_state.assert_called_once_with(level_info)

        # Test with LEVEL state
        self.overhead_info.state = c.LEVEL
        with patch.object(self.overhead_info, 'handle_level_state') as mock_handle_level_state:
            self.overhead_info.update(level_info, mario=Mock())
            mock_handle_level_state.assert_called_once_with(level_info)

    def test_handle_level_state_main_menu(self):
        level_info = {
            c.SCORE: 0,
            c.COIN_TOTAL: 0,
            c.LIVES: 3,
            c.TOP_SCORE: 0,
            c.CURRENT_TIME: 0,
            c.LEVEL_STATE: None,
        }

        self.overhead_info.state = c.MAIN_MENU
        with patch.object(self.overhead_info, 'update_score_images') as mock_update_score_images, \
                patch.object(self.overhead_info, 'update_coin_total') as mock_update_coin_total, \
                patch.object(self.overhead_info.flashing_coin, 'update') as mock_flashing_coin_update:
            self.overhead_info.handle_level_state(level_info)
            mock_update_score_images.assert_called()
            mock_update_coin_total.assert_called()
            mock_flashing_coin_update.assert_called()

    def test_update_score_images(self):
        score = 1234
        with patch('SuperMarioLevel1.data.components.info.Character') as mock_character:
            self.overhead_info.update_score_images(self.overhead_info.score_images, score)
            mock_character.assert_any_call(self.overhead_info.image_dict['1'])
            mock_character.assert_any_call(self.overhead_info.image_dict['2'])
            mock_character.assert_any_call(self.overhead_info.image_dict['3'])
            mock_character.assert_any_call(self.overhead_info.image_dict['4'])

    def test_update_coin_total(self):
        level_info = {c.COIN_TOTAL: 42}
        with patch.object(self.overhead_info, 'create_label') as mock_create_label:
            self.overhead_info.update_coin_total(level_info)
            self.assertEqual(self.overhead_info.coin_total, 42)
            mock_create_label.assert_called_once_with(self.overhead_info.coin_count_images, '*42', ANY, ANY)

    def test_update_coin_total_small_string(self):
        level_info = {c.COIN_TOTAL: 2}
        with patch.object(self.overhead_info, 'create_label') as mock_create_label:
            self.overhead_info.update_coin_total(level_info)
            self.assertEqual(self.overhead_info.coin_total, 2)
            mock_create_label.assert_called_once_with(self.overhead_info.coin_count_images, '*02', ANY, ANY)

    def test_update_coin_total_large_string(self):
        level_info = {c.COIN_TOTAL: 100}
        with patch.object(self.overhead_info, 'create_label') as mock_create_label:
            self.overhead_info.update_coin_total(level_info)
            self.assertEqual(self.overhead_info.coin_total, 100)
            mock_create_label.assert_called_once_with(self.overhead_info.coin_count_images, '*00', ANY, ANY)

    # TODO: Add similar tests for other states in the handle_level_state method
    # TODO: Add tests for update_count_down_clock method
    # TODO: Add tests for the draw method
    # TODO: Add tests for other draw methods in the same manner, adjusting the state and expected call count accordingly

    def test_handle_level_state_load_screen(self):
        self.overhead_info.state = c.LOAD_SCREEN
        level_info = {c.SCORE: 100, c.COIN_TOTAL: 42}
        with patch.object(self.overhead_info, 'update_score_images') as mock_update_score_images:
            with patch.object(self.overhead_info, 'update_coin_total') as mock_update_coin_total:
                self.overhead_info.handle_level_state(level_info)
                mock_update_score_images.assert_called_once_with(self.overhead_info.score_images, 100)
                mock_update_coin_total.assert_called_once_with(level_info)

    def test_handle_level_state_level_not_dead_mario(self):
        level_info = {c.SCORE: 100, c.COIN_TOTAL: 42, c.LEVEL_STATE: c.NOT_FROZEN, c.CURRENT_TIME: 10}
        self.overhead_info.update(level_info, mario=Mock(dead=False))
        self.overhead_info.state = c.LEVEL
        with patch.object(self.overhead_info, 'update_score_images') as mock_update_score_images:
            with patch.object(self.overhead_info, 'update_coin_total') as mock_update_coin_total:
                with patch.object(self.overhead_info, 'update_count_down_clock') as mock_update_count_down_clock:
                    self.overhead_info.handle_level_state(level_info)
                    mock_update_score_images.assert_called_once_with(self.overhead_info.score_images, 100)
                    mock_update_coin_total.assert_called_once_with(level_info)
                # mock_update_count_down_clock.assert_called_once_with(level_info)

    def test_handle_level_state_level_dead_mario(self):
        level_info = {c.SCORE: 100, c.COIN_TOTAL: 42, c.LEVEL_STATE: c.NOT_FROZEN, c.CURRENT_TIME: 10}
        self.overhead_info.update(level_info, mario=Mock())
        self.overhead_info.state = c.LEVEL
        with patch.object(self.overhead_info, 'update_score_images') as mock_update_score_images:
            with patch.object(self.overhead_info, 'update_coin_total') as mock_update_coin_total:
                with patch.object(self.overhead_info, 'update_count_down_clock') as mock_update_count_down_clock:
                    self.overhead_info.handle_level_state(level_info)
                    mock_update_score_images.assert_called_once_with(self.overhead_info.score_images, 100)
                    mock_update_coin_total.assert_called_once_with(level_info)
                    # mock_update_count_down_clock.assert_called_once_with(level_info)

    def test_handle_level_state_time_out(self):
        self.overhead_info.state = c.TIME_OUT
        level_info = {c.SCORE: 100, c.COIN_TOTAL: 42}
        with patch.object(self.overhead_info, 'update_score_images') as mock_update_score_images:
            with patch.object(self.overhead_info, 'update_coin_total') as mock_update_coin_total:
                self.overhead_info.handle_level_state(level_info)
                mock_update_score_images.assert_called_once_with(self.overhead_info.score_images, 100)
                mock_update_coin_total.assert_called_once_with(level_info)

    def test_handle_level_state_game_over(self):
        self.overhead_info.state = c.GAME_OVER
        level_info = {c.SCORE: 100, c.COIN_TOTAL: 42}
        with patch.object(self.overhead_info, 'update_score_images') as mock_update_score_images:
            with patch.object(self.overhead_info, 'update_coin_total') as mock_update_coin_total:
                self.overhead_info.handle_level_state(level_info)
                mock_update_score_images.assert_called_once_with(self.overhead_info.score_images, 100)
                mock_update_coin_total.assert_called_once_with(level_info)

    def test_handle_level_state_fast_count_down(self):
        self.overhead_info.state = c.FAST_COUNT_DOWN
        self.overhead_info.time = 0
        level_info = {c.SCORE: 100, c.COIN_TOTAL: 42, c.CURRENT_TIME: 0}
        with patch.object(self.overhead_info, 'update_score_images') as mock_update_score_images:
            with patch.object(self.overhead_info, 'update_coin_total') as mock_update_coin_total:
                with patch.object(self.overhead_info, 'update_count_down_clock') as mock_update_count_down_clock:
                    self.overhead_info.handle_level_state(level_info)
                    mock_update_score_images.assert_called_once_with(self.overhead_info.score_images,
                                                                     self.overhead_info.score)
                    mock_update_coin_total.assert_called_once_with(level_info)
                    mock_update_count_down_clock.assert_called_once_with(level_info)

    def test_handle_level_state_end_of_level(self):
        self.overhead_info.state = c.END_OF_LEVEL
        self.overhead_info.flashing_coin = Mock()
        level_info = {c.SCORE: 100, c.COIN_TOTAL: 42, c.CURRENT_TIME: 0}
        with patch.object(self.overhead_info, 'update_score_images') as mock_update_score_images:
            with patch.object(self.overhead_info, 'update_coin_total') as mock_update_coin_total:
                with patch.object(self.overhead_info.flashing_coin, 'update') as mock_flashing_coin_update:
                    self.overhead_info.handle_level_state(level_info)
                    mock_flashing_coin_update.assert_called_once_with(0)

    # Add tests for other states in the same manner, adjusting the mock calls accordingly

    def test_update_count_down_clock_regular(self):
        level_info = {c.CURRENT_TIME: 0}
        self.overhead_info.current_time = -400
        self.overhead_info.time = 10
        self.overhead_info.update_count_down_clock(level_info)
        self.assertEqual(self.overhead_info.time, 10)

    def test_update_count_down_clock_fast_count_down(self):
        level_info = {c.CURRENT_TIME: 0}
        self.overhead_info.state = c.FAST_COUNT_DOWN
        self.overhead_info.time = 10
        self.overhead_info.update_count_down_clock(level_info)
        self.assertEqual(self.overhead_info.time, 9)

    def test_update_count_down_clock_big_time_diff(self):
        level_info = {c.CURRENT_TIME: 500}
        self.overhead_info.state = c.MAIN_MENU
        self.overhead_info.time = 10
        self.overhead_info.current_time = 0
        self.overhead_info.update_count_down_clock(level_info)
        self.assertEqual(self.overhead_info.time, 9)

    def test_draw_main_menu(self):
        self.overhead_info.state = c.MAIN_MENU
        surface = Mock()
        with patch.object(self.overhead_info, 'draw_main_menu_info') as mock_draw_main_menu_info:
            self.overhead_info.draw(surface)
            mock_draw_main_menu_info.assert_called_once_with(surface)

    def test_draw_load_screen(self):
        self.overhead_info.state = c.LOAD_SCREEN
        surface = Mock()
        with patch.object(self.overhead_info, 'draw_loading_screen_info') as mock_draw_loading_screen_info:
            self.overhead_info.draw(surface)
            mock_draw_loading_screen_info.assert_called_once_with(surface)

    def test_draw_level(self):
        self.overhead_info.state = c.LEVEL
        surface = Mock()
        with patch.object(self.overhead_info, 'draw_level_screen_info') as mock_draw_level_screen_info:
            self.overhead_info.draw(surface)
            mock_draw_level_screen_info.assert_called_once_with(surface)

    def test_draw_game_over(self):
        self.overhead_info.state = c.GAME_OVER
        surface = Mock()
        with patch.object(self.overhead_info, 'draw_game_over_screen_info') as mock_draw_game_over_screen_info:
            self.overhead_info.draw(surface)
            mock_draw_game_over_screen_info.assert_called_once_with(surface)

    def test_draw_fast_count_down(self):
        self.overhead_info.state = c.FAST_COUNT_DOWN
        surface = Mock()
        with patch.object(self.overhead_info, 'draw_level_screen_info') as mock_draw_level_screen_info:
            self.overhead_info.draw(surface)
            mock_draw_level_screen_info.assert_called_once_with(surface)

    def test_draw_end_of_level(self):
        self.overhead_info.state = c.END_OF_LEVEL
        surface = Mock()
        with patch.object(self.overhead_info, 'draw_level_screen_info') as mock_draw_level_screen_info:
            self.overhead_info.draw(surface)
            mock_draw_level_screen_info.assert_called_once_with(surface)

    def test_draw_time_out(self):
        self.overhead_info.state = c.TIME_OUT
        surface = Mock()
        with patch.object(self.overhead_info, 'draw_time_out_screen_info') as mock_draw_time_out_screen_info:
            self.overhead_info.draw(surface)
            mock_draw_time_out_screen_info.assert_called_once_with(surface)

    def test_draw_main_menu_info(self):
        surface = Mock()
        score_images_len = len(self.overhead_info.score_images)
        letter_len_main_menu = 0
        for label in self.overhead_info.main_menu_labels:
            for letter in label:
                letter_len_main_menu += 1
        coin_count_images_len = len(self.overhead_info.coin_count_images)
        letter_len_label_list = 0
        for label in self.overhead_info.label_list:
            for letter in label:
                letter_len_label_list += 1
        total_expected_blit = score_images_len + letter_len_main_menu + coin_count_images_len + letter_len_label_list + 1
        # ^the +1 is because of line 350 in info.py
        with patch.object(surface, "blit") as mock_blit:
            self.overhead_info.draw_main_menu_info(surface)
            self.assertEqual(mock_blit.call_count, total_expected_blit)

    def test_draw_loading_screen_info(self):
        surface = Mock()
        score_images_len = len(self.overhead_info.score_images)
        center_labels_total_len = 0
        for word in self.overhead_info.center_labels:
            for letter in word:
                center_labels_total_len += 1
        life_total_label_len = len(self.overhead_info.life_total_label)
        coin_count_images_len = len(self.overhead_info.coin_count_images)
        label_list_total_len = 0
        for label in self.overhead_info.label_list:
            for letter in label:
                label_list_total_len += 1
        total_expected_blit = score_images_len + center_labels_total_len + life_total_label_len + 2 + coin_count_images_len + label_list_total_len + 1
        with patch.object(surface, "blit") as mock_blit:
            self.overhead_info.draw_loading_screen_info(surface)
            self.assertEqual(mock_blit.call_count, total_expected_blit)

    def test_draw_level_screen_info(self):
        surface = Mock()
        score_images_len = len(self.overhead_info.score_images)
        count_down_images_len = len(self.overhead_info.count_down_images)
        coin_count_images_len = len(self.overhead_info.coin_count_images)
        label_list_total_len = 0
        for label in self.overhead_info.label_list:
            for letter in label:
                label_list_total_len += 1
        total_expected_blit = score_images_len + count_down_images_len + coin_count_images_len + label_list_total_len + 1
        with patch.object(surface, "blit") as mock_blit:
            self.overhead_info.draw_level_screen_info(surface)
            self.assertEqual(mock_blit.call_count, total_expected_blit)

    def test_draw_game_over_screen_info(self):
        surface = Mock()
        score_images_len = len(self.overhead_info.score_images)
        game_over_labels_total_count = 0
        for word in self.overhead_info.game_over_label:
            for letter in word:
                game_over_labels_total_count += 1
        coin_count_images_len = len(self.overhead_info.coin_count_images)
        label_list_total_len = 0
        for label in self.overhead_info.label_list:
            for letter in label:
                label_list_total_len += 1
        total_expected_blit = score_images_len + game_over_labels_total_count + coin_count_images_len + label_list_total_len + 1
        with patch.object(surface, "blit") as mock_blit:
            self.overhead_info.draw_game_over_screen_info(surface)
            self.assertEqual(mock_blit.call_count, total_expected_blit)

    def test_draw_time_out_screen_info(self):
        surface = Mock()
        score_images_len = len(self.overhead_info.score_images)
        time_out_labels_total_count = 0
        for word in self.overhead_info.time_out_label:
            for letter in word:
                time_out_labels_total_count += 1
        coin_count_images_len = len(self.overhead_info.coin_count_images)
        label_list_total_len = 0
        for label in self.overhead_info.label_list:
            for letter in label:
                label_list_total_len += 1

        total_expected_blit = score_images_len + time_out_labels_total_count + coin_count_images_len + label_list_total_len + 1
        with patch.object(surface, "blit") as mock_blit:
            self.overhead_info.draw_time_out_screen_info(surface)
            self.assertEqual(mock_blit.call_count, total_expected_blit)

# # Will look something like this!
#     with patch('SuperMarioLevel1.data.components.info.pg') as mock_pg:
#         self.overhead_info.state = c.MAIN_MENU
#         surface = Mock()
#         self.overhead_info.draw(surface)
#         blit_calls = surface.blit.call_args_list
#
#         # List of image names expected to be drawn on the surface for the main menu state
#         expected_images = [
#             'player_image',
#             'player_image_small'
#             # Add more image names if necessary
#         ]
#
#         for call in blit_calls:
#             image = call.args[0]
#             for img_name in expected_images:
#                 if image == self.overhead_info.score_images[img_name]:
#                     expected_images.remove(img_name)
#                     break
#
#         # Assert that all expected images have been drawn
#         self.assertEqual(len(expected_images), 0)
