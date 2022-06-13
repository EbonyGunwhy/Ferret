import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# These 2 lines are required if you're importing an external
# python package that doesn't have "pip install" and that's located
# in the same folder as the current menu script.

#The following can be read as:
#from Folder.File import Class as alias
from Ferret.Ferret import Ferret as ferret

from Ferret.Developer.ModelLibrary.MyModels import returnModelList
from Ferret.Developer.ModelLibrary.MyModels import returnDataFileFolder
def isEnabled(weasel):
    return True

def main(weasel):
    #Get the list of mathematical models used in this instance of Ferret
    listModels = returnModelList()
    dataFileFolder = returnDataFileFolder()
    ferretWidget = ferret(weasel.statusBar, dataFileFolder)#,listModels
    icon = ferretWidget.returnFerretLogo()
    title = "Ferret"
    weasel.launchExternalApp(ferretWidget, title, icon)
    