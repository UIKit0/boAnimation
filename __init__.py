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

__VERSION__ = (0, 3, 7)

__version__ = '.'.join([str(n) for n in __VERSION__])
__author__ = 'Bohdon Sayre'

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

def Gui(*args, **kargs):
    import boAnimation.gui
    devReload()
    boAnimation.gui.Gui(*args, **kargs)

def devReload(exclude=[]):
    import boAnimation
    reload(boAnimation)
    if __RELOAD__:
        getLog().debug('Reloading Main')
        import boAnimation.gui
        import boAnimation.animUtil
        import boAnimation.views
        reload(boAnimation.gui)
        reload(boAnimation.animUtil)
        reload(boAnimation.views)
        
        if 'aniUtil' not in exclude:
            getLog().debug('Reloading AniUtil')
            import boAnimation.animUtil.util
            import boAnimation.animUtil.encoder
            import boAnimation.animUtil.decoder
            reload(boAnimation.animUtil.util)
            reload(boAnimation.animUtil.encoder)
            reload(boAnimation.animUtil.decoder)
        
        if 'views' not in exclude:
            getLog().debug('Reloading Views')
            import boAnimation.views.animUtilViews
            import boAnimation.views.mainViews
            reload(boAnimation.views.animUtilViews)
            reload(boAnimation.views.mainViews)
        

