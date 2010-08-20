"""
boAnimation.views - aniLibViews
"""


import boAnimation
from boViewGui import view
from pymel.core import *

LOG = boAnimation.getLog('aniLibViews')


class AniLibMainView(view.View):
    _displayName = 'Ani Library'
    def links(self):
        return ['MainView', self.viewName]
    
    def bodyContent(self):
        button()


VIEWS = [AniLibMainView]
