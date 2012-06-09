"""
boAnimation.views - aniToolsViews
"""


from pymel.core import *
import copy
import sys
import boViewGui
import boAnimation
import animUtil

LOG = boAnimation.getLog('animUtilViews')


class AnimUtilMainView(boViewGui.View):
    displayName = 'Anim Util'
    def links(self):
        return ['MainView', self.viewName]
    
    def buildBody(self):
        pass

class AnimImportExportView(boViewGui.View):
    displayName = 'Anim Import Export'
    _winResize = [360, 300]
    usePasteSettings = True
    btnTemplate = uiTemplate(force=True)
    btnTemplate.define(button, bgc=[0.2, 0.2, 0.2])
    stngsTemplate = uiTemplate(force=True)
    stngsTemplate.define(frameLayout, bgc=[0.24, 0.24, 0.24])
    sep = 2
    headerHeight = 30
    footerHeight = 30
    aniListWidth = 160
    progBarHeight = 12
    
    importIter = 1
    
    animData = {}
    
    def links(self):
        return ['MainView', self.viewName]
    
    def buildBody(self):
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
            popupMenu(mm=True, b=3, p=animList)
            menuItem(l='Print Animation', c=Callback(self.animListPrintCommand))
        
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
            removeBtn = button(l='Remove', bgc=[0.32, 0.26, 0.26], c=Callback(self.removeAnimItems))
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
                with frameLayout(l='Paste Settings', mw=4, mh=4, bs='out', cl=False, cll=True) as changeStngsFrame:
                    self.changeStngsFrameContent()
                with frameLayout(l='Export Settings', mw=4, mh=4, bs='out', cl=True, cll=True) as exportStngsFrame:
                    self.exportStngsContent()
            progBar = progressBar(h=self.progBarHeight)
        
        formLayout(form, e=True,
            af=[
                (stngsFrame, 'top', self.headerHeight),
                (stngsFrame, 'left', 0),
                (stngsFrame, 'right', 0),
                (changeStngsFrame, 'left', 0),
                (changeStngsFrame, 'right', 0),
                (exportStngsFrame, 'left', 0),
                (exportStngsFrame, 'right', 0),
                (exportStngsFrame, 'bottom', self.footerHeight),
                (progBar, 'left', 0),
                (progBar, 'right', 0),
                (progBar, 'bottom', 6),
            ],
            ap=[
                (stngsFrame, 'bottom', self.sep*0.5, 46),
                (changeStngsFrame, 'top', self.sep*0.5, 46)
            ],
            ac=[
                (changeStngsFrame, 'bottom', self.sep, exportStngsFrame),
            ],
        )
        self.stngsFrame = stngsFrame
        self.changeStngsFrame = changeStngsFrame
        self.exportStngsFrame = exportStngsFrame
        self.progBar = progBar
        self.setProg(visible=False)
        self.setSettings()
        return form
    
    def stngsFrameContent(self):
        pass
    
    def changeStngsFrameContent(self):
        labelWidth = 100
        rowHeight = 22
        with formLayout() as mainForm:
            stngsTemplate = uiTemplate(force=True)
            stngsTemplate.define(columnLayout, rs=2, adj=True)
            stngsTemplate.define(button, h=rowHeight)
            stngsTemplate.define(text, h=rowHeight)
            stngsTemplate.define(textField, h=rowHeight)
            stngsTemplate.define(floatField, h=rowHeight)
            with stngsTemplate:
                with columnLayout(cal='right', w=labelWidth) as labelCol:
                    text(l='Time Offset', en=False)
                    text(l='Sample Sub-Range', en=False)
                    text(l='Convert Time Units', en=False)
                    text(l='Object Association')
                    text(l='')
                with columnLayout(cal='left') as controlCol:
                    floatField(w=60, en=False)
                    with rowLayout(nc=3, cw3=(20, 60, 60), en=False):
                        checkBox(l='')
                        floatField(w=60)
                        floatField(w=60)
                    checkBox(h=rowHeight, l='', en=False)
                    objAssocRadio = radioButtonGrp(h=rowHeight, nrb=3, en2=False, la3=('Default', 'Smart', 'Search and Replace'), cw3=(66, 60, 100), sl=1, cc=Callback(self.objAssocRadioChangeCommand))
                    objAssocText = text(l='', en=False)
                    self.objAssocContent()
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
        self.objAssocRadio = objAssocRadio
        self.objAssocText = objAssocText
        self.objAssocRadioChangeCommand()
    
    def objAssocContent(self):
        with columnLayout() as col1:
            pass
        with columnLayout() as col2:
            button(l='Preview')
        with columnLayout() as col3:
            with formLayout(nd=100) as form3:
                searchField = textField()
                replaceText = text(l=' -> ')
                replaceField = textField()
            formLayout(form3, e=True,
                af=[
                    (searchField, 'left', 0),
                    (replaceField, 'right', 0),
                ],
                ap=[ (replaceText, 'left', -10, 50) ],
                ac=[
                    (searchField, 'right', self.sep, replaceText),
                    (replaceField, 'left', self.sep, replaceText),
                ]
            )
            srchRepPreviewBtn = button(l='Preview', w=60, bgc=[0.28, 0.28, 0.28], c=Callback(self.srchRepPreviewBtnHandler))
        self.objAssocLayouts = [col1, col2, col3]
        self.searchField = searchField
        self.replaceField = replaceField
    
    def exportStngsContent(self):
        labelWidth = 100
        rowHeight = 22
        with formLayout() as mainForm:
            with columnLayout(cal='right', adj=True, rs=2, w=labelWidth) as labelCol:
                template = uiTemplate(force=True)
                template.define(text, h=rowHeight)
                with template:
                    text(l='Notes')
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
            self.setProg(visible=True)
            anim = animUtil.getAnim(selList, self.updateProg)
            self.setProg(visible=False)
            newName = self.getNewAnimName()
            self.animData[newName] = anim
            self.updateAnimList()
            LOG.debug(self.animData)
            return anim
        return None
    
    def importAnimBtnHandler(self):
        proj = workspace.getPath()
        if os.path.exists(os.path.join(proj, 'animExports')):
            path = os.path.join(proj, 'animExports')
        else:
            path = proj
        f = fileDialog2(dir=path, fm=1)
        if f is None:
            return
        if type(f) is list:
            f = f[0]
        
        animData = None
        with open(f, 'rb') as fp:
            animData = animUtil.load(fp)
        
        name = os.path.splitext(os.path.basename(f))[0]
        
        #prompt if overwriting
        if self.animData.has_key(name):
            if not self.overwriteAnimItemWarning(name):
                return
        
        if animData is not None:
            self.animData[name] = animData
            self.importIter += 1
            self.updateAnimList()
        
        self.animList.setSelectItem(name)
    
    def setAnimBtnHandler(self):
        animData = self.getSelectedAnimData()
        if animData is None: return
        
        if self.usePasteSettings:
            LOG.debug('Applying Paste Settings')
            pasteAnimData = self.applyAnimDataPasteSettings(animData)
            LOG.debug('Paste Settings Applied')
        else:
            pasteAnimData = animData
        
        self.setProg(visible=True)
        animUtil.setAnim(pasteAnimData['anim'], pasteAnimData['settings'], self.updateProg)
        self.setProg(visible=False)
        LOG.debug(self.animData)
    
    def exportAnimBtnHandler(self):
        animData = self.getSelectedAnimData()
        if animData is None:
            return
        
        proj = workspace.getPath()
        if os.path.exists(os.path.join(proj, 'animExports')):
            path = os.path.join(proj, 'animExports')
        else:
            path = proj
        f = fileDialog2(dir=path, fm=0)
        if f is None:
            return
        if type(f) is list:
            f = f[0]
        
        base, ext = os.path.splitext(f)
        f = '{0}.ani'.format(base)
        
        with open(f, 'wb') as fp:
            animUtil.dump(animData['anim'], fp, dataIsAnim=True, **animData['settings'])
    
    
    def animListSelectCommand(self):
        animData = self.getSelectedAnimData()
        if animData is not None:
            nodeCount = len(animData['anim'])
            dataList = [
                'author',
                'notes',
                'startFrame',
                'endFrame',
                'date',
                'fps',
                'linearUnits',
                'nodes',
            ]
            self.setSettings(dataList=dataList, nodes=nodeCount, **animData['settings'])
        else:
            self.setSettings()
    
    def animListPrintCommand(self):
        import pprint
        selItem = self.getSelectedAnimItem()
        animData = self.getSelectedAnimData()
        if animData is not None:
            sys.__stdout__.write('Anim Data for {0}:\n{1}'.format(selItem, pprint.pformat(animData)))
    
    
    def updateAnimList(self):
        self.animList.removeAll()
        items = self.animData.keys()
        items.sort()
        for item in items:
            self.animList.append(item)
    
    def updateProg(self, count, num):
        """Update the progress bar based on a max count and iterator"""
        self.setProg(maxValue=count, progress=num)
    
    def setProg(self, progress=None, maxValue=None, visible=None):
        if maxValue is not None:
            self.progBar.setMaxValue(maxValue)
        if progress is not None:
            self.progBar.setProgress(progress)
        if visible is not None:
            self.progBar.setVisible(visible)
    
    def objAssocRadioChangeCommand(self):
        stateStrs = [
            'Exact naming matches only',
            'Currently not implemented (will use default)',
            'Search and replace within each node\'s name',
        ]
        state = self.objAssocRadio.getSelect() - 1
        self.objAssocText.setLabel(stateStrs[state])
        for i in range(3):
            if i is state:
                self.objAssocLayouts[i].setVisible(True)
            else:
                self.objAssocLayouts[i].setVisible(False)
    
    def srchRepPreviewBtnHandler(self):
        srchStr, repStr = self.searchField.getText(), self.replaceField.getText()
        animData = self.getSelectedAnimData()
        if animData is None: return
        srchRepDct = self.getSrchRepDct(animData, srchStr, repStr)
        
        longestVal = 0
        for key in srchRepDct.keys():
            if len(key) > longestVal:
                longestVal = len(key)
        
        for key, value in srchRepDct.items():
            print '{0:<{width}} -> {1}'.format(key, value, width=longestVal)
    
    def clearStngsFrame(self):
        nch = frameLayout(self.stngsFrame, q=True, nch=True)
        if nch > 0:
            for item in frameLayout(self.stngsFrame, q=True, ca=True):
                try: deleteUI(item)
                except: pass
    
    def setSettings(self, dataList=None, labelWidth=70, rowHeight=16, **kw):
        self.clearStngsFrame()
        keys, values = [], []
        if dataList is None:
            keys = kw.keys()
            values = kw.values()
        else:
            for key in dataList:
                if kw.has_key(key):
                    keys.append(key)
                    values.append(kw[key])
            for key in kw.keys():
                if not key in keys:
                    keys.append(key)
                    values.append(kw[key])
            
        if kw != {}:
            with self.stngsFrame:
                with formLayout() as form:
                    template = uiTemplate(force=True)
                    template.define(text, h=rowHeight)
                    with template:
                        with columnLayout(cal='right', adj=True, rs=2, w=labelWidth) as labelCol:
                            for i in range(len(keys)):
                                text(l=keys[i], en=False)
                        with columnLayout(cal='left', adj=True, rs=2) as controlCol:
                            for i in range(len(values)):
                                text(l=values[i], en=True)
                
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
                text(l='Copy or Import Animation and select an item...', en=False)
    
    def setChangeStngs(self, enabled=None):
        if enabled is not None:
            self.changeStngsMainForm.setEnable(enabled)
    
    
    def getNewAnimName(self):
        import time
        ltime = time.localtime()
        hr, min, sec = ltime.tm_hour, ltime.tm_min, ltime.tm_sec
        timefmt = '{0:02}:{1:02}:{2:02}'.format(hr, min, sec)
        fmt = 'Anim Copy [{0}]'
        return fmt.format(timefmt)
    
    def getSelectedAnimItem(self):
        result = None
        if hasattr(self, 'animList'):
            selItems = self.animList.getSelectItem()
            if selItems is not None and len(selItems) > 0:
                result = selItems[0]
        return result
    
    def getSelectedAnimData(self):
        selItem = self.getSelectedAnimItem()
        if selItem is not None:
            return copy.deepcopy(self.animData[selItem])
        else:
            return None
    
    def getSrchRepDct(self, animData, srchStr, repStr):
        result = {}
        if animData is not None:
            for node in animData['anim']:
                result[node['name']] = node['name'].replace(srchStr, repStr)
        return result
    
    def renameAnimItem(self):
        selItem = self.getSelectedAnimItem()
        if selItem is None:
            return
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
    
    def removeAnimItems(self):
        selItems = self.animList.getSelectItem()
        if selItems is not None:
            if self.removeAnimItemWarning():
                for item in selItems:
                    if self.animData.has_key(item):
                        del self.animData[item]
                self.updateAnimList()
     
    def removeAnimItemWarning(self):
        kargs = {
            't':'Removing Anim Item(s)',
            'm':'''Animation clips that have not been\nexported will be gone forever!''',
            'icn':'warning',
            'b':['Remove', 'Cancel'],
            'cb':'Cancel',
            'ma':'center',
            'p':'boAnimWin',
        }
        result = confirmDialog(**kargs)
        if result == 'Remove':
            return True
        else:
            return False
    
    def overwriteAnimItemWarning(self, name):
        kargs = {
            't':'Overwrite Anim Item?',
            'm':'''An anim clip already exists with the name\n`{0}`\ndo you want to overwrite it?'''.format(name),
            'icn':'warning',
            'b':['Overwrite', 'Cancel'],
            'cb':'Cancel',
            'ma':'center',
            'p':'boAnimWin',
        }
        result = confirmDialog(**kargs)
        if result == 'Overwrite':
            return True
        else:
            return False
    
    def applyAnimDataPasteSettings(self, animData):
        """Modify values/settings within animData based on paste settings.
        This method assumes that the animData is a deep copy of the source data"""
        useSrchRep = (self.objAssocRadio.getSelect() - 1 == 2)
        if useSrchRep:
            LOG.debug('Applying search and replace...')
            srchStr, repStr = self.searchField.getText(), self.replaceField.getText()
            srchRepDct = self.getSrchRepDct(animData, srchStr, repStr)
            for i in range( len(animData['anim']) ):
                animData['anim'][i]['name'] = srchRepDct[ animData['anim'][i]['name'] ]
        return animData





VIEWS = [AnimUtilMainView, AnimImportExportView]



