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
        setup.SCREEN = MagicMock()  # this is so line 69 in level1.py doesn't cause an error

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
                    self.level1.update(1, 2, 3)
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

    def test_check_points_check_case1(self):
        checkpoint = pg.sprite.Sprite()
        checkpoint.name = '1'
        pg.sprite.spritecollideany = MagicMock(return_value=checkpoint)
        with patch.object(self.level1.enemy_group, 'add') as mock_add:
            self.level1.check_points_check()
            mock_add.assert_called_once_with(self.level1.enemy_group_list[0])

    def test_check_points_check_case2(self):
        checkpoint = pg.sprite.Sprite()
        checkpoint.name = '11'
        checkpoint.rect = pg.Rect(100, 100, 50, 50)
        pg.sprite.spritecollideany = MagicMock(return_value=checkpoint)
        self.level1.mario.rect = pg.Rect(0, 0, 0, 0)
        self.level1.check_points_check()
        self.assertEqual(self.level1.mario.state, c.FLAGPOLE)
        self.assertFalse(self.level1.mario.invincible)
        self.assertEqual(self.level1.mario.rect.bottom, self.level1.flag.rect.y)
        self.assertEqual(self.level1.flag.state, c.SLIDE_DOWN)

    def test_check_points_check_case3(self):
        checkpoint = pg.sprite.Sprite()
        checkpoint.name = '12'
        pg.sprite.spritecollideany = MagicMock(return_value=checkpoint)
        self.level1.check_points_check()
        self.assertEqual(self.level1.state, c.IN_CASTLE)
        ##!BUG FOUND!: line 455 of level1.py does nothing
        self.assertTrue(self.level1.mario.in_castle)
        self.assertEqual(self.level1.overhead_info_display.state, c.FAST_COUNT_DOWN)

    def test_check_points_check_case4(self):
        checkpoint = pg.sprite.Sprite()
        checkpoint.name = 'secret_mushroom'
        checkpoint.rect = pg.Rect(100, 100, 50, 50)
        pg.sprite.spritecollideany = MagicMock(return_value=checkpoint)
        self.level1.mario.y_vel = -1
        self.level1.check_points_check()
        self.assertEqual(self.level1.mario.y_vel, 7)
        self.assertEqual(self.level1.mario.state, c.FALL)

    def test_create_flag_points_case1(self):
        self.level1.mario.rect.bottom = c.GROUND_HEIGHT
        self.level1.create_flag_points()
        self.assertEqual(self.level1.flag_score.score_string, str(100))
        self.assertEqual(self.level1.flag_score_total, 100)

    def test_create_flag_points_case2(self):
        self.level1.mario.rect.bottom = c.GROUND_HEIGHT - 40 - 40 - 1
        self.level1.create_flag_points()
        self.assertEqual(self.level1.flag_score.score_string, str(400))
        self.assertEqual(self.level1.flag_score_total, 400)

    def test_create_flag_points_case3(self):
        self.level1.mario.rect.bottom = c.GROUND_HEIGHT - 40 - 160 - 1
        self.level1.create_flag_points()
        self.assertEqual(self.level1.flag_score.score_string, str(800))
        self.assertEqual(self.level1.flag_score_total, 800)

    def test_create_flag_points_case4(self):
        self.level1.mario.rect.bottom = c.GROUND_HEIGHT - 40 - 240 - 1
        self.level1.create_flag_points()
        self.assertEqual(self.level1.flag_score.score_string, str(2000))
        self.assertEqual(self.level1.flag_score_total, 2000)

    def test_create_flag_points_case5(self):
        self.level1.mario.rect.bottom = c.GROUND_HEIGHT - 40 - 360 - 1
        self.level1.create_flag_points()
        self.assertEqual(self.level1.flag_score.score_string, str(5000))
        self.assertEqual(self.level1.flag_score_total, 5000)

    def test_adjust_sprite_positions(self):
        with patch.object(self.level1, 'adjust_mario_position') as mock_adjust_mario_position:
            with patch.object(self.level1, 'adjust_enemy_position') as mock_adjust_enemy_position:
                self.level1.adjust_sprite_positions()
                mock_adjust_mario_position.assert_called_once_with()
                mock_adjust_enemy_position.assert_called_once_with()

    def test_adjust_mario_position_last_case(self):
        self.level1.mario.rect.x = self.level1.viewport.x + 4
        self.level1.adjust_mario_position()
        self.assertEqual(self.level1.mario.rect.x, self.level1.viewport.x + 5)

    def test_check_mario_x_collisions_case_brick(self):
        pg.sprite.spritecollideany = Mock()
        brick = pg.sprite.spritecollideany(self.level1.mario, self.level1.brick_group)
        pg.sprite.spritecollideany.side_effect = [0, 0, brick, 0, 0, 0]
        with patch.object(self.level1, 'adjust_mario_for_x_collisions') as mock_adjust_mario_for_x_collisions:
            self.level1.check_mario_x_collisions()
            mock_adjust_mario_for_x_collisions.assert_called_once_with(brick)

    def test_check_mario_x_collisions_case_collider(self):
        pg.sprite.spritecollideany = Mock()
        collider = pg.sprite.spritecollideany(self.level1.mario, self.level1.ground_step_pipe_group)
        pg.sprite.spritecollideany.side_effect = [collider, 0, 0, 0, 0, 0]
        with patch.object(self.level1, 'adjust_mario_for_x_collisions') as mock_adjust_mario_for_x_collisions:
            self.level1.check_mario_x_collisions()
            mock_adjust_mario_for_x_collisions.assert_called_once_with(collider)

    def test_check_mario_x_collisions_case_enemy_1(self):
        pg.sprite.spritecollideany = Mock()
        enemy = pg.sprite.spritecollideany(self.level1.mario, self.level1.enemy_group)
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, enemy, 0, 0]
        self.level1.mario.invincible = True
        with patch.object(self.level1.sprites_about_to_die_group, 'add') as mock_add:
            self.level1.check_mario_x_collisions()
            mock_add.assert_called_once_with(enemy)

    def test_check_mario_x_collisions_case_enemy_2(self):
        pg.sprite.spritecollideany = Mock()
        enemy = pg.sprite.spritecollideany(self.level1.mario, self.level1.enemy_group)
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, enemy, 0, 0]
        self.level1.mario.invincible = False
        self.level1.mario.big = True
        self.level1.check_mario_x_collisions()
        self.assertFalse(self.level1.mario.fire)
        self.assertEqual(self.level1.mario.y_vel, -1)
        self.assertEqual(self.level1.mario.state, c.BIG_TO_SMALL)

    def test_check_mario_x_collisions_case_enemy_3(self):
        pg.sprite.spritecollideany = Mock()
        enemy = pg.sprite.spritecollideany(self.level1.mario, self.level1.enemy_group)
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, enemy, 0, 0]
        self.level1.mario.invincible = False
        self.level1.mario.big = False
        self.level1.mario.hurt_invincible = True
        self.level1.check_mario_x_collisions()
        # note this function does nothing other than call a 'pass-only' branch

    def test_check_mario_x_collisions_case_enemy_4(self):
        pg.sprite.spritecollideany = Mock()
        enemy = pg.sprite.spritecollideany(self.level1.mario, self.level1.enemy_group)
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, enemy, 0, 0]
        self.level1.mario.invincible = False
        self.level1.mario.big = False
        self.level1.mario.hurt_invincible = False
        self.level1.check_mario_x_collisions()
        self.assertEqual(self.level1.state, c.FROZEN)

    def test_check_mario_x_collisions_case_shell(self):
        pg.sprite.spritecollideany = Mock()
        shell = pg.sprite.spritecollideany(self.level1.mario, self.level1.shell_group)
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, 0, shell, 0]
        with patch.object(self.level1,
                          'adjust_mario_for_x_shell_collisions') as mock_adjust_mario_for_x_shell_collisions:
            self.level1.check_mario_x_collisions()
            mock_adjust_mario_for_x_shell_collisions.assert_called_once_with(shell)

    def test_check_mario_x_collisions_case_powerup_1(self):
        pg.sprite.spritecollideany = Mock()
        powerup = pg.sprite.spritecollideany(self.level1.mario, self.level1.powerup_group)
        powerup.name = c.STAR
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, 0, 0, powerup]
        self.level1.check_mario_x_collisions()
        self.assertTrue(self.level1.mario.invincible)
        self.assertEqual(self.level1.mario.invincible_start_timer, self.level1.current_time)

    def test_check_mario_x_collisions_case_powerup_2(self):
        pg.sprite.spritecollideany = Mock()
        powerup = pg.sprite.spritecollideany(self.level1.mario, self.level1.powerup_group)
        powerup.name = c.MUSHROOM
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, 0, 0, powerup]
        self.level1.check_mario_x_collisions()
        self.assertTrue(self.level1.mario.in_transition_state)
        self.assertEqual(self.level1.mario.state, c.SMALL_TO_BIG)
        self.assertEqual(self.level1.mario.y_vel, -1)

    def test_check_mario_x_collisions_case_powerup_3(self):
        pg.sprite.spritecollideany = Mock()
        powerup = pg.sprite.spritecollideany(self.level1.mario, self.level1.powerup_group)
        powerup.name = c.LIFE_MUSHROOM
        powerup.rect = pg.Rect(100, 100, 50, 50)
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, 0, 0, powerup]
        old_lives = self.level1.game_info[c.LIVES]
        self.level1.check_mario_x_collisions()
        self.assertEqual(self.level1.game_info[c.LIVES], old_lives + 1)

    # tests check_mario_x_collisions when powerup!= 0 and powerup != None and
    # self.mario.big and self.mario.fire == False
    def test_check_mario_x_collisions_case_powerup_4_inner_if(self):
        pg.sprite.spritecollideany = Mock()
        powerup = pg.sprite.spritecollideany(self.level1.mario, self.level1.powerup_group)
        powerup.name = c.FIREFLOWER
        powerup.rect = pg.Rect(100, 100, 50, 50)
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, 0, 0, powerup]
        self.level1.mario.big = True
        self.level1.mario.fire = False
        self.level1.check_mario_x_collisions()
        self.assertEqual(self.level1.mario.state, c.BIG_TO_FIRE)
        self.assertTrue(self.level1.mario.in_transition_state)

    # tests check_mario_x_collisions when powerup!= 0 and powerup != None and
    # self.mario.big =False
    def test_check_mario_x_collisions_case_powerup_4_inner_elif(self):
        pg.sprite.spritecollideany = Mock()
        powerup = pg.sprite.spritecollideany(self.level1.mario, self.level1.powerup_group)
        powerup.name = c.FIREFLOWER
        powerup.rect = pg.Rect(100, 100, 50, 50)
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, 0, 0, powerup]
        self.level1.mario.big = False
        self.level1.mario.fire = False
        self.level1.check_mario_x_collisions()
        self.assertEqual(self.level1.mario.state, c.SMALL_TO_BIG)
        self.assertTrue(self.level1.mario.in_transition_state)


