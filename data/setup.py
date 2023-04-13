__author__ = 'justinarmstrong'

"""
This module initializes the display and creates dictionaries of resources.
"""

import os
import sys
import pygame as pg
from SuperMarioLevel1.data.tools import load_all_gfx, load_all_music, load_all_fonts, load_all_sfx
from SuperMarioLevel1.data import constants as c

ORIGINAL_CAPTION = c.ORIGINAL_CAPTION


os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(c.ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

current_path = os.path.abspath(__file__)
# we're in SuperMarioLevel1/data/setup.py & want to get to SuperMarioLevel1/resources
resource_path = os.path.join(os.path.dirname(os.path.dirname(current_path)), 'resources')
FONTS = load_all_fonts(os.path.join(resource_path, 'fonts'))
MUSIC = load_all_music(os.path.join(resource_path, 'music'))
GFX = load_all_gfx(os.path.join(resource_path, 'graphics'))
SFX = load_all_sfx(os.path.join(resource_path, 'sound'))

