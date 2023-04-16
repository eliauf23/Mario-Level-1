import pygame as pg
from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock

import SuperMarioLevel1.data.tools as tools
from SuperMarioLevel1.data.components.mario import Mario
import SuperMarioLevel1.data.constants as c
import SuperMarioLevel1.data.setup as setup
from SuperMarioLevel1.data.components.powerups import FireBall


class TestMario(TestCase):
    def setUp(self) -> None:
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.mario = Mario()
        self.keys = {tools.keybinding['action']: False,
                     tools.keybinding['down']: False,
                     tools.keybinding['left']: False,
                     tools.keybinding['right']: False,
                     tools.keybinding['jump']: False}

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

    def test_standing(self):
        fire_group = MagicMock()
        self.mario.standing(self.keys, fire_group)

        # Assert that the frame_index, x_vel, and y_vel are set correctly
        self.assertEqual(self.mario.frame_index, 0)
        self.assertEqual(self.mario.x_vel, 0)
        self.assertEqual(self.mario.y_vel, 0)

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

    def test_jumping_to_death(self):
        self.mario.death_timer = 0
        self.mario.current_time = 1000
        self.mario.y_vel = 0
        self.mario.gravity = 1
        self.mario.jumping_to_death()
        self.assertEqual(self.mario.death_timer, 1000)
        self.assertEqual(self.mario.y_vel, 0)

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


    def test_check_if_invincible(self):
        self.mario.current_time = 10000
        self.mario.invincible = True
        self.mario.invincible_start_timer = self.mario.current_time - 11000
        self.mario.check_if_invincible()
        self.assertTrue(self.mario.losing_invincibility)
        self.mario.invincible_start_timer = self.mario.current_time - 13000
        self.mario.check_if_invincible()
        self.assertFalse(self.mario.invincible)

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
