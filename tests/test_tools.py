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

    def test_update_quit(self): # note state is a class
        self.control.state = Mock(quit=True)
        with patch.object(self.control.state, "update") as mock_update:
            self.control.update()
            mock_update.assert_called()
            self.assertEqual(self.control.done, True)

    def test_update_done(self): # note state is a class
        self.control.state = Mock(quit=False, done=True)
        with patch.object(self.control, "flip_state") as mock_flip_state:
            with patch.object(self.control.state, "update") as mock_update:
                self.control.update()
                mock_flip_state.assert_called()
                mock_update.assert_called()

    def test_flip_state(self):
        pass
        # self.control.state = Mock(next=c.MAIN_MENU)
        # self.control.state_name = c.GAME_OVER
        # self.control.state_dict[c.MAIN_MENU] = c.LEVEL_STATE
        # self.control.flip_state()
        # with patch.object(self.control.state, "startup") as mock_startup:
        #     # pass
        #     self.control.flip_state()
            # mock_startup.assert_called()
