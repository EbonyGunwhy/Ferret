"""
This class module contains two custom widgets that subclass QPushButton:
    OpenFileButton - Opens an open file dialog
    SaveFileButton - Opens a save file dialog
"""
from PyQt5.QtWidgets import  QPushButton, QFileDialog, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal  

class FileFilters:
    """
    This class provides users of the custom widgets 
    OpenFileButton & SaveFileButton, with an easy means
    of selecting a file filter.
    """
    anyFiles = 'Any files (*)'
    csvFiles = '*.csv'
    xmlFiles = '*.xml'
    pdfFiles = '*.pdf'
    pythonFiles = '*.py'


class OpenFileButton(QPushButton):
    """
    This class creates a button which when clicked displays
    an open file dialog.  
    
    When a file is selected its file path is passed back 
    to the parent of this widget using the sigFileLoaded signal.

    Input Arguments
    ***************
    xMaxSize - Maximum button size in the x direction
    yMaxSize - Maximum button size in the y direction
    """
    #This widget passes data back to the parent widget
    #using custom signals
    sigFileLoaded = pyqtSignal(str)
    def __init__(self, 
                 buttonLabel='Load File', 
                 showButton=False,
                 toolTip='Opens a file dialog box for selection of a file',
                 shortCut="Ctrl+L",
                 xMaxSize = 300,
                 yMaxSize = 45,
                 defaultDialogCaption='Select a file to open',
                 defaultDirectory='C:\\',
                 filesFilter='Any files (*)'):
        try:
            super().__init__()
            self.setText(buttonLabel)
            self.setMaximumSize(QtCore.QSize(xMaxSize,yMaxSize))
            self.setVisible(showButton)
            self.setToolTip(toolTip)
            self.setShortcut(shortCut)
            self._defaultDirectory = defaultDirectory
            self.clicked.connect(lambda:self.OpenFile(defaultDialogCaption,
                                                            filesFilter))
        except Exception as e:
            print('Error creating OpenFileButton object: ' + str(e)) 


    def setDefaultDirectory(self, defaultDirectory):
        self._defaultDirectory = defaultDirectory


    def OpenFile(self,
            defaultDialogCaption,
            filesFilter):
            """
                Displays an open file dialog box and returns the selected file path
                to the host via the sigFileLoaded signal.
            """
            try:
                #QFileDialog.getOpenFileName returns an existing file selected by the user. 
                #If the user presses Cancel, it returns a null string
                fullFilePath, _ = QFileDialog.getOpenFileName(parent=None, 
                                                     caption=defaultDialogCaption, 
                                                     directory=self._defaultDirectory,
                                                     filter=filesFilter)
                #Check the Cancel button was not clicked
                if len(fullFilePath):
                   self.sigFileLoaded.emit(fullFilePath)
            except IOError:
                print ('IOError in function OpenFileButton OpenFile: cannot open file' + self.dataFileName + ' or read its data')
                #logger.error ('IOError in function OpenFileButton OpenFile: cannot open file' + self.dataFileName + ' or read its data')
            except RuntimeError as re:
                print('Runtime error in function OpenFileButton OpenFile: ' + str(re))
                #logger.error('Runtime error in function OpenFileButton OpenFile: ' + str(re))
            except Exception as e:
                print('Error in function OpenFileButton OpenFile: ' + str(e) + ' at line {} in the CSV file'.format( readCSV.line_num))
                #logger.error('Error in function OpenFileButton OpenFile: ' + str(e) + ' at line {} in the CSV file'.format( readCSV.line_num))
                QMessageBox().warning(self, "CSV data file", "Error reading CSV file at line {} - {}".format(readCSV.line_num, e), QMessageBox.Ok)



class SaveFileButton(QPushButton):
    """
    This class creates button which when clicked displays
    a save file dialog.  
    
    When a file is selected its
    file path is passed back to the parent of this widget
    using the sigFileSaved signal.

    Input Arguments
    ***************
    xMaxSize - Maximum button size in the x direction
    yMaxSize - Maximum button size in the y direction
    """
    #This widget passes data back to the parent widget
    #using custom signals
    sigFileSaved = pyqtSignal(str)
    def __init__(self, 
                 buttonLabel='Save File', 
                 showButton=False,
                 toolTip='Opens a file dialog box for saving of a file',
                 shortCut="Ctrl+S",
                 xMaxSize = 300,
                 yMaxSize = 45,
                 defaultDialogCaption='Save a file',
                 defaultDirectory='C:\\',
                 filesFilter='Any files (*)'):
        try:
            super().__init__()
            self.setText(buttonLabel)
            self.setMaximumSize(QtCore.QSize(xMaxSize,yMaxSize))
            self.setVisible(showButton)
            self.setToolTip(toolTip)
            self.setShortcut(shortCut)
            self._defaultDirectory = defaultDirectory
            self.clicked.connect(lambda:self.SaveFile(defaultDialogCaption,
                                                            filesFilter))
        except Exception as e:
            print('Error creating SaveFileButton object'+ str(e)) 
            #logger.error('Error creating SaveFileButton object: ' + str(e))


    def setDefaultDirectory(self, defaultDirectory):
        self._defaultDirectory = defaultDirectory


    def SaveFile(self,
            defaultDialogCaption,
            filesFilter):
            """
                Displays an open file dialog box and returns the selected file path
                to the host via the sigFileLoaded signal.
            """
            try:
                #QFileDialog.getOpenFileName returns an existing file selected by the user. 
                #If the user presses Cancel, it returns a null string
                fullFilePath, _ = QFileDialog.getSaveFileName(parent=None, 
                                                     caption=defaultDialogCaption, 
                                                     directory=self._defaultDirectory,
                                                     filter=filesFilter)
                #Check the Cancel button was not clicked
                if len(fullFilePath):
                   self.sigFileSaved.emit(fullFilePath)
            except IOError:
                print ('IOError in function SaveFileButton SaveFile: cannot open file' + self.dataFileName + ' or read its data')
                #logger.error ('IOError in function SaveFileButton SaveFile: cannot open file' + self.dataFileName + ' or read its data')
            except RuntimeError as re:
                print('Runtime error in function SaveFileButton SaveFile: ' + str(re))
                #logger.error('Runtime error in function SaveFileButton SaveFile: ' + str(re))
            except Exception as e:
                print('Error in function SaveFileButton SaveFile: ' + str(e) + ' at line {} in the CSV file'.format( readCSV.line_num))
                #logger.error('Error in function SaveFileButton SaveFile: ' + str(e) + ' at line {} in the CSV file'.format( readCSV.line_num))
                QMessageBox().warning(self, "CSV data file", "Error reading CSV file at line {} - {}".format(readCSV.line_num, e), QMessageBox.Ok)
