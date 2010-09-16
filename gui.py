"""
boAnimation - gui
"""

import logging
import boAnimation
from boAnimation.views import animLibViews, animUtilViews, mainViews
import boViewGui.gui

LOG = boAnimation.getLog('gui')

WIN_TITLE = 'Animation Tools {0}'.format(boAnimation.__version__)
WIN_NAME = 'boAnimWin'


VIEWS = []
VIEWS.extend(animLibViews.VIEWS)
VIEWS.extend(animUtilViews.VIEWS)
VIEWS.extend(mainViews.VIEWS)


def Gui(view = 'MainView', views=VIEWS, winTitle=WIN_TITLE, winName=WIN_NAME):
    """Instance and create a boViewGui Gui"""
    animGui = boViewGui.gui.Gui()
    animGui.title = winTitle
    animGui.winName = winName
    animGui.defaultView = view
    animGui.setViews(views)
    animGui.create()
    del animGui
