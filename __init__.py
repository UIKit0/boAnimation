"""
    Animation
    
    Copyright (C) 2010 Bohdon Sayre
    All Rights Reserved.
    bo@bohdon.com
    
    Description:
        A suite of animation tools for use in Maya.
    
    Instructions:
        Almost all functionality can be accessed
        through the boAnimation Gui
        >>> import boAnimation
        >>> boAnimation.Gui()
"""

import sys, os, logging

__LOG_LEVEL__ = logging.DEBUG
__RELOAD__ = True

def getLog(name=None):
    if name is None:
        logName = 'Animation'
    else:
        logName = 'Animation: {0}:'.format(name)
    log = logging.getLogger(logName)
    log.setLevel(__LOG_LEVEL__)
    return log

def Gui():
    import boAnimation.gui
    devReload()
    boAnimation.gui.Gui()

def devReload():
    import boAnimation
    reload(boAnimation)
    if __RELOAD__:
        from boAnimation import gui, util, aniLib, views
        from boAnimation.views import aniLibViews, aniToolsViews, mainViews, utilViews
        reload(gui)
        reload(util)
        reload(aniLib)
        reload(views)
        reload(aniLibViews)
        reload(aniToolsViews)
        reload(mainViews)
        reload(utilViews)
        

__VERSION__ = (0, 1, 4)

__version__ = '.'.join([str(n) for n in __VERSION__])
__author__ = 'Bohdon Sayre'
