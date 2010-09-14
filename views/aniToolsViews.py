"""
boAnimation.views - aniToolsViews
"""


import boAnimation
from boViewGui import view
from pymel.core import *

LOG = boAnimation.getLog('aniToolsViews')


class AniToolsMainView(view.View):
    _displayName = 'Anim Tools'
    def links(self):
        return ['MainView', self.viewName]
    
    def bodyContent(self):
        button()


VIEWS = [AniToolsMainView]
