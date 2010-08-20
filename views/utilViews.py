"""
boAnimation.views - utilViews
"""


import boAnimation
from boViewGui import view
from pymel.core import *

LOG = boAnimation.getLog('utilViews')


class ImportExportMainView(view.View):
    _displayName = 'Import / Export'
    def links(self):
        return ['MainView', self.viewName]
    
    def bodyContent(self):
        button()


VIEWS = [ImportExportMainView]
