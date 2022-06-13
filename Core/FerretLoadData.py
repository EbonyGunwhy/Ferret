from PyQt5.QtWidgets import QHBoxLayout,  QWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal 
from FileDialogButton import OpenFileButton
from FileDialogButton import FileFilters
from ConstantsMRI import ConstantsMRI
import importlib.util
import os
import pathlib
import sys
#print("FerretLoadData paths=", sys.path)
import csv
import logging
logger = logging.getLogger(__name__)

MIN_NUM_COLUMNS_CSV_FILE = 3

#Determine the path to the model library
pathToThisFile = pathlib.Path(__file__).parent.absolute()
raw_string = r"{}".format(pathToThisFile)
path = pathlib.Path(raw_string)
#path.parent removes Core folder from the file path
defaultPathModelLibray = os.path.join(path.parent, "Developer\ModelLibrary")


class FerretLoadData(QWidget):
    """
    This class creates a custom widget that contains the load model 
    library button and the load data button in a vertical layout.

    The load model library button is only visible if no model object
    list is passed into the instance of the Ferret class, see Ferret.py.
    Otherwise, the load data button is visible.

    Input Arguments
    ***************
    listModelObjects - List of model objects
    dataFileFolder - path to the folder containing Ferret data files
    """
    #This widget passes data and commands back to the parent widget
    #using custom signals
    sigClearGUI = pyqtSignal() #Indicates Ferret GUI needs to be refreshed
    sigUpdateGUI = pyqtSignal()
    sigReturnList = pyqtSignal(list)
    sigReturnStatus =  pyqtSignal(str)
    #DataDictionary is a dictionary holding data from the CSV file
    sigReturnDataDictionary = pyqtSignal(dict)

    def __init__(self, listModelObjects=None, dataFileFolder=None):
        try:
            super().__init__()
            # Dictionary to store signal data from the data input file
            self.signalData={} 
            self.fileFilter = FileFilters()
            self.mainLayout = QHBoxLayout()
            self.setLayout(self.mainLayout)
            self.setUpLoadModelLibraryButton()
            self.setUpLoadDataFileButton(dataFileFolder)
            if listModelObjects is None:
                #The user has not specified a list of models
                #Therefore allow the user to select a model library file
                self.btnLoadModelLibrary.show()
            else:
                self.btnLoadDataFile.show()
        except Exception as e:
            print('Error creating LoadFerretData object: ' + str(e)) 
            logger.error('Error creating LoadFerretData object: ' + str(e))


    def setUpLoadModelLibraryButton(self):
        """
        This function creates the Load Model Library button 
        and adds it to the main widget layout.
        """
        try:
            self.btnLoadModelLibrary = OpenFileButton(buttonLabel='Load Model Library',
                                                      toolTip='Opens file dialog box to select the model library file',
                                                      shortCut='Ctrl+C',
                                                      filesFilter = self.fileFilter.pythonFiles,
                                                      defaultDialogCaption='Select a model library',
                                                      defaultDirectory=defaultPathModelLibray)
            self.btnLoadModelLibrary.sigFileLoaded.connect(lambda filePath: self.LoadModelLibrary(filePath))
            self.btnLoadModelLibrary.hide()
            self.mainLayout.addWidget(self.btnLoadModelLibrary)
        except Exception as e:
            print('Error in function setUpLoadModelLibraryButton: ' + str(e)) 
            logger.error('Error in function setUpLoadModelLibraryButton: ' + str(e))


    def setUpLoadDataFileButton(self, defaultDataFileFolder):
        """
        This function creates the Load Data File button 
        and adds it to the main widget layout.
        """
        try:
            self.btnLoadDataFile = OpenFileButton(buttonLabel='Load Data File',
                                                      showButton=True,
                                                      toolTip='Opens file dialog box to select the data file',
                                                      shortCut='Ctrl+L',
                                                      filesFilter = self.fileFilter.csvFiles,
                                                      defaultDialogCaption='Select a CSV data file',
                                                      defaultDirectory=defaultDataFileFolder)
            self.btnLoadDataFile.sigFileLoaded.connect(lambda filePath: self.LoadDataFile(filePath))
            self.btnLoadDataFile.hide()
            self.mainLayout.addWidget(self.btnLoadDataFile)
        except Exception as e:
            print('Error in function setUpLoadDataFileButton: ' + str(e)) 
            logger.error('Error in function setUpLoadDataFileButton: ' + str(e))


    def NormaliseSignalData(self):
        """
        This function normalises the MR signal data by dividing
        each data point by the average of the initial baseline
        scans done before the perfusion agent is added to the 
        bloodstream.
        """
        try:
            # Get the number of baseline scans is defined 
            # in the xml configuration file
            numBaseLineScans = ConstantsMRI.baseline   

            for key, signalList in self.signalData.items():
                if key == 'model' or key == 'time':
                    # data from a model is already normalised
                    continue
                
                # Calculate mean baseline for the current 
                # list of signals
                signalBaseline = \
                    sum(signalList[0:numBaseLineScans])/numBaseLineScans

                # Divide each value in the list by the baseline
                signalList[:] = [signal/signalBaseline 
                                 for signal in signalList]
                self.signalData[key] = signalList

        except Exception as e:
            print('Error in function LoadFerretData NormaliseSignalData: ' + str(e))
            logger.error('Error in function LoadFerretData NormaliseSignalData: ' + str(e))


    def LoadModelLibrary(self, fullFilePath):
        """
        This function is called when a Model Library python module, with file path fullFilePath, 
        is loaded.

        The Model Library python module is dynamically loaded and it's returnModelList function
        is executed in order to generate a lost of model objects that are returned to the Ferret
        GUI.  Then the Load Data File button is made visible.
        """
        try:
            self.sigClearGUI.emit()
            if os.path.exists(fullFilePath):
                    modelLibraryModule, file_ext = os.path.splitext(os.path.split(fullFilePath)[-1])
                    #update status bar of Ferret
                    self.sigReturnStatus.emit('Model Library file ' +  modelLibraryModule + ' loaded')
                    #dynamically import model library module
                    modelFunctions = importlib.import_module(modelLibraryModule, package='Ferret.Developer.ModelLibrary')
                    returnModelList=getattr(modelFunctions, "returnModelList")
                    #return list of models to the Ferret GUI
                    self.sigReturnList.emit(returnModelList())
                    self.btnLoadDataFile.show()
                    logger.info('Model Library file {} loaded'.format(fullFilePath))
        except ModuleNotFoundError as modErr:
            print ('Module Not Found Error in function LoadFerretData LoadModelLibrary:' + str(modErr))
        except ImportError as impErr:
            print ('Import error in function LoadFerretData LoadModelLibrary:' + str(impErr))
        except IOError as ioe:
            print ('IOError in function LoadFerretData LoadModelLibrary:' + str(ioe))
            logger.error ('IOError in function LoadFerretData LoadModelLibrary: cannot open file' 
                   + str(ioe))
        except RuntimeError as re:
            print('Runtime error in function LoadFerretData LoadModelLibrary: ' + str(re))
            logger.error('Runtime error in function LoadFerretData LoadModelLibrary: ' 
                         + str(re))
        except Exception as e:
            print('Error in function LoadFerretData LoadModelLibrary: ' + str(e))
            logger.error('Error in function LoadFerretData LoadModelLibrary: ' + str(e)) 
         
            
    def LoadDataFile(self, fullFilePath):
        """
        Loads the contents of a CSV file containing time 
        and MR signal data into a dictionary of lists. 
        The key is the name of the organ or the word 'time'  
        and the corresponding value is a list of MR signals
        for that organ (or times when the key is 'time').
        
        The following validation is applied to the data file:
            -The CSV file must contain at least 3 columns of data 
                separated by commas.
            -The first column in the CSV file must contain time data.
            -The header of the time column must contain the word 'time'.
        """
        try:
            # clear the dictionary of previous data
            self.signalData.clear()
        
            #About to load a new data file, so clear existing
            #widgets from the GUI
            self.sigClearGUI.emit()

            if os.path.exists(fullFilePath):
                with open(fullFilePath, newline='') as csvfile:
                    line = csvfile.readline()
                    if line.count(',') < (MIN_NUM_COLUMNS_CSV_FILE - 1):
                        QMessageBox().warning(self, 
                          "CSV data file", 
                          "The CSV file must contain at least 3 columns of data separated by commas.  The first column must contain time data.", 
                          QMessageBox.Ok)
                        raise RuntimeError('The CSV file must contain at least 3 columns of data separated by commas.')
                    
                    # Go back to top of the file
                    csvfile.seek(0)
                    readCSV = csv.reader(csvfile, delimiter=',')
                    # Get column header labels
                    # Returns the headers or `None` if the input is empty
                    headers = next(readCSV, None)  
                    if headers:
                        firstColumnHeader = headers[0].strip().lower()
                        if 'time' not in firstColumnHeader:
                            QMessageBox().warning(self, 
                               "CSV data file", 
                               "The first column must contain time data.", 
                               QMessageBox.Ok)
                            raise RuntimeError('The first column in the CSV file must contain time data.')    

                    logger.info('CSV data file {} loaded'.format(fullFilePath))
                    
                    folderName = os.path.basename(os.path.dirname(fullFilePath))
                    self.dataFileDirectory, self.dataFileName = os.path.split(fullFilePath)
                    self.sigReturnStatus.emit('File ' + self.dataFileName + ' loaded') 
                    
                    # Column headers form the keys in the dictionary 
                    # called self.signalData
                    for header in headers:
                        if 'time' in header.lower():
                            header ='time'
                        self.signalData[header.title().lower()]=[]
                    # Also add a 'model' key to hold a list of concentrations generated by a model
                    self.signalData['model'] = []

                    # Each key in the dictionary is paired 
                    # with a list of corresponding concentrations 
                    # (except the Time key that is paired 
                    # with a list of times)
                    for row in readCSV:
                        colNum=0
                        for key in self.signalData:
                            # Iterate over columns in the selected row
                            if key != 'model':
                                if colNum == 0: 
                                    # time column
                                    self.signalData['time'].append(float(row[colNum])/60.0)
                                else:
                                    self.signalData[key].append(float(row[colNum]))
                                colNum+=1           
                csvfile.close()
                self.NormaliseSignalData()
                self.sigReturnDataDictionary.emit(self.signalData)
                self.sigUpdateGUI.emit()         
        except csv.Error:
            print('CSV Reader error in function LoadFerretData LoadDataFile: file {}, line {}: error={}'.format(self.dataFileName, readCSV.line_num, csv.Error))
            logger.error('CSV Reader error in function LoadFerretData LoadDataFile: file {}, line {}: error ={}'.format(self.dataFileName, readCSV.line_num, csv.Error))
        except IOError:
            print ('IOError in function LoadFerretData LoadDataFile: cannot open file' + self.dataFileName + ' or read its data')
            logger.error ('IOError in function LoadFerretData LoadDataFile: cannot open file' + self.dataFileName + ' or read its data')
        except RuntimeError as re:
            print('Runtime error in function LoadFerretData LoadDataFile: ' + str(re))
            logger.error('Runtime error in function LoadFerretData LoadDataFile: ' + str(re))
        except Exception as e:
            print('Error in function LoadFerretData LoadDataFile: ' + str(e) + ' at line {} in the CSV file'.format( readCSV.line_num))
            logger.error('Error in function LoadFerretData LoadDataFile: ' + str(e) + ' at line {} in the CSV file'.format( readCSV.line_num))
            QMessageBox().warning(self, "CSV data file", "Error reading CSV file at line {} - {}".format(readCSV.line_num, e), QMessageBox.Ok)