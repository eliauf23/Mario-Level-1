import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock

import SuperMarioLevel1.data.tools as tools
from SuperMarioLevel1.data.components.mario import Mario
import SuperMarioLevel1.data.constants as c
import SuperMarioLevel1.data.setup as setup
from SuperMarioLevel1.data.components.powerups import FireBall


class TestMario(TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self) -> None:
        self.mario = Mario()
        self.keys = {tools.keybinding['action']: False,
                     tools.keybinding['down']: False,
                     tools.keybinding['left']: False,
                     tools.keybinding['right']: False,
                     tools.keybinding['jump']: False}

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

        assert (self.mario.key_timer == 0)
        assert (self.mario.state == c.WALK)

    def test_setup_timers(self):
        self.mario.setup_timers()
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

    def test_setup_state_booleans(self):
        self.mario.setup_state_booleans()
        self.assertEqual(self.mario.facing_right, True)
        self.assertEqual(self.mario.allow_jump, True)
        self.assertEqual(self.mario.dead, False)
        self.assertEqual(self.mario.invincible, False)
        self.assertEqual(self.mario.big, False)
        self.assertEqual(self.mario.fire, False)
        self.assertEqual(self.mario.allow_fireball, True)
        self.assertEqual(self.mario.in_transition_state, False)
        self.assertEqual(self.mario.hurt_invincible, False)
        self.assertEqual(self.mario.in_castle, False)
        self.assertEqual(self.mario.crouching, False)
        self.assertEqual(self.mario.losing_invincibility, False)

    def test_setup_forces(self):
        self.mario.setup_forces()
        self.assertEqual(self.mario.x_vel, 0)
        self.assertEqual(self.mario.y_vel, 0)
        self.assertEqual(self.mario.max_x_vel, c.MAX_WALK_SPEED)
        self.assertEqual(self.mario.max_y_vel, c.MAX_Y_VEL)
        self.assertEqual(self.mario.x_accel, c.WALK_ACCEL)
        self.assertEqual(self.mario.jump_vel, c.JUMP_VEL)
        self.assertEqual(self.mario.gravity, c.GRAVITY)

    def test_setup_counters(self):
        self.mario.setup_counters()
        self.assertEqual(self.mario.frame_index, 0)
        self.assertEqual(self.mario.invincible_index, 0)
        self.assertEqual(self.mario.fire_transition_index, 0)
        self.assertEqual(self.mario.fireball_count, 0)
        self.assertEqual(self.mario.flag_pole_right, 0)

    def test_load_images_from_sheet(self):
        pass

    def test_get_image(self):
        pass

    def test_update(self):
        # Create a Mario instance
        mario = Mario()

        # Create mock objects for keys, game_info, and fire_group
        keys = {'key1': True, 'key2': False}
        game_info = {c.CURRENT_TIME: 100}
        fire_group = MagicMock()

        # Patch the methods called within update
        with patch.object(mario, 'handle_state') as mock_handle_state, \
                patch.object(mario, 'check_for_special_state') as mock_check_for_special_state, \
                patch.object(mario, 'animation') as mock_animation:
            # Call the update method with the mock objects
            mario.update(keys, game_info, fire_group)

            # Assert that the methods were called with the correct arguments
            mock_handle_state.assert_called_once_with(keys, fire_group)
            mock_check_for_special_state.assert_called_once()
            mock_animation.assert_called_once()

            # Assert that the current_time is updated correctly
            self.assertEqual(mario.current_time, 100)

    def test_handle_state(self):
        states_methods = [
            (c.STAND, 'standing'),
            (c.WALK, 'walking'),
            (c.JUMP, 'jumping'),
            (c.FALL, 'falling'),
        ]
        fire_group_mock = MagicMock()
        for state, method_name in states_methods:
            self.mario.state = state
            with patch.object(self.mario, method_name) as mock_method:
                self.mario.handle_state(self.keys, fire_group_mock)
                mock_method.assert_called_once_with(self.keys, fire_group_mock)

    def test_handle_state_no_keys(self):
        states_methods = [
            (c.DEATH_JUMP, 'jumping_to_death'),
            (c.SMALL_TO_BIG, 'changing_to_big'),
            (c.BIG_TO_FIRE, 'changing_to_fire'),
            (c.BIG_TO_SMALL, 'changing_to_small'),
            (c.FLAGPOLE, 'flag_pole_sliding'),
            (c.BOTTOM_OF_POLE, 'sitting_at_bottom_of_pole'),
            (c.WALKING_TO_CASTLE, 'walking_to_castle'),
            (c.END_OF_LEVEL_FALL, 'falling_at_end_of_level')
        ]
        fire_group_mock = MagicMock()
        for state, method_name in states_methods:
            self.mario.state = state
            with patch.object(self.mario, method_name) as mock_method:
                self.mario.handle_state(self.keys, fire_group_mock)
                mock_method.assert_called_once_with()

    def test_standing(self):
        fire_group = MagicMock()
        self.mario.standing(self.keys, fire_group)

        # Assert that the frame_index, x_vel, and y_vel are set correctly
        self.assertEqual(self.mario.frame_index, 0)
        self.assertEqual(self.mario.x_vel, 0)
        self.assertEqual(self.mario.y_vel, 0)

    def test_standing_action(self):
        fire_group = MagicMock()
        self.keys[tools.keybinding['action']] = True
        self.mario.fire = True
        self.mario.allow_fireball = True
        with patch.object(self.mario, "shoot_fireball") as mock_shoot_fireball:
            self.mario.standing(self.keys, fire_group)
            mock_shoot_fireball.assert_called_once_with(fire_group)

    def test_standing_down(self):
        fire_group = MagicMock()
        self.keys[tools.keybinding['down']] = True
        self.mario.standing(self.keys, fire_group)
        self.assertTrue(self.mario.crouching)

    def test_standing_left(self):
        fire_group = MagicMock()
        self.keys[tools.keybinding['left']] = True
        with patch.object(self.mario, "get_out_of_crouch") as mock_get_out_of_crouch:
            self.mario.standing(self.keys, fire_group)
            self.assertFalse(self.mario.facing_right)
            mock_get_out_of_crouch.assert_called()
            self.assertEqual(self.mario.state, c.WALK)

    def test_standing_right(self):
        fire_group = MagicMock()
        self.keys[tools.keybinding['right']] = True
        with patch.object(self.mario, "get_out_of_crouch") as mock_get_out_of_crouch:
            self.mario.standing(self.keys, fire_group)
            self.assertTrue(self.mario.facing_right)
            mock_get_out_of_crouch.assert_called()
            self.assertEqual(self.mario.state, c.WALK)

    def test_standing_jump_big(self):
        fire_group = MagicMock()
        setup.SFX['big_jump'] = MagicMock()
        self.keys[tools.keybinding['jump']] = True
        self.mario.allow_jump = True
        self.mario.big = True
        with patch.object(setup.SFX['big_jump'], 'play') as mock_play:
            self.mario.standing(self.keys, fire_group)
            mock_play.assert_called_once_with()
            self.assertEqual(self.mario.state, c.JUMP)
            self.assertEqual(self.mario.y_vel, c.JUMP_VEL)

    def test_standing_jump_not_big(self):
        fire_group = MagicMock()
        setup.SFX['small_jump'] = MagicMock()
        self.keys[tools.keybinding['jump']] = True
        self.mario.allow_jump = True
        self.mario.big = False
        with patch.object(setup.SFX['small_jump'], 'play') as mock_play:
            self.mario.standing(self.keys, fire_group)
            mock_play.assert_called_once_with()
            self.assertEqual(self.mario.state, c.JUMP)
            self.assertEqual(self.mario.y_vel, c.JUMP_VEL)

    def test_get_out_of_crouch(self):
        self.mario.crouching = True
        bottom = self.mario.rect.bottom
        left = self.mario.rect.x

        self.mario.get_out_of_crouch()

        # Assert that the crouching attribute is set to False
        self.assertFalse(self.mario.crouching)

        # Assert that the rect's bottom and x are unchanged
        self.assertEqual(self.mario.rect.bottom, bottom)
        self.assertEqual(self.mario.rect.x, left)

    def test_get_out_of_crouch_not_facing_right(self):
        self.mario.facing_right = False
        self.mario.get_out_of_crouch()
        self.assertEqual(self.mario.image, self.mario.left_frames[0])

    def test_check_to_allow_jump(self):
        self.keys[tools.keybinding['jump']] = False
        self.mario.allow_jump = False

        self.mario.check_to_allow_jump(self.keys)

        # Assert that the allow_jump attribute is set to True
        self.assertTrue(self.mario.allow_jump)

    def test_check_to_allow_fireball(self):
        self.keys[tools.keybinding['action']] = False
        self.mario.allow_fireball = False

        self.mario.check_to_allow_fireball(self.keys)

        # Assert that the allow_fireball attribute is set to True
        self.assertTrue(self.mario.allow_fireball)

    def test_shoot_fireball(self):
        fire_group = MagicMock()
        setup.SFX['fireball'] = MagicMock()
        self.mario.fire = True
        self.mario.current_time = 1000  # Set the current_time attribute
        self.mario.last_fireball_time = 0  # Set the last_fireball_time attribute
        self.mario.shoot_fireball(fire_group)

        setup.SFX['fireball'].play.assert_called_once()
        fire_group.add.assert_called_once()

    def test_shoot_fireball_not_facing_right(self):
        fire_group = MagicMock()
        self.mario.facing_right = False
        setup.SFX['fireball'] = MagicMock()
        self.mario.fire = True
        self.mario.current_time = 1000  # Set the current_time attribute
        self.mario.last_fireball_time = 0  # Set the last_fireball_time attribute
        self.mario.shoot_fireball(fire_group)

        setup.SFX['fireball'].play.assert_called_once()
        fire_group.add.assert_called_once()
        self.assertEqual(self.mario.image, self.mario.left_frames[self.mario.frame_index])


    def test_count_number_of_fireballs(self):
        fire_group = MagicMock()
        powerup_group = [FireBall(0, 0, True) for _ in range(3)]
        fire_group.__iter__.return_value = powerup_group

        count = self.mario.count_number_of_fireballs(fire_group)

        # Assert that the count is correct
        self.assertEqual(count, len(powerup_group))

    def test_walking(self):
        self.mario.current_time = 1000  # Set the current_time attribute
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }

        fire_group = MagicMock()
        self.mario.walking(keys, fire_group)

        # Ensure Mario doesn't move if no keys are pressed
        self.assertEqual(self.mario.x_vel, 0)

    def test_walking_frame_index_not_0_less_than_3(self):
        fire_group = MagicMock()
        zero_func = lambda: 0
        self.mario.frame_index = 1
        with patch.object(self.mario, 'calculate_animation_speed', new=zero_func):
            self.mario.current_time = 100
            self.mario.walking_timer = 10
            self.mario.walking(self.keys, fire_group)
            self.assertEqual(self.mario.frame_index, 2)
            self.assertEqual(self.mario.walking_timer, self.mario.current_time)

    def test_walking_frame_index_not_0_not_less_than_3(self):
        self.mario.frame_index = 3
        fire_group = MagicMock()
        zero_func = lambda: 0
        with patch.object(self.mario, 'calculate_animation_speed', new=zero_func):
            self.mario.current_time = 100
            self.mario.walking_timer = 10
            self.mario.walking(self.keys, fire_group)
            self.assertEqual(self.mario.frame_index, 1)
            self.assertEqual(self.mario.walking_timer, self.mario.current_time)

    def test_walking_action(self):
        fire_group = MagicMock()
        self.keys[tools.keybinding['action']] = True
        self.mario.fire = True
        self.mario.allow_fireball = True
        self.mario.current_time = 0
        with patch.object(self.mario, 'shoot_fireball') as mock_shoot_fireball:
            self.mario.walking(self.keys, fire_group)
            mock_shoot_fireball.assert_called_once_with(fire_group)
            self.assertEqual(self.mario.max_x_vel, c.MAX_RUN_SPEED)
            self.assertEqual(self.mario.x_accel, c.RUN_ACCEL)

    def test_walking_jump_both_inner_ifs(self):
        fire_group = MagicMock()
        self.mario.big = True
        self.mario.current_time = 0
        self.mario.allow_jump = True
        setup.SFX['big_jump'] = MagicMock()
        self.keys[tools.keybinding['jump']] = True
        self.mario.x_vel = 5
        self.mario.walking(self.keys, fire_group)
        setup.SFX['big_jump'].play.assert_called_once()
        self.assertEqual(self.mario.y_vel, c.JUMP_VEL - 0.5)

    def test_walking_jump_both_inner_elses(self):
        fire_group = MagicMock()
        self.mario.big = False
        self.mario.current_time = 0
        self.mario.allow_jump = True
        setup.SFX['small_jump'] = MagicMock()
        self.keys[tools.keybinding['jump']] = True
        self.mario.x_vel = 4.5
        self.mario.walking(self.keys, fire_group)
        setup.SFX['small_jump'].play.assert_called_once()
        self.assertEqual(self.mario.y_vel, c.JUMP_VEL)

    def test_walking_left_all_ifs(self):
        fire_group = MagicMock()
        self.mario.current_time = 0
        self.keys[tools.keybinding['left']] = True
        self.mario.x_vel = 1
        self.mario.max_x_vel = 0
        with patch.object(self.mario, 'get_out_of_crouch') as mock_get_out_of_crouch:
            self.mario.walking(self.keys, fire_group)
            mock_get_out_of_crouch.assert_called_once_with()
            self.assertFalse(self.mario.facing_right)
            self.assertEqual(self.mario.frame_index, 5)
            self.assertEqual(self.mario.x_accel, c.SMALL_TURNAROUND)
            self.assertEqual(self.mario.x_vel, -0.5)

    def test_walking_left_all_elses(self):
        fire_group = MagicMock()
        self.mario.current_time = 0
        self.keys[tools.keybinding['left']] = True
        self.mario.x_vel = -10
        self.mario.max_x_vel = -1
        with patch.object(self.mario, 'get_out_of_crouch') as mock_get_out_of_crouch:
            self.mario.walking(self.keys, fire_group)
            mock_get_out_of_crouch.assert_called_once_with()
            self.assertFalse(self.mario.facing_right)
            self.assertEqual(self.mario.x_accel, c.WALK_ACCEL)
            self.assertEqual(self.mario.x_vel, -9.85)

    def test_walking_right_all_ifs(self):
        fire_group = MagicMock()
        self.mario.current_time = 0
        self.keys[tools.keybinding['right']] = True
        self.mario.x_vel = -1
        # self.mario.max_x_vel = 0
        with patch.object(self.mario, 'get_out_of_crouch') as mock_get_out_of_crouch:
            self.mario.walking(self.keys, fire_group)
            mock_get_out_of_crouch.assert_called_once_with()
            self.assertTrue(self.mario.facing_right)
            self.assertEqual(self.mario.frame_index, 5)
            self.assertEqual(self.mario.x_accel, c.SMALL_TURNAROUND)
            self.assertEqual(self.mario.x_vel, 0.5)

    def test_walking_right_all_elses(self):
        fire_group = MagicMock()
        self.mario.current_time = 0
        self.keys[tools.keybinding['right']] = True
        self.mario.x_vel = 10
        # self.mario.max_x_vel = -1
        with patch.object(self.mario, 'get_out_of_crouch') as mock_get_out_of_crouch:
            self.mario.walking(self.keys, fire_group)
            mock_get_out_of_crouch.assert_called_once_with()
            self.assertTrue(self.mario.facing_right)
            self.assertEqual(self.mario.x_accel, c.WALK_ACCEL)
            self.assertEqual(self.mario.x_vel, 9.85)

    def test_walking_second_to_last_branch(self):
        fire_group = MagicMock()
        self.mario.current_time = 0
        self.mario.facing_right = False
        self.mario.x_vel = -1
        self.mario.walking(self.keys, fire_group)
        self.assertEqual(self.mario.x_vel, -1 + self.mario.x_accel)

    def test_walking_last_branch(self):
        fire_group = MagicMock()
        self.mario.current_time = 0
        self.mario.facing_right = False
        self.mario.x_vel = 0
        self.mario.walking(self.keys, fire_group)
        self.assertEqual(self.mario.x_vel, 0)
        self.assertEqual(self.mario.state, c.STAND)


    def test_calculate_animation_speed(self):
        self.mario.x_vel = 0
        self.assertEqual(self.mario.calculate_animation_speed(), 130)

        self.mario.x_vel = 5
        self.assertEqual(self.mario.calculate_animation_speed(), 65)

        self.mario.x_vel = -5
        self.assertEqual(self.mario.calculate_animation_speed(), 65)

    def test_jumping(self):
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: True,
            tools.keybinding['action']: False
        }

        fire_group = MagicMock()
        self.mario.state = c.JUMP
        self.mario.jumping(keys, fire_group)

        # Ensure Mario's y_vel increases due to gravity
        self.assertGreater(self.mario.y_vel, 0)

    def test_jumping_left(self):
        self.keys[tools.keybinding['left']] = True
        self.mario.x_vel = 1
        self.mario.max_x_vel = 0
        fire_group = MagicMock()
        self.mario.jumping(self.keys, fire_group)
        self.assertEqual(self.mario.x_vel, 1-self.mario.x_accel)

    def test_jumping_right(self):
        self.keys[tools.keybinding['right']] = True
        self.mario.x_vel = 0
        self.mario.max_x_vel = 1
        fire_group = MagicMock()
        self.mario.jumping(self.keys, fire_group)
        self.assertEqual(self.mario.x_vel, self.mario.x_accel)

    def test_jumping_action(self):
        fire_group = MagicMock()
        self.keys[tools.keybinding['action']] = True
        self.mario.fire = True
        self.mario.allow_fireball = True
        with patch.object(self.mario, 'shoot_fireball') as mock_shoot_fireball:
            self.mario.jumping(self.keys, fire_group)
            mock_shoot_fireball.assert_called_once_with(fire_group)
    def test_falling(self):
        keys = {
            tools.keybinding['left']: False,
            tools.keybinding['right']: False,
            tools.keybinding['jump']: False,
            tools.keybinding['action']: False
        }

        fire_group = MagicMock()
        self.mario.state = c.FALL
        self.mario.y_vel = -5
        self.mario.falling(keys, fire_group)

        # Ensure Mario's y_vel increases due to gravity
        self.assertGreater(self.mario.y_vel, -5)

    def test_falling_left(self):
        self.keys[tools.keybinding['left']] = True
        self.mario.x_vel = 1
        self.mario.max_x_vel = 0
        fire_group = MagicMock()
        self.mario.falling(self.keys, fire_group)
        self.assertEqual(self.mario.x_vel, 1 - self.mario.x_accel)

    def test_falling_right(self):
        self.keys[tools.keybinding['right']] = True
        self.mario.x_vel = 0
        self.mario.max_x_vel = 1
        fire_group = MagicMock()
        self.mario.falling(self.keys, fire_group)
        self.assertEqual(self.mario.x_vel, self.mario.x_accel)

    def test_falling_action(self):
        fire_group = MagicMock()
        self.keys[tools.keybinding['action']] = True
        self.mario.fire = True
        self.mario.allow_fireball = True
        with patch.object(self.mario, 'shoot_fireball') as mock_shoot_fireball:
            self.mario.falling(self.keys, fire_group)
            mock_shoot_fireball.assert_called_once_with(fire_group)

    def test_timer_between_these_two_times(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.assertTrue(self.mario.timer_between_these_two_times(0, 51))
        self.assertFalse(self.mario.timer_between_these_two_times(51, 100))

    def test_set_mario_to_middle_image(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.set_mario_to_middle_image()
        self.assertEqual(self.mario.image, self.mario.normal_small_frames[0][7])
        self.assertEqual(self.mario.rect.bottom, 100)
        self.assertEqual(self.mario.rect.centerx, 50)

    def test_set_mario_to_middle_image_not_facing_right(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = False
        self.mario.set_mario_to_middle_image()
        self.assertEqual(self.mario.image, self.mario.normal_small_frames[1][7])
        self.assertEqual(self.mario.rect.bottom, 100)
        self.assertEqual(self.mario.rect.centerx, 50)

    def test_set_mario_to_small_image(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.set_mario_to_small_image()
        self.assertEqual(self.mario.image, self.mario.normal_small_frames[0][0])
        self.assertEqual(self.mario.rect.bottom, 100)
        self.assertEqual(self.mario.rect.centerx, 50)

    def test_set_mario_to_small_image_not_facing_right(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = False
        self.mario.set_mario_to_small_image()
        self.assertEqual(self.mario.image, self.mario.normal_small_frames[1][0])
        self.assertEqual(self.mario.rect.bottom, 100)
        self.assertEqual(self.mario.rect.centerx, 50)

    def test_set_mario_to_big_image(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.set_mario_to_big_image()
        self.assertEqual(self.mario.image, self.mario.normal_big_frames[0][0])
        self.assertEqual(self.mario.rect.bottom, 100)
        self.assertEqual(self.mario.rect.centerx, 50)

    def test_set_mario_to_big_image_not_facing_right(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = False
        self.mario.set_mario_to_big_image()
        self.assertEqual(self.mario.image, self.mario.normal_big_frames[1][0])
        self.assertEqual(self.mario.rect.bottom, 100)
        self.assertEqual(self.mario.rect.centerx, 50)

    def test_become_big(self):
        self.mario.become_big()
        self.assertTrue(self.mario.big)
        # self.assertEqual(self.mario.right_frames, self.mario.right_big_normal_frames)
        # self.assertEqual(self.mario.left_frames, self.mario.left_big_normal_frames)
        # self.assertEqual(self.mario.rect.bottom, 100)
        # self.assertEqual(self.mario.rect.x, 50)

    def test_changing_to_fire(self):
        self.mario.current_time = 100
        # self.mario.transition_timer = 50
        # self.mario.fire_transition_timer = 50
        # self.mario.rect.bottom = 100
        # self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_fire()
        self.assertTrue(self.mario.in_transition_state)
        # self.assertEqual(self.mario.image, self.mario.right_fire_frames[3])

    def test_changing_to_fire_not_facing_right(self):
        self.mario.current_time = 100
        self.mario.facing_right = False
        self.mario.changing_to_fire()
        self.assertTrue(self.mario.in_transition_state)

    #note these next tests are for the final elifs in changing_to_fire
    def test_changing_to_fire_1(self):
        self.mario.facing_right = True
        self.mario.current_time = 100
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, self.mario.right_fire_frames[3])

    def test_changing_to_fire_2(self):
        self.mario.facing_right = True
        self.mario.current_time = 195
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, self.mario.right_big_green_frames[3])

    def test_changing_to_fire_3(self):
        self.mario.facing_right = True
        self.mario.current_time = 260
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, self.mario.right_big_red_frames[3])

    def test_changing_to_fire_4(self):
        self.mario.facing_right = True
        self.mario.current_time = 325
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, self.mario.right_big_black_frames[3])

    def test_changing_to_fire_5(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 390
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[0])

    def test_changing_to_fire_6(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 455
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[1])

    def test_changing_to_fire_7(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 520
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[2])

    def test_changing_to_fire_8(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 585
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[3])

    def test_changing_to_fire_9(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 650
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[0])

    def test_changing_to_fire_10(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 715
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[1])

    def test_changing_to_fire_11(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 780
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[2])

    def test_changing_to_fire_12(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 845
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[3])

    def test_changing_to_fire_13(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 910
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[0])

    def test_changing_to_fire_14(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 975
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[1])

    def test_changing_to_fire_15(self):
        frames = [self.mario.right_fire_frames[3],
                  self.mario.right_big_green_frames[3],
                  self.mario.right_big_red_frames[3],
                  self.mario.right_big_black_frames[3]]
        self.mario.facing_right = True
        self.mario.current_time = 1040
        self.mario.fire_transition_timer = 1
        self.mario.changing_to_fire()
        self.assertEqual(self.mario.image, frames[2])
        self.assertTrue(self.mario.fire)
        self.assertFalse(self.mario.in_transition_state)
        self.assertEqual(self.mario.state, c.WALK)
        self.assertEqual(self.mario.transition_timer, 0)

    def test_changing_to_small(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, self.mario.right_big_normal_frames[4])

    # next tests are checking all the elifs in changing_to_small
    def test_changing_to_small_1(self):
        frames = [self.mario.right_big_normal_frames[4],
                  self.mario.right_big_normal_frames[8],
                  self.mario.right_small_normal_frames[8]
                  ]
        self.mario.current_time = 330
        self.mario.transition_timer = 1
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, frames[1])

    def test_changing_to_small_2(self):
        frames = [self.mario.right_big_normal_frames[4],
                  self.mario.right_big_normal_frames[8],
                  self.mario.right_small_normal_frames[8]
                  ]
        self.mario.current_time = 395
        self.mario.transition_timer = 1
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, frames[2])

    def test_changing_to_small_3(self):
        frames = [self.mario.right_big_normal_frames[4],
                  self.mario.right_big_normal_frames[8],
                  self.mario.right_small_normal_frames[8]
                  ]
        self.mario.current_time = 460
        self.mario.transition_timer = 1
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, frames[1])
    def test_changing_to_small_4(self):
        frames = [self.mario.right_big_normal_frames[4],
                  self.mario.right_big_normal_frames[8],
                  self.mario.right_small_normal_frames[8]
                  ]
        self.mario.current_time = 525
        self.mario.transition_timer = 1
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, frames[2])

    def test_changing_to_small_5(self):
        frames = [self.mario.right_big_normal_frames[4],
                  self.mario.right_big_normal_frames[8],
                  self.mario.right_small_normal_frames[8]
                  ]
        self.mario.current_time = 590
        self.mario.transition_timer = 1
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, frames[1])

    def test_changing_to_small_6(self):
        frames = [self.mario.right_big_normal_frames[4],
                  self.mario.right_big_normal_frames[8],
                  self.mario.right_small_normal_frames[8]
                  ]
        self.mario.current_time = 655
        self.mario.transition_timer = 1
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, frames[2])

    def test_changing_to_small_7(self):
        frames = [self.mario.right_big_normal_frames[4],
                  self.mario.right_big_normal_frames[8],
                  self.mario.right_small_normal_frames[8]
                  ]
        self.mario.current_time = 720
        self.mario.transition_timer = 1
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, frames[1])

    def test_changing_to_small_8(self):
        frames = [self.mario.right_big_normal_frames[4],
                  self.mario.right_big_normal_frames[8],
                  self.mario.right_small_normal_frames[8]
                  ]
        self.mario.current_time = 785
        self.mario.transition_timer = 1
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, frames[2])

    def test_changing_to_small_9(self):
        frames = [self.mario.right_big_normal_frames[4],
                  self.mario.right_big_normal_frames[8],
                  self.mario.right_small_normal_frames[8]
                  ]
        self.mario.current_time = 850
        self.mario.transition_timer = 1
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, frames[1])

    def test_changing_to_small_10(self):
        frames = [self.mario.right_big_normal_frames[4],
                  self.mario.right_big_normal_frames[8],
                  self.mario.right_small_normal_frames[8]
                  ]
        self.mario.current_time = 915
        self.mario.transition_timer = 1
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertFalse(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.WALK)
        self.assertEqual(self.mario.image, frames[2])


    def test_changing_to_small_transition_timer_zero(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 0
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = True
        self.mario.changing_to_small()
        self.assertEqual(self.mario.transition_timer, self.mario.current_time)
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
    def test_changing_to_small_not_facing_right(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.facing_right = False
        self.mario.changing_to_small()
        self.assertTrue(self.mario.in_transition_state)
        self.assertTrue(self.mario.hurt_invincible)
        self.assertEqual(self.mario.state, c.BIG_TO_SMALL)
        self.assertEqual(self.mario.image, self.mario.left_big_normal_frames[4])

    def test_adjust_rect(self):
        self.mario.adjust_rect()
        self.assertEqual(self.mario.rect.x, 0)
        self.assertEqual(self.mario.rect.bottom, 40)

    def test_become_small(self):
        # self.mario.current_time = 100
        # self.mario.transition_timer = 50
        # self.mario.fire_transition_timer = 50
        # self.mario.rect.bottom = 100
        # self.mario.rect.centerx = 50

        self.mario.become_small()
        self.assertFalse(self.mario.big)
        # self.assertEqual(self.mario.right_frames, self.mario.right_small_normal_frames)
        self.assertEqual(self.mario.left_frames, self.mario.left_small_normal_frames)
        # self.assertEqual(self.mario.rect.bottom, 100)
        # self.assertEqual(self.mario.rect.x, 50)

    def test_flag_pole_sliding(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50

        self.mario.flag_pole_right = 60
        self.mario.flag_pole_sliding()
        self.assertEqual(self.mario.state, c.FLAGPOLE)
        self.assertTrue(self.mario.in_transition_state)
        self.assertEqual(self.mario.image, self.mario.right_small_normal_frames[0])

    def test_flag_pole_sliding_elif_line_918(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50
        self.mario.flag_pole_timer = 1
        self.mario.flag_pole_right = 60
        self.mario.flag_pole_sliding()
        self.assertEqual(self.mario.state, c.FLAGPOLE)
        self.assertTrue(self.mario.in_transition_state)
        self.assertEqual(self.mario.image, self.mario.right_frames[10])

    def test_flag_pole_sliding_if_line_916(self):
        self.mario.current_time = 65
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50
        self.mario.flag_pole_timer = 1
        self.mario.flag_pole_right = 60
        self.mario.flag_pole_sliding()
        self.assertEqual(self.mario.state, c.FLAGPOLE)
        self.assertTrue(self.mario.in_transition_state)
        self.assertEqual(self.mario.image, self.mario.right_frames[9])

    def test_flag_pole_sliding_elif_line_920(self):
        self.mario.current_time = 131
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 100
        self.mario.rect.centerx = 50
        self.mario.flag_pole_timer = 1
        self.mario.flag_pole_right = 60
        self.mario.flag_pole_sliding()
        self.assertEqual(self.mario.state, c.FLAGPOLE)
        self.assertTrue(self.mario.in_transition_state)
        self.assertEqual(self.mario.flag_pole_timer, self.mario.current_time)
        # self.assertEqual(self.mario.image, self.mario.right_frames[9])

    def test_flag_pole_sliding_rect_bottom_488(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 488
        self.mario.rect.centerx = 50
        self.mario.flag_pole_timer = 1
        self.mario.flag_pole_right = 60
        self.mario.flag_pole_sliding()
        self.assertEqual(self.mario.state, c.FLAGPOLE)
        self.assertTrue(self.mario.in_transition_state)
        self.assertEqual(self.mario.flag_pole_timer, self.mario.current_time)

    def test_flag_pole_sliding_rect_bottom_493(self):
        self.mario.current_time = 100
        self.mario.transition_timer = 50
        self.mario.fire_transition_timer = 50
        self.mario.rect.bottom = 493
        self.mario.rect.centerx = 50
        self.mario.flag_pole_timer = 1
        self.mario.flag_pole_right = 60
        self.mario.flag_pole_sliding()
        self.assertEqual(self.mario.state, c.FLAGPOLE)
        self.assertTrue(self.mario.in_transition_state)
        self.assertEqual(self.mario.image, self.mario.right_frames[10])

    def test_sitting_at_bottom_of_pole_case_1(self):
        self.mario.current_time = 1
        self.mario.flag_pole_timer = 0
        self.mario.sitting_at_bottom_of_pole()
        self.assertEqual(self.mario.flag_pole_timer, self.mario.current_time)
        self.assertEqual(self.mario.image, self.mario.left_frames[10])

    def test_sitting_at_bottom_of_pole_case_2(self):
        self.mario.current_time = 2
        self.mario.flag_pole_timer = 1
        self.mario.sitting_at_bottom_of_pole()
        self.assertEqual(self.mario.image, self.mario.left_frames[10])

    def test_sitting_at_bottom_of_pole_case_3a(self):
        self.mario.current_time = 220
        self.mario.flag_pole_timer = 1
        self.mario.sitting_at_bottom_of_pole()
        self.assertFalse(self.mario.in_transition_state)
        self.assertEqual(self.mario.state, c.END_OF_LEVEL_FALL)

    def test_sitting_at_bottom_of_pole_case_3b(self):
        self.mario.current_time = 220
        self.mario.rect.bottom = 486
        self.mario.flag_pole_timer = 1
        self.mario.sitting_at_bottom_of_pole()
        self.assertFalse(self.mario.in_transition_state)
        self.assertEqual(self.mario.state, c.WALKING_TO_CASTLE)

    def test_jumping_to_death(self):
        self.mario.death_timer = 0
        self.mario.current_time = 1000
        self.mario.y_vel = 0
        self.mario.gravity = 1
        self.mario.jumping_to_death()
        self.assertEqual(self.mario.death_timer, 1000)
        self.assertEqual(self.mario.y_vel, 0)

    def test_jumping_to_death_elif(self):
        self.mario.death_timer = 1
        self.mario.current_time = 600
        self.mario.rect.y = 0
        self.mario.y_vel = 0
        self.mario.jumping_to_death()
        self.assertEqual(self.mario.rect.y, self.mario.y_vel-self.mario.gravity)


    def test_start_death_jump(self):
        game_info = {c.MARIO_DEAD: False}
        self.mario.start_death_jump(game_info)
        self.assertTrue(self.mario.dead)
        self.assertTrue(game_info[c.MARIO_DEAD])
        self.assertEqual(self.mario.y_vel, -11)
        self.assertEqual(self.mario.gravity, 0.5)
        self.assertEqual(self.mario.frame_index, 6)
        self.assertEqual(self.mario.state, c.DEATH_JUMP)
        self.assertTrue(self.mario.in_transition_state)

    def test_changing_to_big_1(self):
        self.mario.current_time = 0
        self.mario.transition_timer = 0
        self.mario.changing_to_big()
        self.assertEqual(self.mario.transition_timer, self.mario.current_time)

    def test_changing_to_big_2(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 135 and y == 200
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_middle_image') as mock_set_mario_to_middle_image:
                self.mario.changing_to_big()
                mock_set_mario_to_middle_image.assert_called_once_with()

    def test_changing_to_big_3(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 200 and y == 365
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_small_image') as mock_set_mario_to_small_image:
                self.mario.changing_to_big()
                mock_set_mario_to_small_image.assert_called_once_with()

    def test_changing_to_big_4(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 365 and y == 430
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_middle_image') as mock_set_mario_to_middle_image:
                self.mario.changing_to_big()
                mock_set_mario_to_middle_image.assert_called_once_with()

    def test_changing_to_big_5(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 430 and y == 495
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_small_image') as mock_set_mario_to_small_image:
                self.mario.changing_to_big()
                mock_set_mario_to_small_image.assert_called_once_with()

    def test_changing_to_big_6(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 495 and y == 560
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_middle_image') as mock_set_mario_to_middle_image:
                self.mario.changing_to_big()
                mock_set_mario_to_middle_image.assert_called_once_with()

    def test_changing_to_big_7(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 560 and y == 625
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_big_image') as mock_set_mario_to_big_image:
                self.mario.changing_to_big()
                mock_set_mario_to_big_image.assert_called_once_with()

    def test_changing_to_big_8(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 625 and y == 690
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_small_image') as mock_set_mario_to_small_image:
                self.mario.changing_to_big()
                mock_set_mario_to_small_image.assert_called_once_with()

    def test_changing_to_big_9(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 690 and y == 755
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_middle_image') as mock_set_mario_to_middle_image:
                self.mario.changing_to_big()
                mock_set_mario_to_middle_image.assert_called_once_with()

    def test_changing_to_big_10(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 755 and y == 820
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_big_image') as mock_set_mario_to_big_image:
                self.mario.changing_to_big()
                mock_set_mario_to_big_image.assert_called_once_with()

    def test_changing_to_big_11(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 820 and y == 885
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_small_image') as mock_set_mario_to_small_image:
                self.mario.changing_to_big()
                mock_set_mario_to_small_image.assert_called_once_with()

    def test_changing_to_big_12(self):
        self.mario.transition_timer = 1
        fn = lambda x,y: x == 885 and y == 950
        with patch.object(self.mario, 'timer_between_these_two_times', new = fn):
            with patch.object(self.mario, 'set_mario_to_big_image') as mock_set_mario_to_big_image:
                with patch.object(self.mario, 'become_big') as mock_become_big:
                    self.mario.changing_to_big()
                    mock_set_mario_to_big_image.assert_called_once_with()
                    mock_become_big.assert_called_once_with()
                    self.assertEqual(self.mario.state, c.WALK)
                    self.assertEqual(self.mario.transition_timer, 0)
                    self.assertFalse(self.mario.in_transition_state)

    def test_check_if_invincible(self):
        self.mario.current_time = 10000
        self.mario.invincible = True
        self.mario.invincible_start_timer = self.mario.current_time - 11000
        self.mario.check_if_invincible()
        self.assertTrue(self.mario.losing_invincibility)
        self.mario.invincible_start_timer = self.mario.current_time - 13000
        self.mario.check_if_invincible()
        self.assertFalse(self.mario.invincible)

    def test_check_if_invincible_first_if_in_outer_if(self):
        self.mario.invincible = True
        self.mario.current_time = 0
        self.mario.invincible_start_timer = 0
        with patch.object(self.mario, 'change_frame_list') as mock_change_frame_list:
            self.mario.check_if_invincible()
            self.assertFalse(self.mario.losing_invincibility)
            mock_change_frame_list.assert_called_once_with(30)

    def test_check_if_invincible_not_invisible_big(self):
        self.mario.invincible = False
        self.mario.big = True
        self.mario.check_if_invincible()
        self.assertEqual(self.mario.right_frames, self.mario.right_big_normal_frames)
        self.assertEqual(self.mario.left_frames, self.mario.left_big_normal_frames)

    def test_check_if_invincible_not_invisible_not_big(self):
        self.mario.invincible = False
        self.mario.big = False
        self.mario.check_if_invincible()
        self.assertEqual(self.mario.right_frames, self.mario.invincible_small_frames_list[0][0])
        self.assertEqual(self.mario.left_frames, self.mario.invincible_small_frames_list[0][1])

    def test_check_if_crouching(self):
        self.mario.crouching = True
        self.mario.big = True
        self.mario.facing_right = True
        self.mario.check_if_crouching()
        self.assertEqual(self.mario.image, self.mario.right_frames[7])

    def test_check_for_special_state(self):
        # Mock the methods called inside check_for_special_state
        self.mario.check_if_invincible = MagicMock()
        self.mario.check_if_fire = MagicMock()
        self.mario.check_if_hurt_invincible = MagicMock()
        self.mario.check_if_crouching = MagicMock()

        # Call the method
        self.mario.check_for_special_state()

        # Check if the mocked methods were called
        self.mario.check_if_invincible.assert_called_once()
        self.mario.check_if_fire.assert_called_once()
        self.mario.check_if_hurt_invincible.assert_called_once()
        self.mario.check_if_crouching.assert_called_once()

    def test_set_state_to_bottom_of_pole_big(self):
        self.mario.big = True
        self.mario.rect.right = 100
        self.mario.set_state_to_bottom_of_pole()
        self.assertEqual(self.mario.image, self.mario.left_frames[9])
        self.assertEqual(self.mario.rect.x, 90)
        self.assertEqual(self.mario.flag_pole_timer, 0)
        self.assertEqual(self.mario.state, c.BOTTOM_OF_POLE)

    def test_walking_to_castle_both_ifs(self):
        self.mario.current_time = 2
        self.mario.x_vel = 0
        self.mario.walking_timer = 0
        self.mario.walking_to_castle()
        self.assertEqual(self.mario.max_x_vel, 5)
        self.assertEqual(self.mario.x_accel, c.WALK_ACCEL)
        self.assertEqual(self.mario.x_vel, self.mario.x_accel)

    def test_walking_to_castle_if_elif_if(self):
        self.mario.current_time = 100
        self.mario.walking_timer = 1
        self.mario.frame_index = 2
        ret_neg_1000 = lambda : -1000
        with patch.object(self.mario, 'calculate_animation_speed', new=ret_neg_1000):
            self.mario.walking_to_castle()
            self.assertEqual(self.mario.max_x_vel, 5)
            self.assertEqual(self.mario.x_accel, c.WALK_ACCEL)
            self.assertEqual(self.mario.frame_index, 3)
            self.assertEqual(self.mario.walking_timer, self.mario.current_time)

    def test_walking_to_castle_if_elif_else(self):
        self.mario.current_time = 100
        self.mario.walking_timer = 1
        self.mario.frame_index = 3
        ret_neg_1000 = lambda : -1000
        with patch.object(self.mario, 'calculate_animation_speed', new=ret_neg_1000):
            self.mario.walking_to_castle()
            self.assertEqual(self.mario.max_x_vel, 5)
            self.assertEqual(self.mario.x_accel, c.WALK_ACCEL)
            self.assertEqual(self.mario.frame_index, 1)
            self.assertEqual(self.mario.walking_timer, self.mario.current_time)

    def test_falling_at_end_of_level(self):
        self.mario.y_vel = 0
        self.mario.falling_at_end_of_level()
        self.assertEqual(self.mario.y_vel, c.GRAVITY)

    def test_change_frame_list_first_else_and_big(self):
        self.mario.big = True
        self.mario.current_time = 100
        self.mario.invincible_animation_timer = 0
        self.mario.invincible_index = 100
        self.mario.change_frame_list(1)
        self.assertEqual(self.mario.invincible_index, 0)
        self.assertEqual(self.mario.invincible_animation_timer, self.mario.current_time)
        self.assertEqual(self.mario.right_frames, self.mario.invincible_big_frames_list[self.mario.invincible_index][0])
        self.assertEqual(self.mario.left_frames, self.mario.invincible_big_frames_list[self.mario.invincible_index][1])