"""
boAnimation.views - mainViews
"""


import boAnimation
import viewGui
from pymel.core import *

LOG = boAnimation.getLog('mainViews')


class MainView(viewGui.View):
    """The main view of boAnimtion"""
    displayName = 'Main'
    _bodyMargins = [20, 20]
    _winResize = [200, 260]
    def links(self):
        return [self.viewName]
    
    def buildBody(self):
        with columnLayout(adj=True, rs=10):
            self.viewItem( l='Animation Library', viewName='AnimLibMainView', en=False)
            self.viewItem( l='Animation Import / Export', viewName='AnimImportExportView')
            self.viewItem( l='Timing Charts', viewName='TimingChartsMainView', en=False)
            self.viewItem( l='Sketcher', viewName='SketcherMainView', en=False)
    

VIEWS = [MainView]
