"""
Simple animation exporter/importer.
"""


__version__ = '0.1.6'
__all__ = [
    'dump', 'dumps', 'load', 'loads',
    'AnimEncoder', 'AnimDecoder'
]
__author__ = 'Bohdon Sayre <bohdon@gmail.com>'


from . import util as aniutil
from .encoder import AnimEncoder
from .decoder import AnimDecoder
from pymel.core import ls

import logging
LOG = logging.getLogger('Ani Export/Import')
LOG.setLevel(logging.DEBUG)

def dump(data, fp, cls=None, dataIsAnim=False, startFrame=None, endFrame=None, linearUnits=None,
        fps=None, author=None, date=None, notes='', autoEnabled=True, **kw):
    """Write animation to a file like object"""
    if cls is None:
        cls = AnimEncoder
    if dataIsAnim:
        anim = data
    else:
        anim = aniutil.getAnimations(data)
    lines = cls(cls=cls, startFrame=startFrame, endFrame=endFrame, linearUnits=linearUnits,
            fps=fps, author=author, date=date, notes=notes, autoEnabled=autoEnabled, **kw).iterencode(anim)
    for line in lines:
        fp.write(line)
    LOG.debug('Finished exporting to {filename}'.format(filename=fp.name))


def dumps(data, cls=None, dataIsAnim=False, startFrame=None, endFrame=None, linearUnits=None,
        fps=None, author=None, date=None, notes='', autoEnabled=True, **kw):
    """Return animation as encoded string"""
    if cls is None:
        cls = AnimEncoder
    if dataIsAnim:
        anim = data
    else:
        anim = aniutil.getAnimations(data)
    return cls(cls=cls, startFrame=startFrame, endFrame=endFrame, linearUnits=linearUnits,
            fps=fps, author=author, date=date, notes=notes, autoEnabled=autoEnabled, **kw).encode(anim)


def load(fp, cls=None):
    return loads(fp.read(), cls=cls)

def loads(s, cls=None):
    if cls is None:
        cls = AnimDecoder
    return cls().decode(s)



