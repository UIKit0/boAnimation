"""Utils for retrieving information about animation and scene settings
"""

import os
from pymel.core import *

import logging
LOG = logging.getLogger('Ani Utils')
LOG.setLevel(logging.DEBUG)

#Tangent dict is a conversion for using more sensible terms to describe tangent attributes
#the values are converted from values to keys when animation is retrieved, then
#reconverted from the keys to the values when animation is being set
TANGENT_SET_DCT = {
    'inType':'itt',
    'inAngle':'ia',
    'inWeight':'iw',
    'outType':'ott',
    'outAngle':'oa',
    'outWeight':'ow',
    'lockTangents':'l',
    'lockWeights':'wl'
}
TANGENT_GET_DCT = {}
for key, value in TANGENT_SET_DCT.items():
    TANGENT_GET_DCT[value] = key




def getUser():
    return os.environ['USER']

def getStartFrame():
    return playbackOptions(q=True, ast=True)

def getEndFrame():
    return playbackOptions(q=True, aet=True)

def getFps():
    return mel.currentTimeUnitToFPS()

def getLinearUnit():
    return currentUnit(q=True, l=True)

def getDate():
    import time
    from datetime import date
    return str(date.fromtimestamp(time.time()))



def getAnimations(nodes, updateFunc=None):
    """
    Return all animation data for all specified nodes
    The result is a list of animation data dictionaries
    """
    animList = []
    count, num = len(nodes), 0
    for node in nodes:
        anim = getAnimation(node)
        animList.append(anim)
        num += 1
        LOG.debug('getting anim {0}/{1}: {2}'.format(num, count, node))
        if updateFunc is not None:
            updateFunc(count, num)
    return animList

def getAnimation(node):
    """
    Return all animation data for the specified node.
    
    The return value is a complex dictionary. The basic
    structure looks something like this:
    
    result {}
        <node name>
        curves []
            keys []
                values, times, etc {}
                tangents {}
                    types, weights, angles, etc
    """
    
    anim = {}
    anim['name'] = node.name()
    anim['curves'] = []
    
    animCurves = [PyNode(curve) for curve in keyframe(node, q=True, name=True)]
    attrs = [curve.listConnections(d=True, p=True)[0].longName() for curve in animCurves]
    
    numAttrs = len(attrs)
    for i in range(0, numAttrs):
        curve = animCurves[i]
        curveData = {}
        curveData['attr'] = attrs[i]
        curveData['preInfinity'] = str(curve.getPreInfinityType())
        curveData['postInfinity'] = str(curve.getPostInfinityType())
        curveData['keys'] = []
        num = curve.numKeys()
        for j in range(0, num):
            keyData = {}
            keyData['time'] = curve.getTime(j)
            keyData['value'] = curve.getValue(j)
            keyData['breakdown'] = curve.isBreakdown(j)
            keyData['tangent'] = getTangent(curve, j)
            curveData['keys'].append(keyData)
        anim['curves'].append(curveData)
    
    return anim



def setAnimations(animList, updateFunc=None):
    count, num = len(animList), 0
    for anim in animList:
        num += 1
        LOG.debug('setting anim {0}/{1}: {2}'.format(num, count, anim['name']))
        setAnimation(anim)
        if updateFunc is not None:
            updateFunc(count, num)




def setAnimation(anim, create=True):
    """Apply animation to a node"""
    try:
        node = PyNode(anim['name'])
    except:
        if type(anim) is dict and anim.has_key('name'):
            LOG.error('Node does not exist {0}'.format(anim['name']))
        else:
            LOG.error('No animation was found')
        return
    
    for curveData in anim['curves']:
        attr = curveData['attr']
        curve = getCurve(node, attr, create=create)
        
        #LOG.debug('{0}/{1} - {2}'.format(num, count, curve))
        
        if curve is None:
            continue
        for key in curveData['keys']:
            time = key['time']
            value = key['value']
            breakdown = key['breakdown']
            setKey(curve, time, value, breakdown)
        for key in curveData['keys']:
            time = key['time']
            tangent = key['tangent']
            setTangent(curve, time=time, **tangent)



def getCurve(node, attr, create=False):
    curves = keyframe(node, q=True, at=attr, name=True)
    attrNode = getattr(node, attr)
    if curves == []:
        if create:
            if attrNode.isKeyable():
                setKeyframe(getattr(node, attr))
                return PyNode(keyframe(node, q=True, at=attr, name=True)[0])
            else:
                LOG.error('{0} is not keyable'.format(attrNode))
        else:
            LOG.error('No animation curve exists for {0}'.format(attrNode))
            return None
    else:
        return PyNode(curves[0])


def getKeyIndex(curve, time):
    times = keyframe(curve, q=True, tc=True)
    if time in times:
        return times.index(time)
    else:
        return None


def setKey(curve, time, value, breakdown=False, tangent=None):
    """Set a key on a curve to the given values"""
    times = keyframe(curve, q=True, tc=True)
    if time not in times:
        setKeyframe(curve, time=(time,time))
        times = keyframe(curve, q=True, tc=True)
    
    index = times.index(time)
    curve.setValue(index, value)
    curve.setBreakdown(index, breakdown)
    if tangent is not None:
        setTangent(curve, index=index, **tangent)





def getTangent(curve, index, tan_dct=TANGENT_GET_DCT):
    """Return a dict of the tangent properties for the given key of the given curve"""
    tan = {}
    tan['itt'] = keyTangent(curve, index=(index,index), q=True, inTangentType=True)[0]
    tan['ott'] = keyTangent(curve, index=(index,index), q=True, outTangentType=True)[0]
    if tan['itt'] == 'fixed':
        tan['ia'] = keyTangent(curve, index=(index,index), q=True, inAngle=True)[0]
        tan['iw'] = keyTangent(curve, index=(index,index), q=True, inWeight=True)[0]
    if tan['ott'] == 'fixed':
        tan['oa'] = keyTangent(curve, index=(index,index), q=True, outAngle=True)[0]
        tan['ow'] = keyTangent(curve, index=(index,index), q=True, outWeight=True)[0]
    tan['l'] = curve.getTangentsLocked(index)
    tan['wl'] = curve.getWeightsLocked(index)
    #encode tangent dict keys
    ctan = {}
    for key, value in tan.items():
        ctan[tan_dct[key]] = value
    return ctan

def getTanType(tantype):
    if tantype is 'smooth':
        tantype = 'spline'
    if tantype is 'stepNext':
        tantype = 'stepnext'
    return tantype



def setTangent(curve, index=None, time=None, tan_dct=TANGENT_SET_DCT, **kw):
    if kw is {}:
        return
    
    if index is None:
        if time is None:
            LOG.error('Not enough information was provided')
        else:
            index = getKeyIndex(curve, time)
    
    indext = (index, index)
    
    #filter tangent keywords into in, out, and locking keywords
    tankw, lockkw = {}, {}
    for key, value in kw.items():
        if key in tan_dct.keys():
            if 'lock' in key:
                lockkw[tan_dct[key]] = value
            else:
                tankw[tan_dct[key]] = value
    
    if tankw.has_key('itt'):
        tankw['itt'] = getTanType(tankw['itt'])
    if tankw.has_key('ott'):
        tankw['ott'] = getTanType(tankw['ott'])
    
    
    #unlock all, set attributes, then reapply
    #previous state, or apply new lock settings
    keyTangent(curve, index=indext, l=False, wl=False)
    keyTangent(curve, index=indext, **tankw)
    keyTangent(curve, index=indext, **lockkw)
    






