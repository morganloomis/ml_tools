# 
#   -= ml_controlLibrary.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 2, 2016-08-02
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_controlLibrary.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_controlLibrary
#     ml_controlLibrary.ui()
# From MEL, this looks like:
#     python("import ml_controlLibrary;ml_controlLibrary.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This tool is for exporting and then importing nurbs curves
# to be used as animation controls.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI. The first time it is run, it will prompt to create
# a control repository directory if it doesn't find one. This is
# where control curves will be saved, and by default it will be
# in the same directory that the script is in. If you want them saved
# somewhere else, just set the REPOSITORY_PATH variable in this file.
#      ________________
# - -/__ UI Options __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
#  : Right-click for more options
#      __________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the ml_utilities module, which can be downloaded here:
# 	http://morganloomis.com/wiki/tools.html#ml_utilities
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'riggingScripts'
__revision__ = 2


import os, shutil
from functools import partial

import maya.cmds as mc
import maya.mel as mm

try:
    import ml_utilities as utl
    utl.upToDateCheck(20)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
try:
    import ml_parentShape
except ImportError:
    raise ImportError('This module requires ml_parentShape in order to work. Please download from http://morganloomis.com')


REPOSITORY_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ml_controlCurveRepository').replace('\\','/')


def ui():
    '''Launch the UI
    '''
    if not os.path.exists(REPOSITORY_PATH):
        result = mc.confirmDialog( title='Control Repository Not Found', message='Create a repository directory?', 
                                   button=['Create','Cancel'], defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )

        if result != 'Create':
            return None

        os.mkdir(REPOSITORY_PATH)    
    
    win = ControlLibraryUI()
    win.buildMainLayout()
    win.finish()


def controlFilePath(name):
    '''Simply return the expected path for a given control name.
    '''
    assert os.path.exists(REPOSITORY_PATH), "Repository doesn't exist: {}".format(REPOSITORY_PATH)
    return os.path.join(REPOSITORY_PATH, name+'.ctrl').replace('\\','/')


class ControlLibraryUI(utl.MlUi):
    '''Inherited from MlUi
    '''
    
    def __init__(self):
        
        super(ControlLibraryUI, self).__init__('ml_controlLibrary', 
                                               'Control Library', 
                                               width=400, 
                                               height=400, 
                                               info='''Import and Export control curves.
If there's no controls available in the import tab, you'll want to export one first!''')
#Repo: {}'''.format(REPOSITORY_PATH))
        self.buildWindow()
        
    
    def buildMainLayout(self):
        '''Build the main part of the ui
        '''
        
        tabs = mc.tabLayout()
        tab1 = mc.columnLayout(adj=True)
        
        mc.scrollLayout(cr=True)
        self.shelfLayout = mc.shelfLayout()
        
        self.refreshShelfLayout()
        
        mc.setParent(tabs)
        
        tab2 = mc.columnLayout(adj=True)
    
        mc.separator(height=8, style='none')
        mc.text('Select curve(s) to export. Multiple selected curves will be combined.')
        mc.text('Center and fit the curve in the viewport,')
        mc.text('and make sure nothing else is visible for best icon creation.')
        mc.separator(height=16, style='in')
        
        mc.button('Export Selected Curve', command=self.exportControl, annotation='Select a nurbsCurve to export.')
        
        mc.tabLayout( tabs, edit=True, tabLabel=((tab1, 'Import'), 
                                                 (tab2, 'Export')
                                                 ))
        
        if not mc.shelfLayout(self.shelfLayout, query=True, numberOfChildren=True):
            mc.tabLayout( tabs, edit=True, selectTab=tab2)
    
    
    def exportControl(self, *args):
        '''Wrapper to export a control and refresh the ui.
        '''
        
        promptExportControl()
        self.refreshShelfLayout()
        
        
    def refreshShelfLayout(self, *args):
        '''Delete and the shelf buttons and remake them
        '''
        
        shelfButtons = mc.shelfLayout(self.shelfLayout, query=True, childArray=True)
        if shelfButtons:
            for child in shelfButtons:
                mc.deleteUI(child)
        
        mc.setParent(self.shelfLayout)
        
        for each in os.listdir(REPOSITORY_PATH):
            if each.endswith('.ctrl'):
                name = os.path.splitext(each)[0]
                icon = None
                imageFile = os.path.join(REPOSITORY_PATH,name+'.png')
                if os.path.isfile(imageFile):
                    icon = imageFile
                filename = os.path.join(REPOSITORY_PATH,each)
                button = mc.shelfButton(command=partial(importControl, name),
                                        image=icon, 
                                        width=70,
                                        height=70,
                                        imageOverlayLabel=name.replace('_',' ').replace('  ',' '),
                                        annotation=name)
                
                menus = mc.shelfButton(button, query=True, popupMenuArray=True)
                if menus:
                    for menu in menus:
                        mc.deleteUI(menu)
                #mc.popupMenu()
                #mc.menuItem('delete', command=partial(self.deleteShelfButton, name))
    
    
    def deleteShelfButton(self, name, *args):
        '''Delete the shelf button
        '''
        
        #at the moment this crashes my maya. Need to investigate before including.
        path = controlFilePath(name)
        os.remove(path)
        os.remove(path.replace('.ctrl','.png'))
        self.refreshShelfLayout()
    
        
