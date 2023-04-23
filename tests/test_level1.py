import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.states.level1 import Level1
import SuperMarioLevel1.data.setup as setup
import SuperMarioLevel1.data.tools as tools
from data.components import score


class TestLevel1(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        setup.SCREEN = MagicMock() # this is so line 69 in level1.py doesn't cause an error

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self) -> None:
        self.level1 = Level1()
        CURRENT_TIME = 1
        self.persist = {
            c.COIN_TOTAL: 2,
            c.LIVES: 3,
            c.TOP_SCORE: 21,
            c.CAMERA_START_X: 3
        }
        self.level1.startup(CURRENT_TIME, self.persist)
        self.level1.game_info[c.SCORE] = 0
        self.keys = {
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False,
            tools.keybinding['left']: False,
            tools.keybinding['right']: False
        }

    def test_init(self):
        self.assertIsInstance(self.level1, Level1)

    def test_startup(self):
        self.assertEqual(self.level1.game_info, self.persist)
        self.assertEqual(self.level1.state, c.NOT_FROZEN)
        self.assertEqual(self.level1.death_timer, 0)
        self.assertEqual(self.level1.flag_timer, 0)
        self.assertEqual(self.level1.flag_score_total, 0)

    def test_update(self):
        with patch.object(self.level1, 'handle_states') as mock_handle_states:
            with patch.object(self.level1, 'check_if_time_out') as mock_check_if_time_out:
                with patch.object(self.level1, 'blit_everything') as mock_blit_everything:
                    self.level1.update(1,2,3)
                    mock_handle_states.assert_called_once_with(2)
                    mock_check_if_time_out.assert_called_once_with()
                    mock_blit_everything.assert_called_once_with(1)

    def test_handle_states_case1(self):
        self.level1.state = c.FROZEN
        with patch.object(self.level1, 'update_during_transition_state') as mock_update_during_transition_state:
            self.level1.handle_states("keys?")
            mock_update_during_transition_state.assert_called_once_with("keys?")

    def test_handle_states_case2(self):
        self.level1.state = c.NOT_FROZEN
        with patch.object(self.level1, 'update_all_sprites') as mock_update_all_sprites:
            self.level1.handle_states("keys?")
            mock_update_all_sprites.assert_called_once_with("keys?")

    def test_handle_states_case3(self):
        self.level1.state = c.IN_CASTLE
        with patch.object(self.level1, 'update_while_in_castle') as mock_update_while_in_castle:
            self.level1.handle_states("keys?")
            mock_update_while_in_castle.assert_called_once_with()

    def test_handle_states_case4(self):
        self.level1.state = c.FLAG_AND_FIREWORKS
        with patch.object(self.level1, 'update_flag_and_fireworks') as mock_update_flag_and_fireworks:
            self.level1.handle_states("keys?")
            mock_update_flag_and_fireworks.assert_called_once_with()

    def test_update_during_transition_state(self):

        # below is so moving_score_list is nonempty
        self.level1.moving_score_list.append(
            score.Score(self.level1.mario.rect.right - self.level1.viewport.x,
                        self.level1.mario.rect.y, 100))
        self.level1.flag_score = score.Score(1, 1, 100, True)
        with patch.object(self.level1.mario, 'update') as mock_update:
            with patch.object(self.level1.overhead_info_display, 'update') as mock_update_2:
                with patch.object(self.level1, 'check_to_add_flag_score') as mock_check_to_add_flag_score:
                    self.level1.update_during_transition_state(self.keys)
                    mock_update.assert_called_once_with(self.keys, self.level1.game_info, self.level1.powerup_group)
                    mock_update_2.assert_called_once_with(self.level1.game_info, self.level1.mario)
                    mock_check_to_add_flag_score.assert_called_once_with()

    def test_check_if_mario_in_transition_state_case1(self):
        self.level1.mario.in_transition_state = True
        self.level1.check_if_mario_in_transition_state()
        self.assertEqual(self.level1.game_info[c.LEVEL_STATE], c.FROZEN)

    def test_check_if_mario_in_transition_state_case2(self):
        self.level1.mario.in_transition_state = False
        self.level1.state = c.FROZEN
        self.level1.check_if_mario_in_transition_state()
        self.assertEqual(self.level1.game_info[c.LEVEL_STATE], c.NOT_FROZEN)

    def test_update_all_sprites(self):
        self.level1.moving_score_list.append(
            score.Score(self.level1.mario.rect.right - self.level1.viewport.x,
                        self.level1.mario.rect.y, 100))
        self.level1.flag_score = score.Score(1, 1, 100, True)
        with patch.object(self.level1.mario, 'update') as mock_update:
            with patch.object(self.level1.overhead_info_display, 'update') as mock_update_2:
                with patch.object(self.level1, 'check_to_add_flag_score') as mock_check_to_add_flag_score:
                    self.level1.update_all_sprites(self.keys)
                    mock_update.assert_called_once_with(self.keys, self.level1.game_info, self.level1.powerup_group)
                    mock_update_2.assert_called_once_with(self.level1.game_info, self.level1.mario)
                    mock_check_to_add_flag_score.assert_called_once_with()

