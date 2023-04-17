import pygame as pg
from unittest.mock import MagicMock, patch, Mock, ANY
from SuperMarioLevel1.data.components.info import OverheadInfo
import SuperMarioLevel1.data.constants as c
from unittest import TestCase

class TestOverheadInfo(TestCase):
    def setUp(self):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.game_info = {c.COIN_TOTAL: 0, c.LIVES: 3, c.TOP_SCORE: 0}
        self.overhead_info = OverheadInfo(self.game_info, state=c.MAIN_MENU)

    def tearDown(self) -> None:
        pg.quit()

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
        with patch.object(self.overhead_info, 'update_score_images') as mock_update_score_images,\
             patch.object(self.overhead_info, 'update_coin_total') as mock_update_coin_total,\
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

    def test_draw_main_menu_info(self):
        # TODO: Add test for the draw method
        pass
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

