"""
boAnimation.views - aniToolsViews
"""


import boAnimation
from boAnimation import animUtil
from boViewGui import view
from pymel.core import *

LOG = boAnimation.getLog('animUtilViews')


class AnimUtilMainView(view.View):
    _displayName = 'Anim Util'
    def links(self):
        return ['MainView', self.viewName]
    
    def bodyContent(self):
        pass

class AnimImportExportView(view.View):
    _displayName = 'Anim Import Export'
    _winResize = [360, 300]
    btnTemplate = uiTemplate(force=True)
    btnTemplate.define(button, bgc=[0.2, 0.2, 0.2])
    stngsTemplate = uiTemplate(force=True)
    stngsTemplate.define(frameLayout, bgc=[0.24, 0.24, 0.24])
    sep = 2
    headerHeight = 30
    footerHeight = 30
    aniListWidth = 160
    
    animData = {}
    
    def links(self):
        return ['MainView', self.viewName]
    
    def bodyContent(self):
        with formLayout(nd=100) as form:
            leftForm = self.leftContent()
            rightForm = self.rightContent()
        formLayout(form, e=True,
            af=[
                (leftForm, 'top', 0),
                (leftForm, 'left', 0),
                (leftForm, 'bottom', 0),
                (rightForm, 'top', 0),
                (rightForm, 'right', 0),
                (rightForm, 'bottom', 0),
            ],
            ac=[(rightForm, 'left', self.sep*2, leftForm)]
        )
    
    def leftContent(self):
        with formLayout() as form:
            getAnimForm = self.getAnimContent()
            animListForm = self.animListContent()
            animListControlForm = self.animListControlContent()
            setAnimForm = self.setAnimContent()
        formLayout(form, e=True,
            af=[
                (getAnimForm, 'top', 0),
                (getAnimForm, 'left', 0),
                (getAnimForm, 'right', 0),
                (animListForm, 'top', self.headerHeight),
                (animListForm, 'left', 0),
                (animListForm, 'right', 0),
                (animListControlForm, 'left', 0),
                (animListControlForm, 'right', 0),
                (animListControlForm, 'bottom', self.footerHeight),
                (setAnimForm, 'left', 0),
                (setAnimForm, 'right', 0),
                (setAnimForm, 'bottom', 0),
            ],
            ac=[
                (animListForm, 'bottom', self.sep, animListControlForm),
            ],
        )
        return form
    
    def rightContent(self):
        with formLayout() as form:
            settingsForm = self.stngsContent()
        formLayout(form, e=True,
            af=[
                (settingsForm, 'top', 0),
                (settingsForm, 'left', 0),
                (settingsForm, 'right', 0),
                (settingsForm, 'bottom', 0),
            ]
        )
        return form
    
    def getAnimContent(self):
        with formLayout() as form:
            with self.btnTemplate:
                getAnimBtn = button(l='Copy', c=Callback(self.getAnimBtnHandler))
                importAnimBtn = button(l='Import...', c=Callback(self.importAnimBtnHandler))
        formLayout(form, e=True,
            af=[(getAnimBtn, 'left', 0),
                (importAnimBtn, 'right', 0)],
            ap=[(getAnimBtn, 'right', self.sep*0.5, 40),
                (importAnimBtn, 'left', self.sep*0.5, 40)],
        )
        return form
    
    def setAnimContent(self):
        with formLayout() as form:
            with self.btnTemplate:
                setAnimBtn = button(l='Paste', c=Callback(self.setAnimBtnHandler))
                exportAnimBtn = button(l='Export...', c=Callback(self.exportAnimBtnHandler))
        formLayout(form, e=True,
            af=[(setAnimBtn, 'left', 0),
                (exportAnimBtn, 'right', 0)],
            ap=[(setAnimBtn, 'right', self.sep*0.5, 40),
                (exportAnimBtn, 'left', self.sep*0.5, 40)],
        )
        return form
    
    def animListContent(self):
        with formLayout() as form:
            animList = textScrollList(w=self.aniListWidth, ams=True, sc=Callback(self.animListSelectCommand))
        
        formLayout(form, e=True,
            af=[(animList, 'top', 0),
                (animList, 'left', 0),
                (animList, 'right', 0),
                (animList, 'bottom', 0)]
        )
        self.animList = animList
        return form
    
    def animListControlContent(self):
        with formLayout(nd=100) as form:
            removeBtn = button(l='Remove', bgc=[0.32, 0.26, 0.26])
            renameBtn = button(l='Rename', bgc=[0.28, 0.28, 0.28], c=Callback(self.renameAnimItem))
        formLayout(form, e=True,
            af=[(removeBtn, 'left', 0),
                (renameBtn, 'right', 0)],
            ap=[(removeBtn, 'right', self.sep*0.5, 50),
                (renameBtn, 'left', self.sep*0.5, 50)],
        )
        return form
    
    def stngsContent(self):
        with formLayout(nd=100) as form:
            with self.stngsTemplate:
                with frameLayout(l='Settings', mw=4, mh=4, bs='out') as stngsFrame:
                    self.stngsFrameContent()
                with frameLayout(l='Paste Settings', mw=4, mh=4, bs='out') as changeStngsFrame:
                    self.changeStngsFrameContent()
                with frameLayout(l='Export Settings', mw=4, mh=4, bs='out', cl=False, cll=True) as exportStngsFrame:
                    self.exportStngsContent()
        
        formLayout(form, e=True,
            af=[
                (stngsFrame, 'top', self.headerHeight),
                (stngsFrame, 'left', 0),
                (stngsFrame, 'right', 0),
                (changeStngsFrame, 'left', 0),
                (changeStngsFrame, 'right', 0),
                (exportStngsFrame, 'left', 0),
                (exportStngsFrame, 'right', 0),
                (exportStngsFrame, 'bottom', self.headerHeight),
            ],
            ap=[(stngsFrame, 'bottom', self.sep*0.5, 40),
                (changeStngsFrame, 'top', self.sep*0.5, 40)],
            ac=[(changeStngsFrame, 'bottom', self.sep, exportStngsFrame)],
        )
        self.stngsFrame = stngsFrame
        self.changeStngsFrame = changeStngsFrame
        self.exportStngsFrame = exportStngsFrame
        self.setSettings()
        return form
    
    def stngsFrameContent(self):
        pass
    
    def changeStngsFrameContent(self):
        labelWidth = 100
        rowHeight = 22
        with formLayout(en=False) as mainForm:
            with columnLayout(cal='right', adj=True, rs=2, w=labelWidth) as labelCol:
                template = uiTemplate(force=True)
                template.define(text, h=rowHeight)
                with template:
                    text('Time Offset')
                    text('Sample Sub-Range')
                    text('Convert Time Units')
                    text('Object Association')
                    text('')
            with columnLayout(cal='left', adj=True, rs=2) as controlCol:
                floatField(h=rowHeight, w=60)
                with rowLayout(h=rowHeight, nc=3, cw3=(20, 60, 60)):
                    checkBox(h=rowHeight, l='')
                    floatField(h=rowHeight, w=60)
                    floatField(h=rowHeight, w=60)
                checkBox(h=rowHeight, l='')
                radioButtonGrp(h=rowHeight, nrb=3, la3=('Default', 'Smart', 'Search and Replace'), cw3=(66, 60, 100), sl=1)
                text('Exact naming matches only', en=False)
        formLayout(mainForm, e=True,
            af=[
                (labelCol, 'top', 0),
                (labelCol, 'left', 0),
                (labelCol, 'bottom', 0),
                (controlCol, 'top', 0),
                (controlCol, 'left', labelWidth+self.sep),
                (controlCol, 'right', 0),
                (controlCol, 'bottom', 0),
            ],
        )
        self.changeStngsMainForm = mainForm
    
    def exportStngsContent(self):
        labelWidth = 100
        rowHeight = 22
        with formLayout() as mainForm:
            with columnLayout(cal='right', adj=True, rs=2, w=labelWidth) as labelCol:
                template = uiTemplate(force=True)
                template.define(text, h=rowHeight)
                with template:
                    text('Notes')
            with columnLayout(cal='left', adj=True, rs=2) as controlCol:
                textField(h=rowHeight)
        formLayout(mainForm, e=True,
            af=[
                (labelCol, 'top', 0),
                (labelCol, 'left', 0),
                (labelCol, 'bottom', 0),
                (controlCol, 'top', 0),
                (controlCol, 'left', labelWidth+self.sep),
                (controlCol, 'right', 0),
                (controlCol, 'bottom', 0),
            ],
        )
    
    
    
    
    def getAnimBtnHandler(self):
        selList = selected()
        if len(selList) > 0:
            anim = animUtil.getAnim(selList)
            newName = self.getNewCopyName()
            self.animData[newName] = anim
            self.updateAnimList()
            return anim
        return None
    
    def importAnimBtnHandler(self):
        pass
    
    def setAnimBtnHandler(self):
        selItems = self.animList.getSelectItem()
        if selItems is not None:
            selItem = selItems[0]
            if self.animData.has_key(selItem):
                animUtil.setAnim(self.animData[selItem]['anim'], self.animData[selItem]['settings'])
    
    def exportAnimBtnHandler(self):
        pass
    
    
    def animListSelectCommand(self):
        selItems = self.animList.getSelectItem()
        if selItems is not None:
            selItem = selItems[0]
            data = self.animData[selItem]['settings']
            dataList = [
                'author',
                'notes',
                'startFrame',
                'endFrame',
                'date',
                'fps',
                'linearUnits',
            ]
            self.setSettings(dataList=dataList, **data)
        else:
            self.setSettings()
    
    
    
    def updateAnimList(self):
        self.animList.removeAll()
        items = self.animData.keys()
        items.sort()
        for item in items:
            self.animList.append(item)
    
    def clearStngsFrame(self):
        nch = frameLayout(self.stngsFrame, q=True, nch=True)
        if nch > 0:
            for item in frameLayout(self.stngsFrame, q=True, ca=True):
                try: deleteUI(item)
                except: pass
    
    def setSettings(self, dataList=None, labelWidth=70, rowHeight=16, **kw):
        self.clearStngsFrame()
        if dataList is None:
            keys = kw.keys()
            values = kw.values()
        else:
            keys = dataList
            values = [kw[key] for key in keys]
            
        if kw != {}:
            with self.stngsFrame:
                with formLayout() as form:
                    template = uiTemplate(force=True)
                    template.define(text, h=rowHeight)
                    with template:
                        with columnLayout(cal='right', adj=True, rs=2, w=labelWidth) as labelCol:
                            for i in range(len(keys)):
                                text(keys[i], en=False)
                        with columnLayout(cal='left', adj=True, rs=2) as controlCol:
                            for i in range(len(values)):
                                text(values[i], en=True)
                
                formLayout(form, e=True,
                    af=[
                        (labelCol, 'top', 0),
                        (labelCol, 'left', 0),
                        (labelCol, 'bottom', 0),
                        (controlCol, 'top', 0),
                        (controlCol, 'left', labelWidth+self.sep),
                        (controlCol, 'right', 0),
                        (controlCol, 'bottom', 0),
                    ],
                )
        else:
            with self.stngsFrame:
                text('Copy or Import Animation and select an item...', en=False)
    
    def setChangeStngs(self, enabled=None):
        if enabled is not None:
            self.changeStngsMainForm.setEnable(enabled)
    
    
    def getNewCopyName(self):
        import time
        ltime = time.localtime()
        hr, min, sec = ltime.tm_hour, ltime.tm_min, ltime.tm_sec
        timefmt = '{0:02}:{1:02}:{2:02}'.format(hr, min, sec)
        fmt = 'copy [{0}]'
        return fmt.format(timefmt)
    
    def renameAnimItem(self):
        selItems = self.animList.getSelectItem()
        if selItems is not None:
            selItem = selItems[0]
            if self.animData.has_key(selItem):
                kw = {
                    't':'Rename \'{0}\''.format(selItem),
                    'm':'New Name:',
                    'b':('Rename', 'Cancel'),
                    'cb':'Cancel',
                    'db':'Rename',
                    'ds':'dismiss',
                    'p':'boAnimWin',
                }
                LOG.debug(kw)
                result = promptDialog(**kw)
                LOG.debug('result: {0}'.format(result))
                if result == 'Rename':
                    newName = promptDialog(q=True)
                    if newName != '':
                        LOG.debug('New Name: {0}'.format(newName))
                        self.animData[newName] = self.animData[selItem]
                        del self.animData[selItem]
                        self.updateAnimList()
            
            


VIEWS = [AnimUtilMainView, AnimImportExportView]



