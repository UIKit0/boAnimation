

from exporter import AnimationExporter
from pymel.core import ls

def doIt():
    """Return a basic AnimationExporter
    with example settings"""
    
    author = {'username':'bsayre', 'name':'Bohdon Sayre'}
    settings = {'startFrame':1, 'endFrame':24, 'linearUnits':'cm', 'fps':24}
    info = {'dateCreated':'2010-08-06', 'data':'This is an example file'}
    filename = 'X:/dev/maya/2011-x64/scripts/animationFileWrite.xml'
    nodes = ls(sl=True, r=True)
    data = {'author':author, 'settings':settings, 'info':info, 'filename':filename, 'nodes':nodes}
    
    ae = AnimationExporter(data)
    return ae
