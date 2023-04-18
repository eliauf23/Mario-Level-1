import pygame as pg
from unittest.mock import MagicMock, patch, Mock, ANY
from SuperMarioLevel1.data.tools import Control
from SuperMarioLevel1.data.tools import _State
import SuperMarioLevel1.data.constants as c
from unittest import TestCase


class testTools(TestCase):

    def setUp(self):
        pg.init()
        pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.caption = Mock()
        self.control = Control(self.caption)
        o = Mock()
        self.state = _State()

    def tearDown(self) -> None:
        pg.quit()

    def testControlInit(self):
        self.assertEqual(self.control.screen, pg.display.get_surface())
        self.assertEqual(self.control.done, False)
        # self.assertEqual(self.control.clock, pg.time.Clock())
        assert isinstance(self.control.clock, pg.time.Clock)
        self.assertEqual(self.control.caption, self.caption)
        self.assertEqual(self.control.fps, 60)
        self.assertEqual(self.control.show_fps, False)
        self.assertEqual(self.control.current_time, 0.0)
        self.assertEqual(self.control.keys, pg.key.get_pressed())
        self.assertEqual(self.control.state_dict, {})
        self.assertEqual(self.control.state_name, None)
        self.assertEqual(self.control.state, None)

    def test_setup_states(self):
        state_dict = {c.MAIN_MENU: 1}
        start_state = c.MAIN_MENU
        self.control.setup_states(state_dict, start_state)
        self.assertEqual(self.control.state_dict, state_dict)
        self.assertEqual(self.control.state, state_dict[c.MAIN_MENU])

    def test_update_quit(self):
        self.control.state = Mock(quit=True)
        with patch.object(self.control.state, "update") as mock_update:
            self.control.update()
            mock_update.assert_called()
            self.assertEqual(self.control.done, True)

    def test_update_done(self):
        self.control.state = Mock(quit=False, done=True)
        with patch.object(self.control, "flip_state") as mock_flip_state:
            with patch.object(self.control.state, "update") as mock_update:
                self.control.update()
                mock_flip_state.assert_called()
                mock_update.assert_called()

    def test_flip_state(self):
        self.control.state = _State()
        self.control.state.next = c.GAME_OVER
        self.control.state_dict[c.GAME_OVER] = _State()
        with patch.object(_State, "startup") as mock_startup:
            with patch.object(_State, "cleanup") as mock_cleanup:
                self.control.flip_state()
                mock_startup.assert_called()
                mock_cleanup.assert_called()

    def test_event_loop_quit(self):
        self.control.state = _State()
        return_quit = MagicMock(return_value=[pg.event.Event(pg.QUIT)])
        with patch.object(pg.event, "get", new=return_quit):
            with patch.object(_State, "get_event") as mock_get_event:
                self.control.event_loop()
                mock_get_event.assert_called()

    def test_event_loop_keydown(self):
        self.control.state = _State()
        return_keydown = MagicMock(return_value=[pg.event.Event(pg.KEYDOWN, {'key': pg.K_SPACE})])
        with patch.object(self.control, "toggle_show_fps") as mock_toggle_show_fps:
            with patch.object(pg.event, "get", new=return_keydown):
                with patch.object(_State, "get_event") as mock_get_event:
                    self.control.event_loop()
                    mock_get_event.assert_called()
                    mock_toggle_show_fps.assert_called()
                    self.assertEqual(self.control.keys, pg.key.get_pressed())

    def test_event_loop_keyup(self):
        self.control.state = _State()
        return_keyup = MagicMock(return_value=[pg.event.Event(pg.KEYUP, {'key': pg.K_SPACE})])
        with patch.object(pg.event, "get", new=return_keyup):
            with patch.object(_State, "get_event") as mock_get_event:
                self.control.event_loop()
                mock_get_event.assert_called()
                self.assertEqual(self.control.keys, pg.key.get_pressed())

    def test_toggle_show_fps(self):
        self.control.show_fps = True
        with patch.object(pg.display, "set_caption") as mock_set_caption:
            self.control.toggle_show_fps(pg.K_F5)
            self.assertFalse(self.control.show_fps)
            mock_set_caption.assert_called()





