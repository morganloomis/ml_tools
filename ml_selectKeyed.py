# 
#   -= ml_selectKeyed.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 5, 2014-03-01
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_selectKeyed.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_selectKeyed
#     ml_selectKeyed.main()
# From MEL, this looks like:
#     python("import ml_selectKeyed;ml_selectKeyed.main()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Select any node in an animated hierarchy, such as a puppet, and run
# the command to select all the nodes in the hierarchy that are keyed.
# If the selected object has a namespace, it will only return nodes in 
# that namespace. The top node of the hierarchy is excluded.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Select a node in an animated hierarchy, and run the command directly, as
# a hotkey or shelf button.
#      __________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the ml_utilities module, which can be downloaded here:
# 	http://morganloomis.com/wiki/tools.html#ml_utilities
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'animationScripts'
__revision__ = 5

import maya.cmds as mc

try:
    import ml_utilities as utl
    utl.upToDateCheck(9)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
def main():
    '''
    Select any node in a hierarchy, and run the script. 
    It will select all keyed objects within the hierarchy
    except the root node. If the selected object has a namespace,
    only nodes within that namespace will be selected.
    '''
    
    keySel = utl.KeySelection()
    if keySel.keyedInHierarchy():
        mc.select(keySel.nodes, replace=True)
        
        
if __name__ == '__main__': main()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 3: 2012-05-27 : Added revision notes, changed primary function to main() for consistency
#
# Revision 4: 2012-06-10 : Fixing small bug when selecting objects that aren't in a hierarchy.
#
# Revision 5: 2014-03-01 : adding category
