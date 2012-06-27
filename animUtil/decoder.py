"""Animation Decoder
"""

__all__ = ['AnimDecoder']

from pymel.core import *

import logging
LOG = logging.getLogger('Anim Decoder')
LOG.setLevel(logging.DEBUG)


SECTION_TAG = re.compile('\[(\w*)\]')
SETTING = re.compile('(\w+)\s?=\s?(.*)')
NODE = re.compile('([^\s]+)$')
CURVE = re.compile('\s{1}([^\s]+) (\d)')
KEYCHECK = re.compile('\s{2}.*')
KEYITEMS = re.compile('(\S+)')

class AnimDecoder(object):
    
    tan_types = {'cl':'clamped', 'fi':'fixed', 'fl':'flat', 'li':'linear', 'sm':'smooth', 'sp':'spline', 'st':'step', 'pl':'plateau', 'a':'auto'}
    
    def __init__(self):
        self._reinit()
    
    def _reinit(self):
        self.curSection = None
        self.settings = {}
        self.anim = []
        self.curNode = None
        self.curNodeId = -1
        self.curCurve = None
        self.curCurveId = -1
    
    def _lineDecode(self, line, secpat=SECTION_TAG):
        m = secpat.match(line)
        if m:
            self.curSection = m.groups()[0]
            LOG.debug('section: {0}'.format(self.curSection))
            return
        
        mthname = '_lineDecode_{0}'.format(self.curSection)
        if hasattr(self, mthname):
            mth = getattr(self, mthname)
            mth(line)
    
    def _lineDecode_settings(self, line, setpat=SETTING):
        m = setpat.match(line)
        if m:
            key, val = m.groups()
            self.settings[key] = val
            LOG.debug(' setting: {0} = {1}'.format(key, val))
    
    def _lineDecode_animation(self, line, nodpat=NODE, crvpat=CURVE, keychpat=KEYCHECK, keyitpat=KEYITEMS):
        m = nodpat.match(line)
        if m:
            node = m.groups()[0]
            self.curNodeId += 1
            self.anim.append({})
            self.anim[self.curNodeId]['name'] = node
            self.anim[self.curNodeId]['curves'] = []
            self.curCurveId = -1
            LOG.debug('decoding node {0}: {1}'.format(self.curNodeId, node))
            return
        
        m = crvpat.match(line)
        if m:
            curve = m.groups()[0]
            try:
                weighted = m.groups()[1]
            except:
                weighted = True
            data = {
                'attr':curve,
                'weighted':bool(int(weighted)),
                'preInfinity':'constant',
                'postInfinity':'constant',
                'keys':[]
            }
            self.curCurveId += 1
            self.anim[self.curNodeId]['curves'].append({})
            self.anim[self.curNodeId]['curves'][self.curCurveId] = data
            #LOG.debug('decoding curve: {0}'.format(curve))
            return
        
        m = keychpat.match(line)
        if m:
            vals = keyitpat.findall(line)
            inTanType = self.tan_types[vals[5]]
            outTanType = self.tan_types[vals[6]]
            key = {
                'time':float(vals[0]),
                'value':float(vals[1]),
                'breakdown':bool(int(vals[2])),
                'tangent':{
                    'lockTangents':bool(int(vals[3])),
                    'lockWeights':bool(int(vals[4])),
                    'inType':inTanType,
                    'outType':outTanType,
                }
            }
            outTanIndex = 7
            if inTanType == 'fixed':
                key['tangent']['inAngle'] = float(vals[7]) 
                key['tangent']['inWeight'] = float(vals[8])
                outTanIndex += 2
            if outTanType == 'fixed':
                key['tangent']['outAngle'] = float(vals[outTanIndex]) 
                key['tangent']['outWeight'] = float(vals[outTanIndex+1])
            
            self.anim[self.curNodeId]['curves'][self.curCurveId]['keys'].append(key)
            #LOG.debug('decoding key: {0}'.format(vals))
            return
        
    
    def decode(self, s):
        self._reinit()
        lines = s.split('\n')
        for line in lines:
            self._lineDecode(line)
        
        return {'anim':self.anim, 'settings':self.settings}




