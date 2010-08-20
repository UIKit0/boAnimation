"""
boAnimation - gui
"""

import logging
import boAnimation
from boAnimation.views import aniLibViews, aniToolsViews, mainViews, utilViews
import boViewGui, boViewGui.gui
boViewGui.setLogLevel(logging.DEBUG)

LOG = boAnimation.getLog('gui')

WIN_TITLE = 'Animation Tools {0}'.format(boAnimation.__version__)
WIN_NAME = 'boAnimWin'


_VIEWS_ = []
_VIEWS_.extend(aniLibViews.VIEWS)
_VIEWS_.extend(aniToolsViews.VIEWS)
_VIEWS_.extend(mainViews.VIEWS)
_VIEWS_.extend(utilViews.VIEWS)


def Gui():
    """Instance and create a boViewGui Gui"""
    aniGui = boViewGui.gui.Gui()
    aniGui.title = WIN_TITLE
    aniGui.winName = WIN_NAME
    aniGui.defaultView = 'MainView'
    aniGui.setViews(_VIEWS_)
    aniGui.create()
    del aniGui
