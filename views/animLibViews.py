"""
boAnimation.views - aniLibViews
"""


from pymel.core import *
import viewGui
import boAnimation

LOG = boAnimation.getLog('animLibViews')


class AnimLibMainView(viewGui.View):
    displayName = 'Anim Library'
    def links(self):
        return ['MainView', self.viewName]
    
    def buildBody(self):
        button()


VIEWS = [AnimLibMainView]
