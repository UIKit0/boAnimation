"""Animation Encoder
"""

__all__ = ['AnimEncoder']

from . import util as aniutil
from pymel.core import *

import logging
LOG = logging.getLogger('Anim Encoder')
LOG.setLevel(logging.DEBUG)

class SettingsError(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)


SECTION_FMT = '[{name}]\n'
SETTING_FMT = '{s} = {sval}\n'
NODE_FMT =    '{node}\n'
CURVE_FMT =   ' {attr}\n'
KEY_FMT =     '  {data}\n'
KEYDATA_FMT = '{time} {value} {breakdown} {tanLock} {weightLock} {inTanType} {outTanType}'
TANDATA_FMT = '{angle} {weight}'
TANTYPE_ENC_DCT = {
    'clamped':'cl',
    'fixed':'fi',
    'flat':'fl',
    'linear':'li',
    'smooth':'sm',
    'spline':'sp',
    'step':'st',
}
TANGENT_DEC_DCT = {}
for key, value in TANTYPE_ENC_DCT.items():
    TANGENT_DEC_DCT[value] = key



class AnimEncoder(object):
    
    __all__ = ['__init__', 'encode', 'iterencode']
    required_settings = []
    auto_settings = ['author', 'date', 'notes', 'startFrame', 'endFrame', 'linearUnits', 'fps']
    all_settings = required_settings + auto_settings
    setting_err_fmt = '`{s}` was not set'
    setting_auto_fmt = '`{s}` has been set to `{sval}`'
    autofnc_fmt = '_auto_{s}'
    
    curve_fmt = ' {attr}\n'
    key_fmt = '  {data}\n'
    keydata_fmt = '{time} {value} {breakdown} {tanLock} {weightLock} {inTanType} {outTanType}'
    tandata_fmt = '{angle} {weight}'
    tan_types = {'clamped':'cl', 'fixed':'fi', 'flat':'fl', 'linear':'li', 'smooth':'sm', 'spline':'sp', 'step':'st'}
    separator = ['\n', '\n']
    
    float_tol = 6
    
    def __init__(self, startFrame=None, endFrame=None, linearUnits=None, fps=None, 
                author=None, date=None, notes='', autoEnabled=True, **kw):
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.linearUnits = linearUnits
        self.fps = fps
        self.author = author
        self.date = date
        self.notes = notes
        self.autoEnabled = autoEnabled
    
    def _validateSettings(self):
        LOG.debug('Validating settings...')
        for s in self.required_settings:
            if getattr(self, s) is None:
                raise SettingsError(self.setting_err_fmt.format(s=s))
        for s in self.auto_settings:
            if getattr(self, s) is None:
                if self.autoEnabled:
                    fnc = getattr(self, self.autofnc_fmt.format(s=s))
                    sval = fnc()
                    setattr(self, s, sval)
                    LOG.debug(self.setting_auto_fmt.format(s=s, sval=sval))
                else:
                    raise SettingsError(self.setting_err_fmt.format(s=s))
        LOG.debug('All settings validated.')
    
    def _validateNotes(self):
        self.notes = self.notes
    
    
    def _auto_startFrame(self):
        return aniutil.getStartFrame()
    
    def _auto_endFrame(self):
        return aniutil.getEndFrame()
    
    def _auto_linearUnits(self):
        return 'ft'
    
    def _auto_fps(self):
        return 25
    
    def _auto_author(self):
        return aniutil.getUser()
    
    def _auto_date(self):
        return '2010-08-28'
    
    
    def _encodeSettings(self, fmt={'section':SECTION_FMT, 'setting':SETTING_FMT}):
        LOG.debug('Encoding settings')
        settings = [fmt['section'].format(name='settings')]
        for s in self.all_settings:
            settings.append(fmt['setting'].format(s=s, sval=getattr(self, s)))
        return settings
    
    def _encodeAnimation(self, anim, fmt={'section':SECTION_FMT, 'node':NODE_FMT, 'curve':CURVE_FMT}):
        LOG.debug('Encoding animation')
        
        animLines = [fmt['section'].format(name='animation')]
        for node in anim:
            kw = { 'node':node['name'] }
            nodeLine = fmt['node'].format(**kw)
            
            animLines.append(nodeLine)
            
            for curv in node['curves']:
                kw = { 'attr':curv['attr'] }
                curveLine = fmt['curve'].format(**kw)
                
                animLines.append(curveLine)
                
                for key in curv['keys']:
                    LOG.debug('Encoding key: {0}'.format(key))
                    data = []
                    kw = {
                        'time': key['time'],
                        'value': key['value'],
                        'breakdown': int(key['breakdown']),
                        'tanLock': int(key['tangent']['lockTangents']),
                        'weightLock': int(key['tangent']['lockWeights']),
                        'inTanType': self.tan_types[key['tangent']['inType']],
                        'outTanType': self.tan_types[key['tangent']['outType']],
                    }
                    keydata = self.keydata_fmt.format(**kw)
                    data.append(keydata)
                    
                    inTanType = key['tangent']['inType']
                    outTanType = key['tangent']['outType']
                    if inTanType == 'fixed':
                        kw = { 'angle':key['tangent']['inAngle'], 'weight':key['tangent']['inWeight'] }
                        inTanData = self.tandata_fmt.format(**kw)
                        data.append(inTanData)
                    if outTanType == 'fixed':
                        kw = { 'angle':key['tangent']['outAngle'], 'weight':key['tangent']['outWeight'] }
                        outTanData = self.tandata_fmt.format(**kw)
                        data.append(outTanData)
                    
                    keyLine = self.key_fmt.format(data=' '.join(data))
                    
                    animLines.append(keyLine)
        
        return animLines
    
    def _iterencode(self, anim):
        self._validateSettings()
        lines = []
        lines.extend(self._encodeSettings())
        lines.extend(self.separator)
        lines.extend(self._encodeAnimation(anim))
        LOG.debug('Encoding finished.')
        return lines
    
    def iterencode(self, anim):
        lines = self._iterencode(anim)
        return lines
    
    def encode(self, anim):
        lines = self._iterencode(anim)
        return ''.join(lines)





