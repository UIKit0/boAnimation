"""
boAnimation - gui
"""

import logging
import boAnimation
from boAnimation.views import animLibViews, animUtilViews, mainViews
import boViewGui

LOG = boAnimation.getLog('gui')

WIN_TITLE = 'Animation Tools {0}'.format(boAnimation.__version__)
WIN_NAME = 'boAnimWin'


VIEWS = []
VIEWS.extend(animLibViews.VIEWS)
VIEWS.extend(animUtilViews.VIEWS)
VIEWS.extend(mainViews.VIEWS)


def Gui(defaultView='MainView'):
    """Instance and create a boViewGui Gui"""
    g = boViewGui.Gui(WIN_TITLE, WIN_NAME, VIEWS, defaultView)
    g.create()