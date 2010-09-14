"""
boAnimation - gui
"""

import logging
import boAnimation
from boAnimation.views import aniLibViews, aniToolsViews, mainViews, utilViews
import boViewGui, boViewGui.gui

LOG = boAnimation.getLog('gui')

WIN_TITLE = 'Animation Tools {0}'.format(boAnimation.__version__)
WIN_NAME = 'boAnimWin'


VIEWS = []
VIEWS.extend(aniLibViews.VIEWS)
VIEWS.extend(aniToolsViews.VIEWS)
VIEWS.extend(mainViews.VIEWS)
VIEWS.extend(utilViews.VIEWS)


def Gui():
    """Instance and create a boViewGui Gui"""
    aniGui = boViewGui.gui.Gui()
    aniGui.title = WIN_TITLE
    aniGui.winName = WIN_NAME
    aniGui.defaultView = 'MainView'
    aniGui.setViews(VIEWS)
    aniGui.create()
    del aniGui