def exportControl(curves, name):
    '''Export a control curve
    '''
    
    if not isinstance(curves, (list, tuple)):
        curves = [curves]
    
    grp = mc.group(em=True, name=name)

    for each in curves:
        ml_parentShape.parentShape(each, grp)
    
    mc.delete(grp, constructionHistory=True)
    
    tempFile = mc.internalVar(userTmpDir=True)
    tempFile+='tempControlExport.ma'

    mc.select(grp)
    mc.file(tempFile, force=True, typ='mayaAscii', exportSelected=True)
    
    with open(tempFile, 'r') as f:
        contents = f.read()
        
    ctrlLines = ['//ML Control Curve: '+name]
    
    record = False
    for line in contents.splitlines():
        if line.startswith('select'):
            break
        if line.strip().startswith('rename'): #skip the uuid commands
            continue
        if line.startswith('createNode transform'):
            record = True
            ctrlLines.append('string $ml_tempCtrlName = `createNode transform -n "'+name+'_#"`;')
        elif line.startswith('createNode nurbsCurve'):
            ctrlLines.append('createNode nurbsCurve -p $ml_tempCtrlName;')
        elif record:
            ctrlLines.append(line)
            
        
    with open(controlFilePath(name), 'w') as f:
        f.write('\n'.join(ctrlLines))
    
    return grp


def promptExportControl(*args):
    '''Export selection, prompt for name, and create icon as well.
    '''
    
    sel = mc.ls(sl=True)

    assert sel, 'Select a control curve(s) to export.'
    
    for each in sel:
        if mc.nodeType(each) == 'nurbsCurve':
            continue
        shapes = mc.listRelatives(each, shapes=True, type='nurbsCurve')
        assert shapes, '{} is not a nurbsCurve'.format(each)
    
    result = mc.promptDialog(
        title='Export Control Curve',
        message='Enter Name:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

    if result != 'OK':
        return
    
    ctrlName = mc.promptDialog(query=True, text=True)
    ctrlName = ''.join(x if x.isalnum() else '_' for x in ctrlName)
    
    if os.path.exists(controlFilePath(ctrlName)):
        result = mc.confirmDialog(title='Control Exists', 
                                  message='A control of this name already exists.', 
                                  button=['Overwrite','Cancel'], 
                                  defaultButton='Cancel', 
                                  cancelButton='Cancel', 
                                  dismissString='Cancel'
                                  )
        if result != 'Overwrite':
            return 
        
    ctrl = exportControl(sel, ctrlName)
    
    strokes = mc.ls(type='stroke')
    
    #create the icon
    mc.ResetTemplateBrush()
    brush = mc.getDefaultBrush()
    mc.setAttr(brush+'.screenspaceWidth', 1)
    mc.setAttr(brush+'.distanceScaling', 0.01)
    mc.setAttr(brush+'.color1', 0.1, 0.65, 1, type='double3')

    mc.select(ctrl)
    mc.AttachBrushToCurves(ctrl)
    image = utl.renderShelfIcon(name=ctrlName, width=64, height=64)

    imagePath = os.path.join(REPOSITORY_PATH, os.path.basename(image))    
    shutil.move(image, imagePath)

    #delete new strokes.
    newStrokes = [x for x in mc.ls(type='stroke') if x not in strokes]
    for each in newStrokes:
        mc.delete(mc.listRelatives(each, parent=True, pa=True))


def importControl(name):
    '''Import a control file based on name
    '''
    
    path = controlFilePath(name)
    
    if not os.path.isfile(path):
        raise IOError('File not found: {}'.format(path))
    
    assPre = mc.ls(assemblies=True)
    
    #sourcing this file creates the control curve.
    mm.eval('source "{}"'.format(path))
    assPost = mc.ls(assemblies=True)
    
    for each in assPre:
        assPost.remove(each)
    
    mc.select(assPost[0])
    
    return assPost[0]


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-07-31 : First publish.
#
# Revision 2: 2016-08-02 : fixing function order for correct header generation.
