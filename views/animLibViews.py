"""
boAnimation.views - aniLibViews
"""


from pymel.core import *
import boViewGui
import boAnimation

LOG = boAnimation.getLog('animLibViews')


class AnimLibMainView(boViewGui.View):
    displayName = 'Anim Library'
    def links(self):
        return ['MainView', self.viewName]
    
    def buildBody(self):
        button()


VIEWS = [AnimLibMainView]
