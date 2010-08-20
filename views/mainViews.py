"""
boAnimation.views - mainViews
"""


import boAnimation
from boViewGui import view
from pymel.core import *

LOG = boAnimation.getLog('mainViews')


class MainView(view.View):
    """The main view of boAnimtion"""
    _displayName = 'Main'
    _bodyMargins = [20, 20]
    def links(self):
        return [self.viewName]
    
    def bodyContent(self):
        with columnLayout(adj=True, rs=10):
            self.viewItem( l='Animation Library', viewName='AniLibMainView')
            self.viewItem( l='Animation Tools', viewName='AniToolsMainView')
            self.viewItem( l='Timing Charts', viewName='TimingChartsMainView', en=False)
            self.viewItem( l='Sketcher', viewName='SketcherMainView', en=False)
            self.viewItem( l='Import/Export', viewName='ImportExportMainView')


VIEWS = [MainView]
