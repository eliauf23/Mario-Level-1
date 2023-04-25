import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.states.level1 import Level1
import SuperMarioLevel1.data.setup as setup
import SuperMarioLevel1.data.tools as tools
from data.components import score, bricks, castle_flag
from data.components.powerups import LifeMushroom, Mushroom, Star, FireBall
from data.components.score import Score


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
                    with patch.object(self.level1, 'adjust_sprite_positions'):
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

    def test_check_mario_x_collisions_case_coin_box(self):
        pg.sprite.spritecollideany = Mock()
        coin_box = self.level1.coin_box_group.sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, coin_box, 0, 0, 0, 0]
        with patch.object(self.level1, 'adjust_mario_for_x_collisions') as mock_adjust_mario_for_x_collisions:
            self.level1.check_mario_x_collisions()
            mock_adjust_mario_for_x_collisions.assert_called_once_with(coin_box)

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

    # def test_update_all_sprites(self):
    #     with patch.object(self.level1, 'check_if_mario_in_transition_state') as mock_check_if_mario_in_transition_state:
    #         with patch.object(self.level1, 'check_for_mario_death') as mock_check_for_mario_death:
    #             with patch.object(self.level1, 'update_viewport') as mock_update_viewport:
    #                 self.level1.update_all_sprites(self.keys)
    #                 mock_check_if_mario_in_transition_state.assert_called_once_with()
    #                 mock_check_for_mario_death.assert_called_once_with()
    #                 mock_update_viewport.assert_called_once_with()

    def test_convert_mushrooms_to_fireflowers(self):
        for brick in self.level1.brick_group:
            brick.contents = c.MUSHROOM
        self.level1.convert_mushrooms_to_fireflowers()
        for brick in self.level1.brick_group:
            self.assertEqual(brick.contents, c.FIREFLOWER)

    def test_convert_fireflowers_to_mushrooms(self):
        self.level1.coin_box_group.sprites()[0].contents = c.FIREFLOWER
        for brick in self.level1.brick_group:
            brick.contents = c.FIREFLOWER
        self.level1.convert_fireflowers_to_mushrooms()
        for brick in self.level1.brick_group:
            self.assertEqual(brick.contents, c.MUSHROOM)
        for coin_box in self.level1.coin_group:
            self.assertEqual(coin_box.contents, c.MUSHROOM)

    # testing adjust_mario_for_x_collisions when if statement is true
    def test_adjust_mario_for_x_collisions_case_1(self):
        self.level1.adjust_mario_for_x_collisions(self.level1.coin_box_group.sprites()[0])
        self.assertEqual(self.level1.mario.rect.right, self.level1.coin_box_group.sprites()[0].rect.left)
        self.assertEqual(self.level1.mario.x_vel, 0)

    # testing adjust_mario_for_x_collisions when if statement is false
    def test_adjust_mario_for_x_collisions_case_2(self):
        self.level1.coin_box_group.sprites()[0].rect.x = -100000
        self.level1.adjust_mario_for_x_collisions(self.level1.coin_box_group.sprites()[0])
        self.assertEqual(self.level1.mario.rect.left, self.level1.coin_box_group.sprites()[0].rect.right)
        self.assertEqual(self.level1.mario.x_vel, 0)

    def test_adjust_mario_for_x_shell_collisions_case1(self):
        shell = self.level1.coin_box_group.sprites()[0]
        shell.state = c.JUMPED_ON
        old = shell.rect.x
        self.level1.adjust_mario_for_x_shell_collisions(shell)
        self.assertEqual(shell.direction, c.RIGHT)
        self.assertEqual(shell.x_vel, 5)
        self.assertEqual(old + 5, shell.rect.x)
        self.assertEqual(shell.state, c.SHELL_SLIDE)

    def test_adjust_mario_for_x_shell_collisions_case2(self):
        shell = self.level1.coin_box_group.sprites()[0]
        shell.state = c.JUMPED_ON
        old = shell.rect.x
        self.level1.mario.rect.x = 10000
        self.level1.adjust_mario_for_x_shell_collisions(shell)
        self.assertEqual(shell.direction, c.LEFT)
        self.assertEqual(shell.x_vel, -5)
        self.assertEqual(old - 5, shell.rect.x)
        self.assertEqual(shell.state, c.SHELL_SLIDE)

    def test_adjust_mario_for_x_shell_collisions_case3(self):
        shell = self.level1.coin_box_group.sprites()[0]
        shell.state = c.SHELL_SLIDE
        self.level1.mario.big = True
        self.level1.mario.invincible = False
        self.level1.adjust_mario_for_x_shell_collisions(shell)
        self.assertEqual(self.level1.mario.state, c.BIG_TO_SMALL)

    def test_adjust_mario_for_x_shell_collisions_case4(self):
        shell = self.level1.enemy_group_list[0].sprites()[0]
        shell.state = c.SHELL_SLIDE
        self.level1.mario.big = True
        self.level1.mario.invincible = True
        old_score = self.level1.game_info[c.SCORE]
        with patch.object(shell, 'start_death_jump') as mock_start_death_jump:
            self.level1.adjust_mario_for_x_shell_collisions(shell)
            mock_start_death_jump.assert_called_once_with(c.RIGHT)
            self.assertEqual(old_score + 200, self.level1.game_info[c.SCORE])
            assert shell in self.level1.sprites_about_to_die_group

    def test_adjust_mario_for_x_shell_collisions_case5(self):
        shell = self.level1.enemy_group_list[0].sprites()[0]
        shell.state = c.SHELL_SLIDE
        self.level1.mario.big = False
        self.level1.mario.invincible = False
        self.level1.mario.hurt_invincible = False
        with patch.object(self.level1.mario, 'start_death_jump') as mock_start_death_jump:
            self.level1.adjust_mario_for_x_shell_collisions(shell)
            self.assertEqual(self.level1.state, c.FROZEN)
            mock_start_death_jump.assert_called_once_with(self.level1.game_info)

    def test_check_mario_y_collisions_case_brick(self):
        pg.sprite.spritecollideany = Mock()
        brick = self.level1.brick_group.sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, brick, 0, 0]
        with patch.object(self.level1,
                          'adjust_mario_for_y_brick_collisions') as mock_adjust_mario_for_y_brick_collisions:
            with patch.object(self.level1, 'test_if_mario_is_falling') as mock_test_if_mario_is_falling:
                self.level1.check_mario_y_collisions()
                mock_adjust_mario_for_y_brick_collisions.assert_called_once_with(brick)
                mock_test_if_mario_is_falling.assert_called_once_with()

    def test_check_mario_y_collisions_case_coin_box(self):
        pg.sprite.spritecollideany = Mock()
        coin_box = self.level1.coin_box_group.sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, 0, coin_box, 0]
        with patch.object(self.level1,
                          'adjust_mario_for_y_coin_box_collisions') as mock_adjust_mario_for_y_coin_box_collisions:
            with patch.object(self.level1, 'test_if_mario_is_falling') as mock_test_if_mario_is_falling:
                self.level1.check_mario_y_collisions()
                mock_adjust_mario_for_y_coin_box_collisions.assert_called_once_with(coin_box)
                mock_test_if_mario_is_falling.assert_called_once_with()

    def test_check_mario_y_collisions_case_ground_step_or_pipe(self):
        pg.sprite.spritecollideany = Mock()
        ground_step_or_pipe = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany.side_effect = [ground_step_or_pipe, 0, 0, 0, 0, 0]
        with patch.object(self.level1,
                          'adjust_mario_for_y_ground_pipe_collisions') as mock_adjust_mario_for_y_ground_pipe_collisions:
            with patch.object(self.level1, 'test_if_mario_is_falling') as mock_test_if_mario_is_falling:
                self.level1.check_mario_y_collisions()
                mock_adjust_mario_for_y_ground_pipe_collisions.assert_called_once_with(ground_step_or_pipe)
                mock_test_if_mario_is_falling.assert_called_once_with()

    def test_check_mario_y_collisions_case_enemy_1(self):
        self.level1.mario.invincible = True
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, enemy, 0, 0, 0, 0]
        with patch.object(self.level1, 'test_if_mario_is_falling') as mock_test_if_mario_is_falling:
            self.level1.check_mario_y_collisions()
            # mock_adjust_mario_for_y_ground_pipe_collisions.assert_called_once_with(ground_step_or_pipe)
            mock_test_if_mario_is_falling.assert_called_once_with()
            assert enemy in self.level1.sprites_about_to_die_group

    def test_check_mario_y_collisions_case_enemy_2(self):
        self.level1.mario.invincible = False
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, enemy, 0, 0, 0, 0]
        with patch.object(self.level1, 'test_if_mario_is_falling') as mock_test_if_mario_is_falling:
            with patch.object(self.level1,
                              'adjust_mario_for_y_enemy_collisions') as mock_adjust_mario_for_y_enemy_collisions:
                self.level1.check_mario_y_collisions()
                mock_test_if_mario_is_falling.assert_called_once_with()
                mock_adjust_mario_for_y_enemy_collisions.assert_called_once_with(enemy)

    def test_check_mario_y_collisions_case_shell(self):
        pg.sprite.spritecollideany = Mock()
        shell = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, 0, shell, 0, 0, 0]
        with patch.object(self.level1, 'test_if_mario_is_falling') as mock_test_if_mario_is_falling:
            with patch.object(self.level1,
                              'adjust_mario_for_y_shell_collisions') as mock_adjust_mario_for_y_shell_collisions:
                self.level1.check_mario_y_collisions()
                mock_test_if_mario_is_falling.assert_called_once_with()
                mock_adjust_mario_for_y_shell_collisions.assert_called_once_with(shell)

    def test_check_mario_y_collisions_case_powerup(self):
        pg.sprite.spritecollideany = Mock()
        powerup = self.level1.enemy_group_list[0].sprites()[0]
        powerup.name = c.STAR
        # print(powerup)
        pg.sprite.spritecollideany.side_effect = [0, 0, 0, 0, 0, powerup]
        with patch.object(self.level1, 'test_if_mario_is_falling') as mock_test_if_mario_is_falling:
            self.level1.check_mario_y_collisions()
            mock_test_if_mario_is_falling.assert_called_once_with()
            self.assertTrue(self.level1.mario.invincible)
            self.assertEqual(self.level1.mario.invincible_start_timer, self.level1.current_time)

    # test when all if statements in prevent_collision_conflict evaluate to true
    def test_prevent_collision_conflict_all_ifs(self):
        brick = self.level1.brick_group.sprites()[0]
        coin_box = self.level1.coin_box_group.sprites()[0]
        o1, o2 = self.level1.prevent_collision_conflict(coin_box, brick)
        self.assertFalse(o2)

    # testing whether prevent_collision_conflict behaves corretly when the else statement is executed
    def test_prevent_collision_conflict_else(self):
        brick = self.level1.brick_group.sprites()[0]
        coin_box = self.level1.coin_box_group.sprites()[0]
        brick.rect.centerx = 0
        coin_box.rect.centerx = 0
        o1, o2 = self.level1.prevent_collision_conflict(coin_box, brick)
        self.assertFalse(o1)

    # testing adjust_mario_for_y_coin_box_collisions when all if statements evaluate to true
    def test_adjust_mario_for_y_coin_box_collisions_all_ifs(self):
        coin_box = self.level1.coin_box_group.sprites()[0]
        old_total = self.level1.game_info[c.SCORE]
        with patch.object(coin_box, 'start_bump') as mock_start_bump:
            self.level1.adjust_mario_for_y_coin_box_collisions(coin_box)
            mock_start_bump.assert_called_once_with(self.level1.moving_score_list)
            self.assertEqual(self.level1.mario.y_vel, 7)
            self.assertEqual(self.level1.mario.rect.y, coin_box.rect.bottom)
            self.assertEqual(self.level1.mario.state, c.FALL)
            self.assertEqual(old_total + 200, self.level1.game_info[c.SCORE])

    # testing adjust_mario_for_y_coin_box_collisions when executing elif statement (this does nothing as it's just pass)
    def test_adjust_mario_for_y_coin_box_collisions_elif(self):
        coin_box = self.level1.coin_box_group.sprites()[0]
        coin_box.state = c.OPENED
        self.level1.adjust_mario_for_y_coin_box_collisions(coin_box)

    # testing adjust_mario_for_y_coin_box_collisions when executing last else statement
    def test_adjust_mario_for_y_coin_box_collisions_last_else(self):
        coin_box = self.level1.coin_box_group.sprites()[0]
        self.level1.mario.rect.y = 0
        self.level1.adjust_mario_for_y_coin_box_collisions(coin_box)
        self.assertEqual(self.level1.mario.y_vel, 0)
        self.assertEqual(self.level1.mario.rect.bottom, coin_box.rect.top)
        self.assertEqual(self.level1.mario.state, c.WALK)

    # testing adjust_mario_for_y_coin_box_collisions when executing first else statement
    def test_adjust_mario_for_y_coin_box_collisions_first_else(self):
        coin_box = self.level1.coin_box_group.sprites()[0]
        coin_box.contents = c.COIN_TOTAL
        with patch.object(coin_box, 'start_bump') as mock_start_bump:
            self.level1.adjust_mario_for_y_coin_box_collisions(coin_box)
            mock_start_bump.assert_called_once_with(self.level1.moving_score_list)
            self.assertEqual(self.level1.mario.y_vel, 7)
            self.assertEqual(self.level1.mario.rect.y, coin_box.rect.bottom)
            self.assertEqual(self.level1.mario.state, c.FALL)

    # testing adjust_mario_for_y_brick_collisions when all if statements evaluate to true
    def test_adjust_mario_for_y_brick_collisions_all_ifs(self):
        brick = self.level1.brick_group.sprites()[0]
        brick.state = c.RESTING
        self.level1.mario.big = True
        brick.contents = None
        with patch.object(self.level1, 'check_if_enemy_on_brick') as mock_check_if_enemy_on_brick:
            with patch.object(brick, 'kill') as mock_kill:
                self.level1.adjust_mario_for_y_brick_collisions(brick)
                mock_check_if_enemy_on_brick.assert_called_once_with(brick)
                mock_kill.assert_called_once_with()

    # testing adjust_mario_for_y_brick_collisions when first else is executed
    def test_adjust_mario_for_y_brick_collisions_first_else(self):
        brick = self.level1.brick_group.sprites()[0]
        brick.state = c.RESTING
        brick.coin_total = 1
        self.level1.mario.big = False
        brick.contents = None
        old_coin_total = self.level1.game_info[c.COIN_TOTAL]
        old_score = self.level1.game_info[c.SCORE]
        with patch.object(self.level1, 'check_if_enemy_on_brick') as mock_check_if_enemy_on_brick:
            self.level1.adjust_mario_for_y_brick_collisions(brick)
            mock_check_if_enemy_on_brick.assert_called_once_with(brick)
            self.assertEqual(self.level1.game_info[c.COIN_TOTAL], old_coin_total + 1)
            self.assertEqual(self.level1.game_info[c.SCORE], old_score + 200)

    # testing adjust_mario_for_y_brick_collisions when first elif is executed
    def test_adjust_mario_for_y_brick_collisions_first_elif(self):
        brick = self.level1.brick_group.sprites()[0]
        brick.state = c.OPENED
        self.level1.adjust_mario_for_y_brick_collisions(brick)
        self.assertEqual(self.level1.mario.y_vel, 7)
        self.assertEqual(self.level1.mario.rect.y, brick.rect.bottom)
        self.assertEqual(self.level1.mario.state, c.FALL)

    # testing adjust_mario_for_y_brick_collisions when last else is executed
    def test_adjust_mario_for_y_brick_collisions_last_else(self):
        brick = self.level1.brick_group.sprites()[0]
        brick.state = c.OPENED
        self.level1.mario.rect.y = 0
        self.level1.adjust_mario_for_y_brick_collisions(brick)
        self.assertEqual(self.level1.mario.y_vel, 0)
        self.assertEqual(self.level1.mario.rect.bottom, brick.rect.top)
        self.assertEqual(self.level1.mario.state, c.WALK)

    # testing check_if_enemy_on_brick when both ifs eval to true
    def test_check_if_enemy_on_brick_both_ifs(self):
        brick = self.level1.brick_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [enemy, 0, 0, 0, 0, 0]
        self.level1.mario.rect.centerx = 10000000
        with patch.object(enemy, 'start_death_jump') as mock_start_death_jump:
            self.level1.check_if_enemy_on_brick(brick)
            assert enemy in self.level1.sprites_about_to_die_group
            mock_start_death_jump.assert_called_once_with('right')

    # testing check_if_enemy_on_brick when else statement is executed
    def test_check_if_enemy_on_brick_else(self):
        brick = self.level1.brick_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [enemy, 0, 0, 0, 0, 0]
        with patch.object(enemy, 'start_death_jump') as mock_start_death_jump:
            self.level1.check_if_enemy_on_brick(brick)
            assert enemy in self.level1.sprites_about_to_die_group
            mock_start_death_jump.assert_called_once_with('left')

    # testing adjust_mario_for_y_ground_pipe_collisions when elif evals to true
    def test_adjust_mario_for_y_ground_pipe_collisions_elif(self):
        collider = self.level1.coin_box_group.sprites()[0]
        # collider.rect.bottom = 100000
        # self.level1.mario.state = c.END_OF_LEVEL_FALL
        self.level1.adjust_mario_for_y_ground_pipe_collisions(collider)
        self.assertEqual(self.level1.mario.y_vel, 7)
        self.assertEqual(self.level1.mario.rect.top, collider.rect.bottom)
        self.assertEqual(self.level1.mario.state, c.FALL)

    # testing adjust_mario_for_y_ground_pipe_collisions when first if evals to true
    def test_adjust_mario_for_y_ground_pipe_collisions_first_else(self):
        collider = self.level1.coin_box_group.sprites()[0]
        collider.rect.bottom = 100000
        # self.level1.mario.state = c.END_OF_LEVEL_FALL
        self.level1.adjust_mario_for_y_ground_pipe_collisions(collider)
        self.assertEqual(self.level1.mario.y_vel, 0)
        self.assertEqual(self.level1.mario.rect.bottom, collider.rect.top)
        self.assertEqual(self.level1.mario.state, c.WALK)

    # testing adjust_mario_for_y_ground_pipe_collisions when both ifs eval to true
    def test_adjust_mario_for_y_ground_pipe_collisions_both_ifs(self):
        collider = self.level1.coin_box_group.sprites()[0]
        collider.rect.bottom = 100000
        self.level1.mario.state = c.END_OF_LEVEL_FALL

        self.level1.adjust_mario_for_y_ground_pipe_collisions(collider)
        self.assertEqual(self.level1.mario.y_vel, 0)
        self.assertEqual(self.level1.mario.rect.bottom, collider.rect.top)
        self.assertEqual(self.level1.mario.state, c.WALKING_TO_CASTLE)

    def test_test_if_mario_is_falling_inner_if(self):
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, None]
        self.level1.test_if_mario_is_falling()
        self.assertEqual(self.level1.mario.state, c.FALL)

    def test_test_if_mario_is_falling_inner_elif(self):
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, None]
        self.level1.mario.state = c.WALKING_TO_CASTLE
        self.level1.test_if_mario_is_falling()
        self.assertEqual(self.level1.mario.state, c.END_OF_LEVEL_FALL)

    def test_adjust_mario_for_y_enemy_collisions_both_ifs(self):
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        enemy.name = c.GOOMBA
        self.level1.mario.y_vel = 1
        self.level1.adjust_mario_for_y_enemy_collisions(enemy)
        self.assertEqual(enemy.state, c.JUMPED_ON)
        self.assertEqual(enemy.death_timer, self.level1.current_time)
        assert enemy in self.level1.sprites_about_to_die_group
        self.assertEqual(self.level1.mario.rect.bottom, enemy.rect.top)
        self.assertEqual(self.level1.mario.state, c.JUMP)
        self.assertEqual(self.level1.mario.y_vel, -7)

    def test_adjust_mario_for_y_enemy_collisions_elif(self):
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        enemy.name = c.KOOPA
        self.level1.mario.y_vel = 1
        self.level1.adjust_mario_for_y_enemy_collisions(enemy)
        self.assertEqual(enemy.state, c.JUMPED_ON)
        self.assertEqual(enemy.death_timer, self.level1.current_time)
        assert enemy in self.level1.shell_group
        self.assertEqual(self.level1.mario.rect.bottom, enemy.rect.top)
        self.assertEqual(self.level1.mario.state, c.JUMP)
        self.assertEqual(self.level1.mario.y_vel, -7)

    def test_adjust_mario_for_y_shell_collisions_all_ifs(self):
        shell = self.level1.enemy_group_list[0].sprites()[0]
        shell.state = c.JUMPED_ON
        self.level1.mario.rect.centerx = shell.rect.centerx - 1
        self.level1.mario.y_vel = 1
        self.level1.adjust_mario_for_y_shell_collisions(shell)
        self.assertEqual(shell.state, c.SHELL_SLIDE)
        self.assertEqual(shell.direction, c.RIGHT)
        self.assertEqual(shell.rect.left, self.level1.mario.rect.right + 5)

    def test_adjust_mario_for_y_shell_collisions_first_else(self):
        shell = self.level1.enemy_group_list[0].sprites()[0]
        shell.state = c.JUMPED_ON
        self.level1.mario.rect.centerx = shell.rect.centerx + 1
        self.level1.mario.y_vel = 1
        self.level1.adjust_mario_for_y_shell_collisions(shell)
        self.assertEqual(shell.state, c.SHELL_SLIDE)
        self.assertEqual(shell.direction, c.LEFT)
        self.assertEqual(shell.rect.right, self.level1.mario.rect.left - 5)

    def test_adjust_mario_for_y_shell_collisions_second_else(self):
        shell = self.level1.enemy_group_list[0].sprites()[0]
        shell.state = c.COIN_TOTAL
        self.level1.mario.rect.centerx = shell.rect.centerx + 1
        self.level1.mario.y_vel = 1
        self.level1.adjust_mario_for_y_shell_collisions(shell)
        self.assertEqual(shell.state, c.JUMPED_ON)

    def test_adjust_enemy_position(self):
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        self.level1.enemy_group.add(enemy)
        with patch.object(self.level1, 'delete_if_off_screen') as mock_delete_if_off_screen:
            self.level1.adjust_enemy_position()
            mock_delete_if_off_screen.assert_called_once_with(enemy)

    def test_check_enemy_x_collisions_collider_case_1(self):
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        enemy.direction = c.RIGHT
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany.side_effect = [collider, 0, 0, 0, 0, 0]
        self.level1.check_enemy_x_collisions(enemy)
        self.assertEqual(enemy.rect.right, collider.rect.left)
        self.assertEqual(enemy.direction, c.LEFT)
        self.assertEqual(enemy.x_vel, -2)
        assert enemy in self.level1.enemy_group
        assert self.level1.enemy_group in self.level1.mario_and_enemy_group

    def test_check_enemy_x_collisions_collider_case_2(self):
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        enemy.direction = c.LEFT
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany.side_effect = [collider, 0, 0, 0, 0, 0]
        self.level1.check_enemy_x_collisions(enemy)
        self.assertEqual(enemy.rect.left, collider.rect.right)
        self.assertEqual(enemy.direction, c.RIGHT)
        self.assertEqual(enemy.x_vel, 2)
        assert enemy in self.level1.enemy_group
        assert self.level1.enemy_group in self.level1.mario_and_enemy_group

    def test_check_enemy_x_collisions_enemy_collider_case_1(self):
        pg.sprite.spritecollideany = Mock()
        enemy_collider = self.level1.enemy_group_list[0].sprites()[0]
        enemy_collider.direction = c.RIGHT
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, enemy_collider, 0, 0, 0, 0]
        self.level1.check_enemy_x_collisions(enemy_collider)
        self.assertEqual(enemy_collider.rect.right, collider.rect.left)
        self.assertEqual(enemy_collider.direction, c.RIGHT)
        self.assertEqual(enemy_collider.x_vel, 2)
        assert enemy_collider in self.level1.enemy_group
        assert self.level1.enemy_group in self.level1.mario_and_enemy_group

    def test_check_enemy_x_collisions_enemy_collider_case_2(self):
        pg.sprite.spritecollideany = Mock()
        enemy_collider = self.level1.enemy_group_list[0].sprites()[0]
        enemy_collider.direction = c.LEFT
        pg.sprite.spritecollideany.side_effect = [0, enemy_collider, 0, 0, 0, 0]
        self.level1.check_enemy_x_collisions(enemy_collider)
        self.assertEqual(enemy_collider.direction, c.LEFT)
        self.assertEqual(enemy_collider.x_vel, -2)
        assert enemy_collider in self.level1.enemy_group
        assert self.level1.enemy_group in self.level1.mario_and_enemy_group

    def test_check_enemy_y_collisions_case_collider_1(self):
        pg.sprite.spritecollideany = Mock()
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        enemy.rect.bottom = 10000
        pg.sprite.spritecollideany.side_effect = [collider, 0, 0, 0, 0, 0]
        self.level1.check_enemy_y_collisions(enemy)
        self.assertEqual(enemy.y_vel, 7)
        self.assertEqual(enemy.rect.top, collider.rect.bottom)
        self.assertEqual(enemy.state, c.FALL)

    def test_check_enemy_y_collisions_case_collider_2(self):
        pg.sprite.spritecollideany = Mock()
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [collider, 0, 0, 0, 0, 0]
        self.level1.check_enemy_y_collisions(enemy)
        self.assertEqual(enemy.y_vel, 0)
        self.assertEqual(enemy.rect.bottom, collider.rect.top)
        self.assertEqual(enemy.state, c.WALK)

    # testing if statement inside 'if brick.state == c.BUMPED' in check_enemy_y_collisions
    def test_check_enemy_y_collisions_case_brick_bumped_if(self):
        brick = self.level1.brick_group.sprites()[0]
        brick.state = c.BUMPED
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, brick, 0, 0, 0, 0]
        self.level1.mario.rect.centerx = 10000
        with patch.object(enemy, 'start_death_jump') as mock_start_death_jump:
            self.level1.check_enemy_y_collisions(enemy)
            mock_start_death_jump.assert_called_once_with('right')
            assert enemy in self.level1.sprites_about_to_die_group

    # testing else statement inside 'if brick.state == c.BUMPED' in check_enemy_y_collisions
    def test_check_enemy_y_collisions_case_brick_bumped_else(self):
        brick = self.level1.brick_group.sprites()[0]
        brick.state = c.BUMPED
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, brick, 0, 0, 0, 0]
        # self.level1.mario.rect.centerx = 10000
        with patch.object(enemy, 'start_death_jump') as mock_start_death_jump:
            self.level1.check_enemy_y_collisions(enemy)
            mock_start_death_jump.assert_called_once_with('left')
            assert enemy in self.level1.sprites_about_to_die_group

    # testing elif enemy.rect.x > brick.rect.x in check_enemy_y_collisions
    def test_check_enemy_y_collisions_case_brick_elif(self):
        brick = self.level1.brick_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        enemy.rect.x = 10000
        pg.sprite.spritecollideany.side_effect = [0, brick, 0, 0, 0, 0]
        self.level1.check_enemy_y_collisions(enemy)
        self.assertEqual(enemy.y_vel, 7)
        self.assertEqual(enemy.rect.top, brick.rect.bottom)
        self.assertEqual(enemy.state, c.FALL)

    # testing else after elif enemy.rect.x > brick.rect.x in check_enemy_y_collisions
    def test_check_enemy_y_collisions_case_brick_else_after_elif(self):
        brick = self.level1.brick_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, brick, 0, 0, 0, 0]
        self.level1.check_enemy_y_collisions(enemy)
        self.assertEqual(enemy.y_vel, 0)
        self.assertEqual(enemy.rect.bottom, brick.rect.top)
        self.assertEqual(enemy.state, c.WALK)

    # testing if statement when coinbox is bumped in check_enemy_y_collisions
    def test_check_enemy_y_collisions_case_coin_box_bumped_if(self):
        coin_box = self.level1.coin_box_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, 0, coin_box, 0, 0, 0]
        coin_box.state = c.BUMPED
        self.level1.mario.rect.centerx = 1000
        # self.level1.check_enemy_y_collisions(enemy)
        with patch.object(enemy, 'start_death_jump') as mock_start_death_jump:
            self.level1.check_enemy_y_collisions(enemy)
            mock_start_death_jump.assert_called_once_with('right')
            assert enemy in self.level1.sprites_about_to_die_group

    # testing else statement when coinbox is bumped in check_enemy_y_collisions
    def test_check_enemy_y_collisions_case_coin_box_bumped_else(self):
        coin_box = self.level1.coin_box_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, 0, coin_box, 0, 0, 0]
        coin_box.state = c.BUMPED
        # self.level1.mario.rect.centerx = 1000
        # self.level1.check_enemy_y_collisions(enemy)
        with patch.object(enemy, 'start_death_jump') as mock_start_death_jump:
            self.level1.check_enemy_y_collisions(enemy)
            mock_start_death_jump.assert_called_once_with('left')
            assert enemy in self.level1.sprites_about_to_die_group

    # testing elif for coinbox when it's not bumped in check_enemy_y_collisions
    def test_check_enemy_y_collisions_case_coin_box_not_bumped_elif(self):
        coin_box = self.level1.coin_box_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, 0, coin_box, 0, 0, 0]
        enemy.rect.x = 700
        self.level1.check_enemy_y_collisions(enemy)
        self.assertEqual(enemy.y_vel, 7)
        self.assertEqual(enemy.rect.top, coin_box.rect.bottom)
        self.assertEqual(enemy.state, c.FALL)

    # testing elif for coinbox when it's not bumped in check_enemy_y_collisions
    def test_check_enemy_y_collisions_case_coin_box_not_bumped_else(self):
        coin_box = self.level1.coin_box_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [0, 0, coin_box, 0, 0, 0]
        self.level1.check_enemy_y_collisions(enemy)
        self.assertEqual(enemy.y_vel, 0)
        self.assertEqual(enemy.rect.bottom, coin_box.rect.top)
        self.assertEqual(enemy.state, c.WALK)

    # testing final else statement (with both ifs true) in check_enemy_y_collisions
    def test_check_enemy_y_collisions_case_last_else(self):
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany.side_effect = [None, None, None, None, None, None]
        self.level1.check_enemy_y_collisions(enemy)
        self.assertEqual(enemy.state, c.FALL)

    def test_adjust_shell_position(self):
        shell = self.level1.enemy_group_list[0].sprites()[0]
        self.level1.shell_group.add(shell)
        with patch.object(self.level1, 'delete_if_off_screen') as mock_delete_if_off_screen:
            self.level1.adjust_shell_position()
            mock_delete_if_off_screen.assert_called_once_with(shell)

    def test_check_shell_x_collisions_all_ifs(self):
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany.side_effect = [collider, enemy, None, None, None, None]
        shell = self.level1.enemy_group_list[0].sprites()[0]
        shell.x_vel = 1
        self.level1.check_shell_x_collisions(shell)
        assert enemy in self.level1.sprites_about_to_die_group
        self.assertEqual(shell.direction, c.LEFT)
        self.assertEqual(shell.rect.right, collider.rect.left)

    def test_check_shell_x_collisions_else(self):
        pg.sprite.spritecollideany = Mock()
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany.side_effect = [collider, enemy, None, None, None, None]
        shell = self.level1.enemy_group_list[0].sprites()[0]
        self.level1.check_shell_x_collisions(shell)
        assert enemy in self.level1.sprites_about_to_die_group
        self.assertEqual(shell.direction, c.RIGHT)
        self.assertEqual(shell.rect.left, collider.rect.right)

    def test_check_shell_y_collisions_if(self):
        pg.sprite.spritecollideany = Mock()
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany.side_effect = [collider, None, None, None, None, None]
        shell = self.level1.enemy_group_list[0].sprites()[0]
        self.level1.check_shell_y_collisions(shell)
        self.assertEqual(shell.state, c.SHELL_SLIDE)

    def test_check_shell_y_collisions_else(self):
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, None, None, None, None, None]
        shell = self.level1.enemy_group_list[0].sprites()[0]
        self.level1.check_shell_y_collisions(shell)
        self.assertEqual(shell.state, c.FALL)

    def test_adjust_powerup_position(self):
        mushroom = Mushroom(0, 0)
        star = Star(0, 0)
        fireball = FireBall(0, 0, False)
        life_mushroom = LifeMushroom(0, 0)
        self.level1.powerup_group.add(mushroom, star, fireball, life_mushroom)
        with patch.object(self.level1, 'adjust_mushroom_position') as mock_adjust_mushroom_position:
            with patch.object(self.level1, 'adjust_star_position') as mock_adjust_star_position:
                with patch.object(self.level1, 'adjust_fireball_position') as mock_adjust_fireball_position:
                    self.level1.adjust_powerup_position()
                    mock_adjust_mushroom_position.assert_called()
                    mock_adjust_star_position.assert_called_once_with(star)
                    mock_adjust_fireball_position.assert_called_once_with(fireball)

    def test_adjust_mushroom_position(self):
        mushroom = Mushroom(0, 0)
        mushroom.state = c.LEFT
        with patch.object(self.level1, 'check_mushroom_x_collisions') as mock_check_mushroom_x_collisions:
            with patch.object(self.level1, 'check_mushroom_y_collisions') as mock_check_mushroom_y_collisions:
                with patch.object(self.level1, 'delete_if_off_screen') as mock_delete_if_off_screen:
                    self.level1.adjust_mushroom_position(mushroom)
                    mock_check_mushroom_x_collisions.assert_called_once_with(mushroom)
                    mock_check_mushroom_y_collisions.assert_called_once_with(mushroom)
                    mock_delete_if_off_screen.assert_called_once_with(mushroom)

    def test_check_mushroom_x_collisions_case_1(self):
        mushroom = Mushroom(0, 0)
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [collider, None, None, None, None, None]
        with patch.object(self.level1, 'adjust_mushroom_for_collision_x') as mock_adjust_mushroom_for_collision_x:
            self.level1.check_mushroom_x_collisions(mushroom)
            mock_adjust_mushroom_for_collision_x.assert_called_once_with(mushroom, collider)

    def test_check_mushroom_x_collisions_case_2(self):
        mushroom = Mushroom(0, 0)
        brick = self.level1.brick_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, brick, None, None, None, None]
        with patch.object(self.level1, 'adjust_mushroom_for_collision_x') as mock_adjust_mushroom_for_collision_x:
            self.level1.check_mushroom_x_collisions(mushroom)
            mock_adjust_mushroom_for_collision_x.assert_called_once_with(mushroom, brick)

    def test_check_mushroom_x_collisions_case_3(self):
        mushroom = Mushroom(0, 0)
        coin_box = self.level1.coin_box_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, None, coin_box, None, None, None]
        with patch.object(self.level1, 'adjust_mushroom_for_collision_x') as mock_adjust_mushroom_for_collision_x:
            self.level1.check_mushroom_x_collisions(mushroom)
            mock_adjust_mushroom_for_collision_x.assert_called_once_with(mushroom, coin_box)

    def test_check_mushroom_y_collisions_case_1(self):
        mushroom = Mushroom(0, 0)
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [collider, None, None, None, None, None]
        with patch.object(self.level1, 'adjust_mushroom_for_collision_y') as mock_adjust_mushroom_for_collision_y:
            self.level1.check_mushroom_y_collisions(mushroom)
            mock_adjust_mushroom_for_collision_y.assert_called_once_with(mushroom, collider)

    def test_check_mushroom_y_collisions_case_2(self):
        mushroom = Mushroom(0, 0)
        brick = self.level1.brick_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, brick, None, None, None, None]
        with patch.object(self.level1, 'adjust_mushroom_for_collision_y') as mock_adjust_mushroom_for_collision_y:
            self.level1.check_mushroom_y_collisions(mushroom)
            mock_adjust_mushroom_for_collision_y.assert_called_once_with(mushroom, brick)

    def test_check_mushroom_y_collisions_case_3(self):
        mushroom = Mushroom(0, 0)
        coin_box = self.level1.coin_box_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, None, coin_box, None, None, None]
        with patch.object(self.level1, 'adjust_mushroom_for_collision_y') as mock_adjust_mushroom_for_collision_y:
            self.level1.check_mushroom_y_collisions(mushroom)
            mock_adjust_mushroom_for_collision_y.assert_called_once_with(mushroom, coin_box)

    def test_check_mushroom_y_collisions_case_4(self):
        mushroom = Mushroom(0, 0)
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, None, None, None, None, None]
        with patch.object(self.level1, 'check_if_falling') as mock_check_if_falling:
            self.level1.check_mushroom_y_collisions(mushroom)
            self.assertEqual(mock_check_if_falling.call_count, 3)

    def test_adjust_mushroom_for_collision_x_case_1(self):
        item = Mushroom(0, 0)
        collider = self.level1.coin_box_group.sprites()[0]
        self.level1.adjust_mushroom_for_collision_x(item, collider)
        self.assertEqual(item.rect.right, collider.rect.x)
        self.assertEqual(item.direction, c.LEFT)

    def test_adjust_mushroom_for_collision_x_case_2(self):
        item = Mushroom(0, 0)
        item.rect.x = 10000
        collider = self.level1.coin_box_group.sprites()[0]
        self.level1.adjust_mushroom_for_collision_x(item, collider)
        self.assertEqual(item.rect.x, collider.rect.right)
        self.assertEqual(item.direction, c.RIGHT)

    def test_adjust_mushroom_for_collision_y(self):
        item = Mushroom(0, 0)
        collider = self.level1.coin_box_group.sprites()[0]
        self.level1.adjust_mushroom_for_collision_y(item, collider)
        self.assertEqual(item.rect.bottom, collider.rect.y)
        self.assertEqual(item.state, c.SLIDE)
        self.assertEqual(item.y_vel, 0)

    def test_adjust_star_position(self):
        star = Star(0, 0)
        old_x = star.rect.x
        star.state = c.BOUNCE
        with patch.object(self.level1, 'delete_if_off_screen') as mock_delete_if_off_screen:
            self.level1.adjust_star_position(star)
            self.assertEqual(old_x + star.x_vel, star.rect.x)
            mock_delete_if_off_screen.assert_called_once_with(star)

    def test_check_star_y_collisions_case_1(self):
        star = Star(0, 0)
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [collider, None, None, None, None, None]
        with patch.object(self.level1, 'adjust_star_for_collision_y') as mock_adjust_star_for_collision_y:
            self.level1.check_star_y_collisions(star)
            mock_adjust_star_for_collision_y.assert_called_once_with(star, collider)

    def test_check_star_y_collisions_case_2(self):
        star = Star(0, 0)
        brick = self.level1.brick_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, brick, None, None, None, None]
        with patch.object(self.level1, 'adjust_star_for_collision_y') as mock_adjust_star_for_collision_y:
            self.level1.check_star_y_collisions(star)
            mock_adjust_star_for_collision_y.assert_called_once_with(star, brick)

    def test_check_star_y_collisions_case_3(self):
        star = Star(0, 0)
        coin_box = self.level1.coin_box_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, None, coin_box, None, None, None]
        with patch.object(self.level1, 'adjust_star_for_collision_y') as mock_adjust_star_for_collision_y:
            self.level1.check_star_y_collisions(star)
            mock_adjust_star_for_collision_y.assert_called_once_with(star, coin_box)

    def test_adjust_star_for_collision_y_case_1(self):
        star = Star(0, 0)
        star.rect.y = 10000
        collider = self.level1.coin_box_group.sprites()[0]
        self.level1.adjust_star_for_collision_y(star, collider)
        self.assertEqual(star.rect.y, collider.rect.bottom)
        self.assertEqual(star.y_vel, 0)

    def test_adjust_star_for_collision_y_case_2(self):
        star = Star(0, 0)
        collider = self.level1.coin_box_group.sprites()[0]
        self.level1.adjust_star_for_collision_y(star, collider)
        self.assertEqual(star.rect.bottom, collider.rect.top)

    def test_adjust_fireball_position_case_1(self):
        fireball = FireBall(0, 0, True)
        fireball.state = c.FLYING
        old_x = fireball.rect.x
        with patch.object(self.level1, 'delete_if_off_screen') as mock_delete_if_off_screen:
            self.level1.adjust_fireball_position(fireball)
            mock_delete_if_off_screen.assert_called_once_with(fireball)
            self.assertEqual(old_x + fireball.x_vel, fireball.rect.x)

    def test_adjust_fireball_position_case_2(self):
        fireball = FireBall(0, 0, True)
        fireball.state = c.BOUNCING
        old_y_vel = fireball.y_vel
        with patch.object(self.level1, 'delete_if_off_screen') as mock_delete_if_off_screen:
            self.level1.adjust_fireball_position(fireball)
            mock_delete_if_off_screen.assert_called_once_with(fireball)
            self.assertEqual(old_y_vel + fireball.gravity, fireball.y_vel)

    def test_bounce_fireball_case_1(self):
        fireball = FireBall(0, 0, True)
        self.level1.powerup_group.add(fireball)
        fireball.direction = c.RIGHT
        self.level1.bounce_fireball(fireball)
        self.assertEqual(fireball.x_vel, 15)
        self.assertEqual(fireball.state, c.BOUNCING)

    def test_bounce_fireball_case_2(self):
        fireball = FireBall(0, 0, True)
        self.level1.powerup_group.add(fireball)
        fireball.direction = c.LEFT
        self.level1.bounce_fireball(fireball)
        self.assertEqual(fireball.x_vel, -15)
        self.assertEqual(fireball.state, c.BOUNCING)

    def test_check_fireball_x_collisions(self):
        fireball = FireBall(0, 0, True)
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [collider, None, None, None, None, None]
        with patch.object(fireball, 'explode_transition') as mock_explode_transition:
            self.level1.check_fireball_x_collisions(fireball)
            mock_explode_transition.assert_called_once_with()
            assert fireball in self.level1.sprites_about_to_die_group

    def test_check_fireball_y_collisions_case_1(self):
        fireball = FireBall(0, 0, True)
        collider = self.level1.ground_step_pipe_group.sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [collider, None, None, None, None, None]
        self.level1.powerup_group.add(fireball)
        self.level1.check_fireball_y_collisions(fireball)
        self.assertEqual(fireball.rect.bottom, collider.rect.y)

    def test_check_fireball_y_collisions_case_2(self):
        fireball = FireBall(0, 0, True)
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, enemy, None, None, None, None]
        with patch.object(self.level1, 'fireball_kill') as mock_fireball_kill:
            self.level1.check_fireball_y_collisions(fireball)
            mock_fireball_kill.assert_called_once_with(fireball, enemy)

    def test_check_fireball_y_collisions_case_3(self):
        fireball = FireBall(0, 0, True)
        shell = self.level1.enemy_group_list[0].sprites()[0]
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, None, shell, None, None, None]
        with patch.object(self.level1, 'fireball_kill') as mock_fireball_kill:
            self.level1.check_fireball_y_collisions(fireball)
            mock_fireball_kill.assert_called_once_with(fireball, shell)

    def test_fireball_kill(self):
        fireball = FireBall(0, 0, True)
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        self.level1.fireball_kill(fireball, enemy)
        assert enemy, fireball in self.level1.sprites_about_to_die_group

    def test_check_if_falling(self):
        mushroom = Mushroom(0,0)
        mushroom.state = c.COIN
        pg.sprite.spritecollideany = Mock()
        pg.sprite.spritecollideany.side_effect = [None, None, None, None, None, None]
        self.level1.check_if_falling(mushroom, self.level1.ground_step_pipe_group)
        self.assertEqual(mushroom.state, c.FALL)

    def test_delete_if_off_screen_case_1(self):
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        enemy.rect.x = -1000
        with patch.object(enemy, 'kill') as mock_kill:
            self.level1.delete_if_off_screen(enemy)
            mock_kill.assert_called_once_with()

    def test_delete_if_off_screen_case_2(self):
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        self.level1.viewport.bottom = 0
        with patch.object(enemy, 'kill') as mock_kill:
            self.level1.delete_if_off_screen(enemy)
            mock_kill.assert_called_once_with()

    def test_delete_if_off_screen_case_3(self):
        enemy = self.level1.enemy_group_list[0].sprites()[0]
        enemy.state = c.SHELL_SLIDE
        self.level1.viewport.bottom = 9999990
        self.level1.viewport.right = -10000
        with patch.object(enemy, 'kill') as mock_kill:
            self.level1.delete_if_off_screen(enemy)
            mock_kill.assert_called_once_with()

    def test_check_flag(self):
        self.level1.flag.state = c.BOTTOM_OF_POLE
        self.level1.mario.state = c.FLAGPOLE
        with patch.object(self.level1.mario, 'set_state_to_bottom_of_pole') as mock_set_state_to_bottom_of_pole:
            self.level1.check_flag()
            mock_set_state_to_bottom_of_pole.assert_called_once_with()

    def test_check_to_add_flag_score(self):
        self.level1.flag_score = MagicMock()
        self.level1.flag_score.y_vel = 0
        old_score = self.level1.game_info[c.SCORE]
        self.level1.check_to_add_flag_score()
        self.assertEqual(old_score + self.level1.flag_score_total, self.level1.game_info[c.SCORE])
        self.assertEqual(self.level1.flag_score_total, 0)

    def test_check_for_mario_death(self):
        self.level1.mario.rect.y = 10000
        self.level1.mario.in_castle = False
        self.level1.mario.dead = True
        with patch.object(self.level1, 'play_death_song') as mock_play_death_song:
            self.level1.check_for_mario_death()
            self.assertTrue(self.level1.mario.dead)
            self.assertEqual(self.level1.mario.x_vel, 0)
            self.assertEqual(self.level1.state, c.FROZEN)
            self.assertTrue(self.level1.game_info[c.MARIO_DEAD])
            mock_play_death_song.assert_called_once_with()

    def test_play_death_song_case_1(self):
        self.level1.death_timer = 0
        self.level1.play_death_song()
        self.assertEqual(self.level1.death_timer, self.level1.current_time)

    def test_play_death_song_case_2(self):
        self.level1.death_timer = 1
        self.level1.current_time = 3999
        self.level1.play_death_song()
        self.assertTrue(self.level1.done)

    # tests set_game_info_values where all outer if statements eval to True
    def test_set_game_info_values_all_ifs(self):
        self.level1.game_info[c.SCORE] = 1
        self.level1.persist[c.TOP_SCORE] = 0
        self.level1.mario.dead = True
        self.level1.persist[c.LIVES] = 1
        self.level1.set_game_info_values()
        self.assertEqual(self.level1.persist[c.TOP_SCORE], self.level1.game_info[c.SCORE])
        self.assertEqual(self.level1.persist[c.LIVES], 0)
        self.assertEqual(self.level1.next, c.GAME_OVER)
        self.assertEqual(self.level1.game_info[c.CAMERA_START_X], 0)

    # testing whether set_game_info_values behaves correctly when second elif evals to True
    def test_set_game_info_values_second_elif(self):
        self.level1.mario.dead = True
        self.level1.persist[c.LIVES] = 100
        self.level1.overhead_info_display.time = 0
        self.level1.set_game_info_values()
        self.assertEqual(self.level1.next, c.TIME_OUT)

    # testing whether set_game_info_values behaves correctly when final else evals to True
    def test_set_game_info_values_final_else(self):
        self.level1.mario.dead = True
        self.level1.persist[c.LIVES] = 100
        self.level1.overhead_info_display.time = 1
        self.level1.mario.rect.x = 10000
        self.level1.game_info[c.CAMERA_START_X] = 0
        self.level1.set_game_info_values()
        self.assertEqual(self.level1.game_info[c.CAMERA_START_X], 3440)
        self.assertEqual(self.level1.next, c.LOAD_SCREEN)

    def test_check_if_time_out(self):
        self.level1.overhead_info_display.time = 0
        self.level1.mario.dead = False
        self.level1.mario.in_castle = False
        with patch.object(self.level1.mario, 'start_death_jump') as mock_start_death_jump:
            self.level1.check_if_time_out()
            self.assertEqual(self.level1.state, c.FROZEN)
            mock_start_death_jump.assert_called_once_with(self.level1.game_info)

    def test_update_viewport(self):
        self.level1.viewport.x = 128
        self.level1.viewport.w = 0
        self.level1.viewport.centerx = 10000
        self.level1.mario.x_vel += 1
        self.level1.update_viewport()
        self.assertEqual(self.level1.viewport.x, 128.5)

    def test_update_while_in_castle(self):
        self.level1.moving_score_list.append(
            score.Score(self.level1.mario.rect.right - self.level1.viewport.x,
                        self.level1.mario.rect.y, 100))
        self.level1.overhead_info_display.state = c.END_OF_LEVEL
        with patch.object(self.level1.overhead_info_display, 'update') as mock_update:
            self.level1.update_while_in_castle()
            mock_update.assert_called_once_with(self.level1.game_info)
            self.assertEqual(self.level1.state, c.FLAG_AND_FIREWORKS)

    def test_update_flag_and_fireworks(self):
        self.level1.moving_score_list.append(
            score.Score(self.level1.mario.rect.right - self.level1.viewport.x,
                        self.level1.mario.rect.y, 100))
        with patch.object(self.level1.overhead_info_display, 'update') as mock_update:
            with patch.object(self.level1.flag_pole_group, 'update') as mock_flag_update:
                with patch.object(self.level1, 'end_game') as mock_end_game:
                    self.level1.update_flag_and_fireworks()
                    mock_update.assert_called_once_with(self.level1.game_info)
                    mock_end_game.assert_called_once_with()
                    mock_flag_update.assert_called_once_with()

    # testing end_game when first if statement evals to true
    def test_end_game_case_1(self):
        self.level1.flag_timer = 0
        self.level1.end_game()
        self.assertEqual(self.level1.flag_timer, self.level1.current_time)

    # testing end_game when elif statement evals to true
    def test_end_game_case_2(self):
        self.level1.flag_timer = 1
        self.level1.current_time = 3000
        self.level1.end_game()
        self.assertEqual(self.level1.next, c.GAME_OVER)
        self.assertTrue(self.level1.done)

    def test_blit_everything(self):
        self.level1.moving_score_list.append(
            score.Score(self.level1.mario.rect.right - self.level1.viewport.x,
                        self.level1.mario.rect.y, 100))
        surface = MagicMock()
        self.level1.flag_score = MagicMock()
        self.level1.level = MagicMock()
        with patch.object(self.level1.level, 'blit') as mock_level_blit:
            self.level1.blit_everything(surface)
            mock_level_blit.assert_called_once_with(self.level1.background, self.level1.viewport, self.level1.viewport)