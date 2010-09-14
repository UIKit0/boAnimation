"""
boAnimation.views - utilViews
"""


import boAnimation
from boViewGui import view
from pymel.core import *

LOG = boAnimation.getLog('utilViews')


class ImportExportMainView(view.View):
    _displayName = 'Import / Export'
    _bodyMargins = [14, 14]
    def links(self):
        return ['MainView', self.viewName]
    
    def bodyContent(self):
        template = uiTemplate(force=True)
        template.define(button, h=30, bgc=[0.26, 0.26, 0.26])
        with template:
            with columnLayout(adj=True, rs=6):
                button(l='Export Selected Animation', c=Callback(self.exportSelected))
                button(l='Import Animation', c=Callback(self.importAnimation))
                button(l='Import Animation at current time', c=Callback(self.importAnimation, atCurrentTime=True))
                button(l='Import Animation to Selected', c=Callback(self.importAnimation, onSelected=True))
                separator(st='single', h=1)
                button(l='Copy', c=Callback(self.copyAnimation))
                button(l='Paste', c=Callback(self.pasteAnimation))
    
    def exportSelected(self):
        pass
    
    def importAnimation(self, atCurrentTime=False, onSelected=False):
        pass
    
    def copyAnimation(self):
        pass
    
    def pasteAnimation(self):
        pass


VIEWS = [ImportExportMainView]
