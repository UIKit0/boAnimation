"""
boAnimation - gui
"""

import logging
import boAnimation
from boAnimation.views import animLibViews, animUtilViews, mainViews
import viewGui

LOG = boAnimation.getLog('gui')

WIN_TITLE = 'Animation Tools {0}'.format(boAnimation.__version__)
WIN_NAME = 'boAnimWin'


VIEWS = []
VIEWS.extend(animLibViews.VIEWS)
VIEWS.extend(animUtilViews.VIEWS)
VIEWS.extend(mainViews.VIEWS)


def Gui(defaultView='MainView'):
    """Instance and create a viewGui Gui"""
    g = viewGui.Gui(WIN_TITLE, WIN_NAME, VIEWS, defaultView)
    g.create()