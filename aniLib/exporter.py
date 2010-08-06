



__version__ = '0.6'
__author__ = 'Bohdon Sayre'


import logging
from xml.dom import minidom
from pymel.core import *

logger = logging.getLogger('Ani Export')
logger.setLevel(logging.DEBUG)


class AnimationExporter():
    """
    Class for exporting animation on the specified objects.
    Animation is stored in an XML format that is easily
    parsed by the animation importer.
    
    >>> ae = AnimationExporter(data)
    >>> ae.toprettyxml() -> build and return the exported text as well-formatted xml
    >>> ae.write(filename) -> build and write animation to a file
    """
    
    
    settingAttrs = ['startFrame', 'endFrame', 'linearUnits', 'fps']
    
    def __init__(self, data):
        self.author = data['author']
        self.settings = data['settings']
        self.info = data['info']
        self.nodes = data['nodes']
        self.filename = data['filename']
        self.version = __version__
        self.anidom = None
    
    def buildDom(self):
        logger.debug('Building Animation DOM...')
        
        self.anidom = minidom.Document()
        ani = self.anidom.createElement('animation')
        ani.setAttribute('version', self.version)
        self.anidom.appendChild(ani)
        
        logger.debug('Building Settings...')
        if not self.validateSettings():
            logger.error('Settings were not valid')
            return
        self.buildSettings()
        
        logger.debug('Building Nodes...')
        self.buildNodes()
        
        logger.debug('Animation DOM Built')
    
    def buildSettings(self):
        docElem = self.anidom.documentElement
        author = self.anidom.createElement('author')
        settings = self.anidom.createElement('settings')
        info = self.anidom.createElement('info')
        #set author attributes
        author.setAttribute('username', self.author['username'])
        author.setAttribute('name', self.author['name'])
        #set settings attributes
        settings.setAttribute('startFrame', self.settings['startFrame'])
        settings.setAttribute('endFrame', self.settings['endFrame'])
        #set info attributes
        info.setAttribute('dateCreated', self.info['dateCreated'])
        infoText = self.anidom.createTextNode(self.info['data'])
        info.appendChild(infoText)
        #append child to parent element
        docElem.appendChild(author)
        docElem.appendChild(settings)
        docElem.appendChild(info)
    
    def buildNodes(self):
        docElem = self.anidom.documentElement
        nodesElem = self.anidom.createElement('nodes')
        docElem.appendChild(nodesElem)
        
        anims = getAnimations(self.nodes)
        for anim in anims:
            if anim != None:
                nodeElem = self.anidom.createElement('node')
                nodeElem.setAttribute('name', anim['name'])
                for curve in anim['curves']:
                    nodeCurve = self.anidom.createElement('animCurve')
                    nodeCurve.setAttribute('attr', curve['attr'])
                    nodeCurve.setAttribute('preInfinity', curve['preInfinity'])
                    nodeCurve.setAttribute('postInfinity', curve['postInfinity'])
                    for key in curve['keys']:
                        nodeCurveKey = self.anidom.createElement('key')
                        nodeCurveKey.setAttribute('time', key['time'])
                        nodeCurveKey.setAttribute('value', key['value'])
                        nodeCurveKey.setAttribute('inbetween', key['breakdown'])
                        nodeCurveKeyTan = self.anidom.createElement('tangents')
                        tans = key['tangents']
                        nodeCurveKeyTan.setAttribute('weightLock', tans['weightLock'])
                        nodeCurveKeyTan.setAttribute('lock', tans['lock'])
                        nodeCurveKeyTan.setAttribute('in', tans['in']['type'])
                        nodeCurveKeyTan.setAttribute('out', tans['out']['type'])
                        if tans['in']['type'] == 'fixed':
                            nodeCurveKeyTan.setAttribute('inAngle', tans['in']['angle'])
                            nodeCurveKeyTan.setAttribute('inWeight', tans['in']['weight'])
                        if tans['out']['type'] == 'fixed':
                            nodeCurveKeyTan.setAttribute('outAngle', tans['out']['angle'])
                            nodeCurveKeyTan.setAttribute('outWeight', tans['out']['weight'])
                        nodeCurveKey.appendChild(nodeCurveKeyTan)
                        nodeCurve.appendChild(nodeCurveKey)
                    nodeElem.appendChild(nodeCurve)
                nodesElem.appendChild(nodeElem)
    
    
    def validateSettings(self):
        """Ensure that all necessary settings exist and
        are valid data types"""
        #check for important keys
        if set(self.settings.keys()) != set(self.settingAttrs):
            logger.debug('Settings does not contain the necessary keys')
            return False
        #ensure all values are strings
        for key in self.settings:
            self.settings[key] = str(self.settings[key])
        #all settings validated
        return True
    
    
    
    def toxml(self, build=True):
        """ Return the animation data DOM as xml.
        If build is set to false, the
        xml from the last build will be returned"""
        if build: self.buildDom()
        return self.anidom.toxml()
    
    def toprettyxml(self, indent='    ', build=True):
        """ Return the animation data DOM as well-formatted
         xml. If build is set to false, the
        xml from the last build will be returned"""
        if build: self.buildDom()
        return self.anidom.toprettyxml(indent=indent)
    
    def write(self):
        """Write the animation xml to a file"""      
        self.buildDom()
        logger.debug('Exporting to file %s' % self.filename)
        with open(self.filename, 'w') as f:
            f.write(self.toprettyxml(build=False))
            logger.info('Export successful : %s' % self.filename)





def getAnimations(nodes):
    """
    Return all animation data for all specified nodes
    The result is a list of animation data dictionaries
    """
    anims = []
    for node in nodes:
        anim = getAnimation(node)
        anims.append(anim)
    return anims


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
            keyData['time'] = str(curve.getTime(j))
            keyData['value'] = str(curve.getValue(j))
            keyData['breakdown'] = str(curve.isBreakdown(j))
            keyData['tangents'] = {}
            keyData['tangents']['weightLock'] = str(curve.getWeightsLocked(j))
            keyData['tangents']['lock'] = str(curve.getTangentsLocked(j))
            keyData['tangents']['in'] = {}
            keyData['tangents']['out'] = {}
            keyData['tangents']['in']['type'] = str(curve.getInTangentType(j))
            keyData['tangents']['out']['type'] = str(curve.getOutTangentType(j))
            if keyData['tangents']['in']['type'] == 'fixed':
                keyData['tangents']['in']['angle'] = str(keyTangent(animCurves[i], index=(j, j) , q=True, inAngle=True)[0])
                keyData['tangents']['in']['weight'] = str(keyTangent(animCurves[i], index=(j, j) , q=True, inWeight=True)[0])
            if keyData['tangents']['out']['type'] == 'fixed':
                keyData['tangents']['out']['angle'] = str(keyTangent(animCurves[i], index=(j, j) , q=True, outAngle=True)[0])
                keyData['tangents']['out']['weight'] = str(keyTangent(animCurves[i], index=(j, j) , q=True, outWeight=True)[0])
            curveData['keys'].append(keyData)
        anim['curves'].append(curveData)
    
    #pretty print the data
    #import pprint
    #pp = pprint.PrettyPrinter()
    #pp.pprint(anim)
    
    return anim



