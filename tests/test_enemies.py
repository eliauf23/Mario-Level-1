import unittest
import pygame as pg
import SuperMarioLevel1.data.constants as c
from SuperMarioLevel1.data.components.enemies import Enemy, Goomba, Koopa
from unittest.mock import Mock

class TestEnemy(unittest.TestCase):
    
    def setUp(self):
        pg.init()
        pg.display.set_mode(c.SCREEN_SIZE)
       
    
    
    def test_set_velocity(self):
        """Test that set_velocity sets x_vel to negative when direction is LEFT and to positive when direction is RIGHT"""
        enemy = Enemy()
        enemy.direction = c.LEFT
        enemy.set_velocity()
        self.assertTrue(enemy.x_vel < 0)
        enemy.direction = c.RIGHT
        enemy.set_velocity()
        self.assertTrue(enemy.x_vel > 0)

    

    def test_get_image(self):
        """Test that get_image returns a surface with the correct dimensions"""
        enemy = Goomba()
        image = enemy.get_image(0, 0, 16, 16)
        self.assertIsInstance(image, pg.Surface)
        self.assertEqual(image.get_width(), 16 * c.SIZE_MULTIPLIER)
        self.assertEqual(image.get_height(),  16 * c.SIZE_MULTIPLIER)
        #self.assertEqual(image.get_colorkey(), c.BLACK)
        # add more checking

    def test_handle_state_walking(self):
        enemy = Enemy()
        enemy.state = c.WALK
        enemy.walking = Mock()
        enemy.handle_state()
        enemy.walking.assert_called_once()

    def test_handle_state_falling(self):
        enemy = Enemy()
        enemy.state = c.FALL
        enemy.falling = Mock()
        enemy.handle_state()
        enemy.falling.assert_called_once()

    def test_handle_state_jumped_on(self):
        enemy = Enemy()
        enemy.state = c.JUMPED_ON
        enemy.jumped_on = Mock()
        enemy.handle_state()
        enemy.jumped_on.assert_called_once()

    def test_handle_state_shell_sliding(self):
        enemy = Enemy()
        enemy.state = c.SHELL_SLIDE
        enemy.shell_sliding = Mock()
        enemy.handle_state()
        enemy.shell_sliding.assert_called_once()

    def test_handle_state_death_jumping(self):
        enemy = Enemy()
        enemy.state = c.DEATH_JUMP
        enemy.death_jumping = Mock()
        enemy.handle_state()
        enemy.death_jumping.assert_called_once()

    def test_walking(self):
        """Test that walking updates the frame_index"""
        enemy = Enemy()
        enemy.current_time = 150
        enemy.animate_timer = 0
        enemy.frame_index = 0
        enemy.walking()
        self.assertEqual(enemy.frame_index, 1)
        enemy.current_time = 150
        enemy.animate_timer = 0
        enemy.walking()
        self.assertEqual(enemy.frame_index, 0)

    def test_falling(self):
        """Test that falling leads to an increase in falling speed but that falling speed will eventually slow"""
        enemy = Enemy()
        enemy.y_vel = 0
        original_vel = enemy.y_vel
        enemy.gravity = 1.5
        enemy.falling()
        self.assertTrue(enemy.y_vel > original_vel)
        enemy.y_vel = 11
        enemy.falling()
        self.assertEqual(enemy.y_vel, 11)

    def test_jumped_on(self):
       enemy = Enemy()
       enemy.jumped_on()
       self.assertTrue(True);

    def test_death_jumping(self):
        """Test that death_jumping updates the rect and y_vel"""
        enemy = Goomba()
        enemy.rect = pg.Rect(0, 0, 16, 16)
        enemy.start_death_jump(c.RIGHT)
        enemy.death_jumping()

        #self.assertTrue(enemy.rect.bottom > 600)
        #self.assertEqual(enemy.y_vel, c.GRAVITY)
        self.assertFalse(enemy.alive())

        # add testing for enemy committing suicide

    def test_start_death_jump(self):
        # Test that the enemy jumps with correct velocity and direction
        enemy = Goomba()
        enemy.start_death_jump(c.RIGHT)
        self.assertEqual(enemy.y_vel, -8)
        self.assertEqual(enemy.x_vel, 2)
        self.assertEqual(enemy.gravity, .5)
        self.assertEqual(enemy.frame_index, 3)
        self.assertEqual(enemy.image, enemy.frames[3])
        self.assertEqual(enemy.state, c.DEATH_JUMP)
        enemy.start_death_jump(c.LEFT)
        self.assertEqual(enemy.y_vel, -8)
        self.assertEqual(enemy.x_vel, -2)
        self.assertEqual(enemy.gravity, .5)
        self.assertEqual(enemy.frame_index, 3)
        self.assertEqual(enemy.image, enemy.frames[3])
        self.assertEqual(enemy.state, c.DEATH_JUMP)

    def test_animation(self):
        # Test that the enemy animation updates its image
        enemy = Goomba()
        enemy.frame_index = 0
        enemy.animation()
        self.assertEqual(enemy.image, enemy.frames[0])
        enemy.frame_index = 1
        enemy.animation()
        self.assertEqual(enemy.image, enemy.frames[1])

    def test_update(self):
        # Test that the enemy updates its behavior based on game info and arguments
        enemy = Enemy()
        game_info = {c.CURRENT_TIME: 0}
        enemy.handle_state = Mock()
        enemy.animation = Mock()
        enemy.update(game_info)
        enemy.handle_state.assert_called_once()
        enemy.animation.assert_called_once()
        self.assertEqual(enemy.current_time, game_info[c.CURRENT_TIME])
        

    # Goomba testing
    def test_goomba_init(self):
        goomba = Goomba()
        self.assertEqual(goomba.direction, c.LEFT)
        self.assertEqual(goomba.state, c.WALK)
        self.assertEqual(goomba.name, "goomba")
        self.assertIsNotNone(goomba.sprite_sheet)
        self.assertIsNotNone(goomba.frames)
        self.assertIsNotNone(goomba.image)
        self.assertIsNotNone(goomba.rect)
        self.assertEqual(goomba.rect.x, 0)
        self.assertEqual(goomba.rect.bottom, c.GROUND_HEIGHT)


    def test_goomba_frames(self): 
        goomba = Goomba()  # calls setup_frames from constructor
        self.assertEqual(len(goomba.frames), 4)

    def test_jump_on(self):
        goomba = Goomba()
        goomba.death_timer = 0
        goomba.current_time = 0
        goomba.jumped_on()
        self.assertEqual(goomba.frame_index, 2)
        goomba.death_timer = 0
        goomba.current_time = 1000
        goomba.jumped_on()
        self.assertFalse(goomba.alive())



    # Koopa testing
    def test_init(self):
        koopa = Koopa(y=100, x=50, direction=c.RIGHT, name='green_koopa')
       
        self.assertEqual(koopa.state, c.WALK)
        self.assertEqual(koopa.rect.bottom, 100)
        self.assertEqual(koopa.rect.x, 50)
        self.assertEqual(koopa.direction, c.RIGHT)
        self.assertEqual(koopa.name, 'green_koopa')
        self.assertEqual(len(koopa.frames), 4)
        self.assertEqual(koopa.frame_index, 0)
        self.assertIsNotNone(koopa.sprite_sheet)
        self.assertIsNotNone(koopa.image)
       
       
     

    def test_setup_frames(self):
        koopa = Koopa(y=100, x=50, direction=c.RIGHT, name='green_koopa') # calls setup frames from constructor
        self.assertEqual(len(koopa.frames), 4)

    def test_jumped_on(self):
        koopa = Koopa(y=100, x=50, direction=c.RIGHT, name='green_koopa')
        koopa.jumped_on()
        self.assertEqual(koopa.x_vel, 0)
        self.assertEqual(koopa.frame_index, 2)
        #self.assertEqual(koopa.rect.bottom, koopa.frames[koopa.frame_index].get_rect().bottom)
        #self.assertEqual(koopa.rect.x, koopa.frames[koopa.frame_index].get_rect().x)

    def test_shell_sliding(self):
        koopa = Koopa(y=100, x=50, direction=c.RIGHT, name='green_koopa')
        koopa.shell_sliding()
        self.assertEqual(koopa.x_vel, 10)
        koopa.direction = c.LEFT
        koopa.shell_sliding()
        self.assertEqual(koopa.x_vel, -10)




    def tearDown(self):
        pg.quit()
