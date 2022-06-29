"""This module of classes contains the code for building the GUI of the
    FERRET Model Fitting application. 
    The GUI was built using PyQT5.

How to Use.
-----------
   The FERRET-Model-Fitting application allows the user to analyse 
   data that varies over time by fitting a model to one of the time curves. 

   The FERRET-Model-Fitting application provides the following functionality:
        1. Load a python script that describes the models to be used in the 
            analysis.
        2. Then load a CSV file of  MR Signal/time data.  
            The first column must contain time data in seconds. 
            remaining columns of data must contain MR signal data 
            at the time points in the time column. 
			There must be at least 2 columns of signal data.  
			There is no upper limit on the number of columns of signal data.
			Each time a CSV file is loaded, the screen is reset to its initial state.
        3. Select the variables to be plotted on a line graph.
        4. The user can then select a model they would like to fit one of the curves
            displayed in 3.  
        5. The selected model is used to create a time series
           based on default values for the models input parameters,
           which is also plotted on the above axes.
        6. The default model parameters are displayed on the form 
           and the user may vary them and observe the effect on 
           the curve generated in step 5.
        7. Clicking the 'Reset' button resets the model input parameters to their default values.
        9. Clicking the 'Fit Model' button, fits the model to one of the curves
           and the resulting values of the model input parameters are displayed on 
           the screen together with their 95% confidence limits. The variable, whose curve is
           used to fit the model to, is specified in the definition of the model.
        10. By clicking the 'Save plot data to CSV file' button the data plotted on the screen is saved
            to a CSV file - one column for each plot and a column for time.
            A file dialog box is displayed allowing the user to select a location 
            and enter a file name.
        11. By clicking the 'Save Report in PDF Format', current state of the model fitting session
            is saved in PDF format.  This includes a image of the plot, name of the model, name of the 
            data file and the values of the model input parameters. 
            If curve fitting has been carried out and the values of the model input parameters 
            have not been manually adjusted, then the report 
            will contain the 95% confidence limits of the 
            model input parameter values arrived at by curve fitting.
        12. While this application is running, events & function 
            calls with data where appropriate are logged to a file called Ferret.log, 
            stored at the same location as the source code or executable. 
            This file can be used as a debugging aid. 
            When a new instance of the application is started, 
            FERRET.log from the last session will be deleted and a new log file started.

Application Module Structure.
---------------------------
The code in FERRET.py defines the GUI, built using PyQT5.

The styleSheet.py module contains style instructions using CSS 
notation for each control/widget.

GUI Structure
--------------
The GUI is based on the QWidget class.
The GUI contains a single form.  Controls are arranged in two 
vertical columns on this form using Vertical Layout widgets.
Consequently, a horizontal layout control in placed on this form. 
Within this horizontal layout are placed the 2 vertical layout controls.

The left-hand side vertical layout holds controls for the selection of a model 
to analyse the data and the selection & input of data. The module FerretLoadData.py
contains the functionality for the creation and operation of the load model 
and load data file buttons.

The GUI is built using the definition of the selected model in this module.

At the bottom of the left-handside vertical layout are 3 buttons for the 
export of data from Ferret: Save plot data to a CSV file, Save plot data to
DICOM (currently not implemented) and Create a PDF report of the current analysis.
The code in module FerretExportData.py creates these buttons & implements their functionality. 

The right-hand side vertical layout holds a canvas widget for the 
graphical display of the data using Matplotlib. The module FerretPlotData.py contains
the functionality for the display of the Matplotlib graph as well as the logic
to run models and perform curve fitting.

The appearance of the GUI is controlled by the CSS commands in styleSheet.py

Reading Data into Ferret.
----------------------------------
A Python list of model objects can be passed into Ferret when a Ferret object
is created from the Ferret class.  If a list of model objects is not presented
to the Ferret class during object instantiation, then a Load Model Library is 
displayed on the GUI, which the user can use to browse to a Python script containing
the definition of thier model list.  

Clicking the 'Load Data File' button executes the LoadDataFile function in FerretLoadData.py.
The function LoadDataFile loads the contents of a CSV file
containing time and MR signal data into a dictionary of lists.
The header label of each column of data is taken as a dictionary key and the 
corresponding value is a list of MR signals for that data type
(or times when the key is 'time').    
        
The following validation is applied to the data file:
    -The CSV file must contain at least 3 columns of data separated by commas.
    -The first column in the CSV file must contain time data.
    -The header of the time column must contain the word 'time'.

A list of keys is created and displayed in a drop down list for each model variable.
Model variables are described in the definition of each model.

As the time data is read, it is divided by 60 in order to convert it into minutes.
        """
__author__ = "Steve Shillitoe"
__version__ = "1.0"
__date__ = "Date: 2018/12/12"
import sys
import os
import pathlib
import numpy as np
import logging
from typing import List
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QDoubleSpinBox,\
     QVBoxLayout, QHBoxLayout, QGroupBox, QComboBox, QLabel,  \
     QMessageBox, QFileDialog, QCheckBox, QSpacerItem, \
     QGridLayout, QWidget,  QMainWindow
 
########################################
##              CONSTANTS             ##
########################################
IMAGE_NAME = 'model.png' #Used to save an image of the plot to disc

#Determine the location of this file on the fly
pathToThisFile = pathlib.Path(__file__).parent.absolute()
#The following 5 lines of code are necessary for Ferret to access the user's 
#mathematical models
defaultPathModelLibrary  = os.path.join(pathToThisFile, "Developer\ModelLibrary")
defaultPathModelLibrarySupportModules  = os.path.join(pathToThisFile, "Developer\ModelLibrary\SupportModules")
sys.path.append(defaultPathModelLibrary)
sys.path.append(defaultPathModelLibrarySupportModules)
sys.path.append(os.path.join(pathToThisFile, "Core"))

#Image Files
FERRET_LOGO = os.path.join(pathToThisFile, 'images\FERRET_LOGO.png')

#Create and configure the logger
#First delete the previous log file if there is one
LOG_FILE_NAME = "Ferret.log"
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename=LOG_FILE_NAME, 
                    level=logging.INFO, 
                    format=LOG_FORMAT)
logger = logging.getLogger(__name__)

#CoreModules folder renamed to Core because of name clash
#with folder of the same name in Weasel
#Note relative import from, using .Core
if __name__ == '__main__':
    #run stand alone
    from Core.PDFWriter import PDF
    from Core.ExcelWriter import ExcelWriter
    from Core.FerretLoadData import FerretLoadData
    from Core.FerretExportData import FerretExportData
    from Core.FerretPlotData import FerretPlotData
    from Core.FerretConstants import FerretConstants
else:
    #run from Weasel
    from Ferret.Core.PDFWriter import PDF
    from Ferret.Core.ExcelWriter import ExcelWriter
    from Ferret.Core.FerretLoadData import FerretLoadData
    from Ferret.Core.FerretExportData import FerretExportData
    from Ferret.Core.FerretPlotData import FerretPlotData
    from Ferret.Core.FerretConstants import FerretConstants

#Custom widgets for the display of parameter & constant data
#A shortName property is added to each widget so that it can
#be identified with the parameter or constant it is displaying
class ModelParameterSpinBox(QDoubleSpinBox):
    """
    A spin box for the display of a model parameter called shortName
    """
    def __init__(self, shortName):
        super().__init__()
        self._shortName = shortName
        self.setMaximumWidth(150)

    @property
    def shortName(self):
        return self._shortName


class ModelParameterCheckBox(QCheckBox):
    """
    A check box, when checked, for fixing the value 
    of a model parameter during curve fitting.
    """
    def __init__(self, shortName):
        super().__init__()
        self._shortName = shortName
        self.setStyleSheet("spacing: 0px; padding : 0px; alignment: center;")

    @property
    def shortName(self):
        return self._shortName


class ModelLabel(QLabel):
    """
    A label that displays the text in the input argument shortName
    """
    def __init__(self, shortName):
        super().__init__()
        self._shortName = shortName
        self.setText(shortName)

    @property
    def shortName(self):
        return self._shortName


class ModelParameterConfLimits(QLabel):
    """
    A label for the display of optimum parameter 
    confidence limits after curve fitting.
    """
    def __init__(self, shortName):
        super().__init__()
        self._shortName = shortName

    @property
    def shortName(self):
        return self._shortName


class ModelComboBox(QComboBox):
    """
    A combo box for the display & selection
    of parameter and constant values.
    """
    def __init__(self, shortName, longName=None):
        super().__init__()
        self._shortName = shortName
        if longName:
            self.setToolTip('Select {}'.format(longName))

    @property
    def shortName(self):
        return self._shortName


class Ferret(QWidget):   
    """
    This class defines the FERRET Model Fitting GUI.
    """
    def __init__(self, statusBar=None, dataFileFolder=None, modelList=None):
        """
        Creates the GUI. 
        
        Controls on the GUI are placed on 2 vertical
        layout panals placed on a horizontal layout panal.
        The horizontal layout panal is contained by a QWidget object
        that is returned to the MDI subwindow hosting FERRET, where
        it is displayed.
           
        The left-handside vertical layout panal holds widgets for the 
        input of data & the selection of the model to fit to the data.
        Optimum parameter data and their confidence limits resulting
        from the model fit are also displayed.
           
        The right-handside vertical layout panal holds the graph 
        displaying the time/concentration data and the fitted model.
           
        This method coordinates the calling of methods that set up the 
        widgets on the 2 vertical layout panals.

        The appearance of the widgets is determined by CSS 
        commands in the module styleSheet.py. 

        Input parameters
        ------------------------------------
        statusBar - object reference to the status bar on the MDI
        dataFileFolder - file path of the folder containing signal/time data
        modelList - list of names of models available to Ferret
        """
        try:
            super().__init__()
            self.statusBar = statusBar

            self.constantsString = None
            # Store path to time/concentration data files for use 
            # in batch processing.
            self.dataFileFolder = dataFileFolder

            # Boolean variable indicating that the last 
            # change to the model parameters was caused
            # by curve fitting.
            self.isCurveFittingDone = False

            # Dictionary to store signal data from the data input file
            self.signalData={} 

            # List to store data calculated by the model
            self.listModelPredictedValues = [] 

            #List to store the models available to the user of Ferret
            #Each model is represented by an object of class Model
            self.listModelObjects = modelList

            #Object representing the model selected from the above list
            self.currentModelObject = None

            #store dynamically created parameter widgets in lists
            self.parameterSpinBoxList = []
            self.parameterFixedCheckBoxList = []
            self.parameterIntervalLimitList = []

            #store dynamically created constants widgets in a list
            self.constantsWidgetList = []

            #store dynamically created variable widgets in lists
            self.variableComboList = []
            self.variableLabelList = []

            # Stores optimum parameters from Curve fitting
            self.optimisedParamaterDict = {}
            
            self.setUpMainLayouts()
            
            # Set up the graph to plot signal/time data on
            #  the right-hand side vertical layout
            self.setUpPlotArea()
            
            #Add widgets to the left-hand side vertical layout
            self.setUpLeftVerticalLayout()
            
            logger.info("FERRET GUI created successfully.")
        except Exception as e:
            print('Error creating FERRET object: ' + str(e)) 
            logger.error('Error creating FERRET object: ' + str(e))


    def setUpMainLayouts(self):
        """
        Creates the main layouts that divide the Ferret GUI
        into two columns.
        """
        self.horizontalGridLayout = QGridLayout() #Parent layout
        self.verticalLayoutLeft = QVBoxLayout()
        self.verticalLayoutRight = QVBoxLayout()
        self.horizontalGridLayout.setColumnStretch(0, 2)
        self.horizontalGridLayout.setColumnStretch(1, 2)
        self.horizontalGridLayout.addLayout(self.verticalLayoutLeft, 0, 0)
        self.horizontalGridLayout.addLayout(self.verticalLayoutRight, 0, 1)
        #Add the parent layout to the Ferret widget
        self.setLayout(self.horizontalGridLayout)


    def setListModelPredictedValues(self, listPredictedValues):
        self.listModelPredictedValues = listPredictedValues


    def setSignalData(self, signalData):
        self.signalData = signalData


    def returnFerretLogo(self):
        return FERRET_LOGO


    def setUpLeftVerticalLayout(self):
        """
        Creates widgets and places them on the left-handside vertical layout. 
        """
        try:
            self.setUpLoadDataWidget()
            self.setUpModelGroupBox()
            self.setUpExportGroupBox()
            self.verticalLayoutLeft.addStretch(1)
        except Exception as e:
            print('Error in FERRET.setUpLeftVerticalLayout: ' + str(e)) 
            logger.error('Error in FERRET.setUpLeftVerticalLayout: ' + str(e))


    def setUpLoadDataWidget(self):
        """
        Sets up the Load Data widget at the top of the left-handside vertical layout.
        """
        try:
            self.loadDataWidget = FerretLoadData(self.listModelObjects, self.dataFileFolder)
            self.verticalLayoutLeft.addWidget(self.loadDataWidget)
            self.loadDataWidget.sigClearGUI.connect(self.HideAllControlsOnGUI)
            self.loadDataWidget.sigClearGUI.connect(self.lineGraph.clearGraph)
            self.loadDataWidget.sigReturnList.connect(lambda modelList:
                                                    self.setListModelObjects(modelList))
            self.loadDataWidget.sigReturnList.connect(self.populateModelListCombo)
            self.loadDataWidget.sigReturnStatus.connect(lambda statusText: 
                                                    self.statusBar.showMessage(statusText))
            self.loadDataWidget.sigReturnDataDictionary.connect(lambda signalData: self.setSignalData(signalData))
            self.loadDataWidget.sigUpdateGUI.connect(self.ConfigureGUIAfterLoadingData)
        except Exception as e:
            print('Error in FERRET.setUpLoadDataWidget: ' + str(e)) 
            logger.error('Error in FERRET.setUpLoadDataWidget: ' + str(e))
    

    def setUpModelDropDownList(self):  
        """
        Set up the drop down list of models available in Ferret
        """
        self.modelLabel = QLabel("Model:")
        self.cmbModels = QComboBox()
        self.cmbModels.setToolTip('Select a model to fit to the data')
        #Display first item in list, the string "Please Select"
        self.cmbModels.setCurrentIndex(0) 
        self.modelLabel.hide()
        self.cmbModels.hide()
        #activated signal used, so function only connected 
        #when the user selects a model in the dropdown list
        self.cmbModels.activated.connect(self.deleteVariableWidgets)
        self.cmbModels.activated.connect(self.getSelectedModelObject)
        self.cmbModels.activated.connect(self.setUpModelVariableWidgits)
        self.cmbModels.activated.connect(self.UncheckFixParameterCheckBoxes)
        self.cmbModels.activated.connect(lambda: self.clearOptimisedParamaterList('cmbModels')) 
        self.cmbModels.activated.connect(self.displayFitModelButton)
        self.cmbModels.activated.connect(self.configureGUIForEachModel) 
        self.modelHorizontalLayoutTopRow.addWidget(self.modelLabel)
        self.modelHorizontalLayoutTopRow.addWidget(self.cmbModels)
        self.variablesGridLayout = QGridLayout()
        self.modelHorizontalLayoutTopRow.addLayout(self.variablesGridLayout)
        if self.listModelObjects is not None: 
            self.populateModelListCombo()

    
    def setUpModelVariableWidgits(self):
        """
        Creats a label-combobox pair for each model variable 
        and places them in a grid layout.
        """
        try:
            if self.currentModelObject is not None:
                listDataNames = []
                listDataNames = self.GetListDataNames()
                colNumber = 0
                for obj in self.currentModelObject.variablesList:
                    self.label = ModelLabel(obj.shortName)
                    self.label.show()
                    self.comboBox = ModelComboBox(obj.shortName, obj.longName)
                    self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
                    self.comboBox.addItems(listDataNames)
                    self.comboBox.show()   
                    self.variablesGridLayout.addWidget(self.label, 0, colNumber)
                    self.variablesGridLayout.addWidget( self.comboBox, 0, colNumber+1)
                    self.comboBox.activated.connect(self.lineGraph.plotGraph)
                    self.comboBox.activated.connect(self.displayFitModelButton)
                    self.variableComboList.append(self.comboBox)
                    self.variableLabelList.append(self.label)
                    colNumber+=2
        except Exception as e:
            print('Error in function FERRET setUpModelVariableWidgits: ' + str(e) )
            logger.error('Error in function FERRET setUpModelVariableWidgits: ' + str(e) )


    def getSelectedModelObject(self):
        """
        When the user selects a model in the drop down list of models,
        this function gets the corresponding model object
        """
        self.setCurrentModelObject(self.cmbModels.currentText())
       
    
    def setCurrentModelObject(self, shortModelName):
        """
        This function interates through a list of model objects
        and returns the model object with the shortName, shortModelName 
        """
        self.currentModelObject = None
        for obj in self.listModelObjects:
            if obj.shortName == shortModelName:
                self.currentModelObject = obj
                break


    def setUpResetButton(self): 
        """
        Sets up the Reset button. Clicking this button reset parameter
        and constant fields to their default values. 
        """
        self.btnReset = QPushButton('Reset')
        self.btnReset.setMaximumSize(QtCore.QSize(100,45))
        self.btnReset.setToolTip('Reset parameters to their default values.')
        self.btnReset.hide()
        self.btnReset.clicked.connect(self.resetParameterSpinBoxes)
        self.btnReset.clicked.connect(self.resetConstantValues)
        self.btnReset.clicked.connect(self.OptimumParameterChanged)
        # If parameters are reset to their default values, 
        # replot the concentration and model data
        self.btnReset.clicked.connect(self.lineGraph.plotGraph)
        self.modelHorizontalLayoutReset.addWidget(self.btnReset)


    def setUpFitModelButton(self):  
        """
        Sets up the Fit Model button
        """
        self.btnFitModel = QPushButton('Fit Model')
        self.btnFitModel.setMaximumSize(QtCore.QSize(130,45))
        self.btnFitModel.setToolTip('Fit the selected model to the data')
        self.btnFitModel.hide()
        self.btnFitModel.clicked.connect(self.lineGraph.curveFit)
        self.modelHorizontalLayoutReset.addWidget(self.btnFitModel)


    def setUpParameterGridHeader(self): 
        """
        Widgets displaying parameters are placed in a grid layout.  
        This function creates the first header row in the parameter grid layout.
        """
        self.lblConfInt = QLabel("<u>95% Conf' Interval</u>")
        self.lblFix = QLabel("<u>Fix</u>")
        self.lblConfInt.setAlignment(QtCore.Qt.AlignRight)
        self.lblFix.setAlignment(QtCore.Qt.AlignLeft)
        self.paramGridLayout.addWidget(self.lblFix, 0, 2)
        self.paramGridLayout.addWidget(self.lblConfInt, 0, 3)


    def setUpExportGroupBox(self):
        """
        Creates the Export Data group box and adds it to
        left-hand side vertical layout.
        """
        try:
            self.groupBoxExport = FerretExportData()
            self.groupBoxExport.setExportGroupBoxVisible(False)
            self.verticalLayoutLeft.addWidget(self.groupBoxExport)
            self.groupBoxExport.sigPrepareForDataExport.connect(self.collectDataForExport)
        except Exception as e:
            print('Error in FERRET.setUpExportGroupBox: ' + str(e)) 
            logger.error('Error in FERRET.setUpExportGroupBox: ' + str(e))

    
    def getVariableValueFromComboBox(self, name):
        """
        This function returns the value of a variable called name
        from the corresponding combobox.
        """
        valueVariable = None
        for comboBox in self.variableComboList:
            if comboBox.shortName == name:
                valueVariable = comboBox.currentText()
                return valueVariable


    def setVariableValuesInModelObject(self):
        """
        This function iterates through all the variables associated with 
        the current model and sets their values to those selected in thier
        associated widgets on the GUI.
        """
        for variable in self.currentModelObject.variablesList:
            variable.setValue(self.getVariableValueFromComboBox(variable.shortName))
            

    def getListModelVariableValues(self):
        """
        Returns a list of variable values from their associated comboboxes
        """
        tempList = []
        for variable in self.currentModelObject.variablesList:
            tempList.append(self.getVariableValueFromComboBox(variable.shortName))
        return tempList


    def collectDataForPlotting(self):
        """
        This function ensures all data is available for  
        running the model and plotting the data on a graph.
        """
        try:
            self.setVariableValuesInModelObject()
            self.lineGraph.setCurrentModelObject(self.currentModelObject)
            self.lineGraph.setParameterList(self.buildParameterArray())
            self.lineGraph.setSignalData(self.signalData)
        except Exception as e:
            print("Error in Ferret.collectDataForPlotting: " + str(e))
                        
            
    def collectDataForExport(self):
        """
        This function ensures all data is available for  
        export out of Ferret.
        """
        self.setVariableValuesInModelObject()
        shortModelName = self.cmbModels.currentText()
        longModelName = self.currentModelObject.longName
        self.groupBoxExport.setLongModelName(longModelName)
        self.groupBoxExport.setModelName(shortModelName)
        if self.isCurveFittingDone:
            parameterDict = self.optimisedParamaterDict
        else:
            parameterDict = self.BuildParameterDictionary()
        self.groupBoxExport.setDataFileName(self.loadDataWidget.dataFileName)
        self.groupBoxExport.setParameterDictionary(parameterDict) 
        self.groupBoxExport.setSignalData(self.signalData)
        self.groupBoxExport.setListModelValues(self.listModelPredictedValues)
        self.groupBoxExport.setListModelVariableValues(self.getListModelVariableValues())
        self.lineGraph.savePlotToPDF(IMAGE_NAME)
 

    def setUpConstantsGroupBox(self):
        self.groupBoxConstants = QGroupBox('Model Constants')
        self.groupBoxConstants.hide()
        #Grid layout to manage constants widgets
        self.constantsGridLayout = QGridLayout()
        self.modelHorizontalLayoutMiddleRow.addWidget(self.groupBoxConstants)
        self.groupBoxConstants.setLayout(self.constantsGridLayout)
            

    def setUpParametersGroupBox(self):
        self.groupBoxParameters = QGroupBox('Model Parameters')
        self.groupBoxParameters.hide()
        #Grid layout to manage parameter widgets
        self.paramGridLayout = QGridLayout()
        self.modelHorizontalLayoutMiddleRow.addWidget(self.groupBoxParameters)
        self.groupBoxParameters.setLayout(self.paramGridLayout)
        self.setUpParameterGridHeader()


    def connectLineGraphSignalsToSlots(self):
        self.lineGraph.sigGetPlotData.connect(self.collectDataForPlotting)
        self.lineGraph.sigGetPlotData.connect(self.buildConstantsString)
        self.lineGraph.sigGetCurveFitData.connect(self.curveFitCollectParameterData)
        self.lineGraph.sigGetCurveFitData.connect(self.buildConstantsString)
        self.lineGraph.sigCurveFittingComplete.connect(lambda listResults: 
                                                       self.postCurveFittingProcessing(listResults))
        self.lineGraph.sigReturnOptimumParamDict.connect(lambda optParamDict:
                                                         self.display95ConfidenceLimits(optParamDict))


    def setUpLayoutsInModelGroupBox(self):
        """ Creates the 3 horizontal layouts in the Model group box.

        They are added to a vertical layout, which is
        then added to the Model group box.
       
        One row of widgets is added to each horizontal layout. """

        # modelHorizontalLayoutTopRow contains the combo boxes
        # for selecting the model and its variables
        self.modelHorizontalLayoutTopRow = QHBoxLayout()
        self.modelHorizontalLayoutMiddleRow = QHBoxLayout()
        self.modelHorizontalLayoutReset = QHBoxLayout()
        #The above horizontal layouts are stacked in the following vertical layout
        self.modelVerticalLayout = QVBoxLayout()
        self.modelVerticalLayout.addLayout(self.modelHorizontalLayoutTopRow)
        self.modelVerticalLayout.addLayout(self.modelHorizontalLayoutMiddleRow)
        self.modelVerticalLayout.addLayout(self.modelHorizontalLayoutReset)
        self.groupBoxModel.setLayout(self.modelVerticalLayout)


    def setUpModelGroupBox(self):    
        """Creates a group box to hold widgets associated with the 
        selection of a model and for inputing/displaying that model's
        parameter data."""
        try:
            self.groupBoxModel = QGroupBox('Model Fitting')
            # The group box is hidden until a Model is selected.
            self.groupBoxModel.hide()
            self.verticalLayoutLeft.addWidget(self.groupBoxModel)
 
            self.setUpLayoutsInModelGroupBox()

            self.setUpConstantsGroupBox()

            self.setUpParametersGroupBox()
            
            self.setUpModelDropDownList()

            self.setUpResetButton()

            self.setUpFitModelButton()

            self.connectLineGraphSignalsToSlots()
        except Exception as e:
            print('Error in FERRET.setUpModelGroupBox: ' + str(e)) 
            logger.error('Error in FERRET.setUpModelGroupBox: ' + str(e))


    def postCurveFittingProcessing(self, listResults):
        """
        After curve fitting has been performed, this function
        configures the Ferret GUI.
        """
        self.isCurveFittingDone = True 
        self.ClearOptimumParamaterConfLimitsOnGUI()
        self.SetParameterSpinBoxValues(listResults)
        self.lineGraph.setParameterFixedCheckBoxList(self.parameterFixedCheckBoxList)


    def displayModelList(self):
        """
        Makes the Model label-combobox pair visible
        """
        self.cmbModels.show()
        self.modelLabel.show()


    def setUpPlotArea(self):
        """Adds widgets for the display of the graph onto the 
        right-hand side vertical layout.
        """
        try:
            self.lineGraph = FerretPlotData(yLabel="Signal",
                                       xLabel="Time",
                                       title="Signal-Time Curves")
            self.lineGraph.sigReturnListModelConcentrations.connect(lambda listConcs:
                                                            self.setListModelPredictedValues(listConcs))
            self.verticalLayoutRight.setAlignment(QtCore.Qt.AlignTop)
            self.verticalLayoutRight.addWidget(self.lineGraph)
        except Exception as e:
            print('Error in FERRET.setUpPlotArea: ' + str(e)) 
            logger.error('Error in FERRET.setUpPlotArea: ' + str(e))

    
    def OptimumParameterChanged(self):  
        """Sets boolean self.isCurveFittingDone to false if the 
        plot of the model curve is changed by manually changing the values of 
        model input parameters rather than by running curve fitting.
        
        Also, clears the labels that display the optimum value of each 
        parameter and its confidence inteval."""
        self.isCurveFittingDone=False
        self.clearOptimisedParamaterList('Function-OptimumParameterChanged')


    def ClearOptimumParamaterConfLimitsOnGUI(self):  
        """Clears the contents of the labels on the left 
        handside of the GUI that display parameter value
        confidence limits resulting from curve fitting. """
        try:
            logger.info('Function FERRET.ClearOptimumParamaterConfLimitsOnGUI called.')           
            for confIntLabel in self.parameterIntervalLimitList:
                confIntLabel.clear()  
        except Exception as e:
            print('Error in function FERRET.ClearOptimumParamaterConfLimitsOnGUI: ' + str(e))
            logger.error('Error in function FERRET.ClearOptimumParamaterConfLimitsOnGUI: ' + str(e))
    

    def clearOptimisedParamaterList(self, callingControl: str):
        """Clears results of curve fitting from the GUI 
        and from the global list self.optimisedParamaterDict """
        try:
            logger.info('FERRET.clearOptimisedParamaterList called from ' + callingControl)
            self.optimisedParamaterDict.clear()
            self.ClearOptimumParamaterConfLimitsOnGUI()
        except Exception as e:
            print('Error in function FERRET.clearOptimisedParamaterList: ' + str(e)) 
            logger.error('Error in function FERRET.clearOptimisedParamaterList: ' + str(e))


    def displayFitModelButton(self):
        """Displays the Fit Model, Save CSV and Save PFD Report
       buttons if a model selected.  Otherwise hides them."""
        try:
            modelName = str(self.cmbModels.currentText())
            if self.currentModelObject:
                #A model has been selected
                logger.info("Function FERRET.displayFitModelButton called. Model is " + modelName)
                self.btnFitModel.show() 
                self.groupBoxExport.setExportGroupBoxVisible(True)
        except Exception as e:
            print('Error in function FERRET.displayFitModelButton: ' + str(e))
            logger.error('Error in function FERRET.displayFitModelButton: ' + str(e))

           
    def buildConstantsString(self):
        """
        This function builds a string representation of a
        python dictionary of constant name:value pairs.

        This string forms part of the input to a model function.
        It is passed to the FerretPlotData object for use with
        the model function.
        """
        constantsDict = {}
        for widget in self.constantsWidgetList:
            if isinstance(widget, QComboBox):
                constantsDict[widget.shortName] = widget.currentText()
            elif isinstance(widget, QDoubleSpinBox):
                constantsDict[widget.shortName] = widget.value()
        self.lineGraph.setConstantsString(str(constantsDict))


    def buildParameterArray(self) -> List[float]:
        """Forms a 1D array of model input parameters
            for input to the model function.  
            
            Returns
            -------
                A list of model input parameter values.
            """
        try:
            logger.info('Function FERRET.buildParameterArray called.')
            initialParametersArray = []
            for spinBox in self.parameterSpinBoxList:
                #print("parameter {}, value {}".format(spinBox.shortName, spinBox.value()))
                if spinBox.suffix() == '%':
                    # This is a volume fraction so convert % to a decimal fraction
                    initialParametersArray.append(spinBox.value()/100.0)
                else:
                    initialParametersArray.append(spinBox.value())
            return initialParametersArray
        except Exception as e:
            print('Error in function FERRET.buildParameterArray ' + str(e))
            logger.error('Error in function FERRET.buildParameterArray '  + str(e))


    def SetParameterSpinBoxValues(self, parameterList):
        """Sets the value displayed in the model parameter spinboxes 
           to the calculated optimum model parameter values.
        
        Input Parameters
        ----------------
            parameterList - List of optimum model input parameter values.
        """
        try:
            logger.info('Function FERRET.SetParameterSpinBoxValues called with parameterList = {}'.format(parameterList))
            for objSpinBox in self.parameterSpinBoxList:
                objSpinBox.blockSignals(True)
                value = float(parameterList[objSpinBox.shortName])
                if objSpinBox.suffix() == '%':
                    value = value * 100 
                objSpinBox.setValue(round(value, 4))
                objSpinBox.blockSignals(False)
        except Exception as e:
            print('Error in function FERRET.SetParameterSpinBoxValues ' + str(e))
            logger.error('Error in function FERRET.SetParameterSpinBoxValues '  + str(e))
    

    def display95ConfidenceLimits(self, optParamDict):
        """
        This function displays the lower and upper confidence limits
        of each optimal parameter value for the best curve fit on the
        Ferret GUI.
        """
        self.optimisedParamaterDict = optParamDict
        for objLabel in self.parameterIntervalLimitList:
            tempList = self.optimisedParamaterDict[objLabel.shortName]
            lowerLimit = tempList[1]
            upperLimit = tempList[2]
            confidenceStr = '[{}  {}]'.format(lowerLimit, upperLimit)
            objLabel.setText(confidenceStr)


    def curveFitCollectParameterData(self)-> List[float]:
        """
        Forms a list of model input parameters to 
        be used as input to model for curve fitting.
        
        It is passed to the FerretPlotData object for use with
        the model function.
        """
        try:
            logger.info('function FERRET curveFitCollectParameterData called.')
            parameterDataList = []

            for paramObject in self.currentModelObject.parameterList:
                paramShortName = paramObject.shortName
                units = paramObject.units
                upper = paramObject.upperConstraint
                lower = paramObject.lowerConstraint
                value = self.getParamaterSpinBoxValue(paramShortName)
                if units == "%":
                    value = value/100
                vary = True    
                self.getFixedCheckBoxValue(paramShortName)
                if self.getFixedCheckBoxValue(paramShortName):
                    vary = False
                #each tuple must be (name, value, vary, min, max, expr, brute_step).
                tempTuple = (paramShortName, float(value), vary, lower, upper, None, None)
                parameterDataList.append(tempTuple)

            self.lineGraph.setCurveFitParameterList(parameterDataList)
        except Exception as e:
            print('Error in function FERRET curveFitCollectParameterData ' + str(e))
            logger.error('Error in function FERRET curveFitCollectParameterData '  + str(e))


    def BuildParameterDictionary(self):
        """
        This function builds a dictionary of parameter names:value pairs 
        that is used to create the parameter value table used in the PDF report.  
        """
        try:
            logger.info('BuildParameterDictionary called.')
            parameterDictionary = {}
            for objSpinBox in self.parameterSpinBoxList:
                parameterList = []
                parameterList.append(str(round(objSpinBox.value(), 4)))
                parameterList.append('N/A')
                parameterList.append('N/A')
                units = self.currentModelObject.getParameterUnits(objSpinBox.shortName)
                parameterList.append(units)
                parameterDictionary[objSpinBox.shortName] = parameterList
            return parameterDictionary
        except Exception as e:
            print('Error in function FERRET BuildParameterDictionary: ' + str(e))
            logger.error('Error in function FERRET BuildParameterDictionary: ' + str(e))


    def setListModelObjects(self, modelObjectList):
        """
        This function assigns the list of model objects returned by the
        load data widget to a local class property.
        """
        self.listModelObjects = modelObjectList


    def populateModelListCombo(self):
        """
        Builds a list of model short names and adds this list to the 
        cmbModels combo box for display on the GUI.
        """
        try:
            logger.info('function FERRET populateModelListCombo called.')
            listModelNames = [FerretConstants.PLEASE_SELECT]
            for obj in self.listModelObjects:
                listModelNames.append(obj.shortName)
            self.cmbModels.clear()
            self.cmbModels.blockSignals(True)
            self.cmbModels.addItems(listModelNames)
            self.cmbModels.blockSignals(False)
        except Exception as e:
            print('Error in function FERRET populateModelListCombo: ' + str(e))
            logger.error('Error in function FERRET populateModelListCombo: ' + str(e))


    def HideAllControlsOnGUI(self):
        """
        Hides/clears all the widgets on left-hand side of the application 
        except for the Load & Display Data buttons.  
        It is called before a data file is loaded in case the 
        Cancel button on the dialog is clicked.  
        This prevents the scenario where buttons are displayed 
        but there is no data loaded to process when they are clicked.
        """
        try:
            logger.info('function FERRET HideAllControlsOnGUI called')
            if self.statusBar is not None: 
                self.statusBar.clearMessage()
            self.groupBoxModel.hide()
            self.groupBoxConstants.hide()
            self.groupBoxParameters.hide()
            self.deleteVariableWidgets()
            self.groupBoxExport.setExportGroupBoxVisible(False)
            self.btnFitModel.hide()
            self.btnReset.hide()
        except Exception as e:
            print('Error in function FERRET HideAllControlsOnGUI: ' + str(e))
            logger.error('Error in function FERRET HideAllControlsOnGUI: ' + str(e))
        

    def ConfigureGUIAfterLoadingData(self):   
        """
        After a model library has been selected 
        and a data file is loaded, this function makes
        the model group box and model list visible.
        """
        try:
            self.groupBoxModel.show()
            self.displayModelList()
            logger.info('function FERRET ConfigureGUIAfterLoadingData called.')
        except RuntimeError as re:
            print('runtime error in function FERRET ConfigureGUIAfterLoadingData: ' + str(re) )
            logger.error('runtime error in function FERRET ConfigureGUIAfterLoadingData: ' + str(re) )
        except Exception as e:
            print('Error in function FERRET ConfigureGUIAfterLoadingData: ' + str(e) )
            logger.error('Error in function FERRET ConfigureGUIAfterLoadingData: ' + str(e))
     
            
    def GetListDataNames(self):
        """Builds a list of data types from the headers in the CSV data file. 
        The CSV data file comprises columns of  data for a set of data types.  
        Each column of  data is labeled with a header giving the name of its data type.
        
        Returns
        -------
            A list of data type names for which there is  data.
        """
        try:
            logger.info('function FERRET GetListDataNames called')
            dataTypeList =[]
            dataTypeList.append(FerretConstants.PLEASE_SELECT) #First item at the top of the drop-down list
            for key in self.signalData:
                if key.lower() != 'time' and key.lower() != 'model':  
                    dataTypeList.append(str(key))
            return dataTypeList
        except RuntimeError as re:
            print('runtime error in function FERRET GetListDataNames' + str(re))
            logger.error('runtime error in function FERRET GetListDataNames' + str(re))
        except Exception as e:
            print('Error in function FERRET GetListDataNames: ' + str(e))
            logger.error('Error in function FERRET GetListDataNames: ' + str(e))
    

    def UncheckFixParameterCheckBoxes(self):
        """Uncheckes all the fix parameter checkboxes."""
        logger.info('function FERRET UncheckFixParameterCheckBoxes called')
        for objCheckBox in self.parameterFixedCheckBoxList:
            objCheckBox.blockSignals(True)
            objCheckBox.setChecked(False)
            objCheckBox.blockSignals(False)
  

    def resetConstantValues(self):
        """
        On the GUI, this function resets all the displayed constant values
        to their defaults. 

        The user may adjust the constant values, to see their effect on the 
        output of the model.
        """
        for widget in self.constantsWidgetList:
            defaultValue = self.currentModelObject.getDefaultConstantValue(widget.shortName)
            if isinstance(widget, QComboBox):
                listValues = self.currentModelObject.getConstantListValues(widget.shortName)
                self.comboBox.setCurrentIndex(listValues.index(str(defaultValue)))
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(defaultValue)


    def resetParameterSpinBoxes(self): 
        """
        Sets the parameter spinbox values to their defaults.
        """
        try:
            modelName = str(self.cmbModels.currentText())
            logger.info(
                'function FERRET resetParameterSpinBoxes called when model = ' 
                + modelName)
            for objSpinBox in self.parameterSpinBoxList:
                defaultValue = self.currentModelObject.getDefaultParameterValue(objSpinBox.shortName)
                objSpinBox.blockSignals(True)
                objSpinBox.setValue(defaultValue)
                objSpinBox.blockSignals(False) 
        except Exception as e:
            print('Error in function FERRET resetParameterSpinBoxes: ' + str(e) )
            logger.error('Error in function FERRET resetParameterSpinBoxes: ' + str(e) )
    

    def getParamaterSpinBoxValue(self, shortName):
        """
        This function returns the value displayed in the spinbox
        representing the model parameter with the short name, shortName.
        """
        spinBoxValue = None
        for spinBox in self.parameterSpinBoxList:
            if spinBox.shortName == shortName:
                spinBoxValue = spinBox.value()
                break
        return spinBoxValue
        

    def getFixedCheckBoxValue(self, shortName):
        """
        This function returns the checked state (checked=True) of the
        checkbox that allows a user to fix the value of the parameter 
        whose short name is shortName, during curve fitting.
        """
        isFixed = False
        for checkBox in self.parameterFixedCheckBoxList:
            if checkBox.shortName == shortName:
                if checkBox.isChecked() == True:
                    isFixed = True
                break
        return isFixed


    def setUpConstantsLabelsAndWidgets(self): 
        """
        Sets up the label displaying the constants name 
        and its associated widget (list or spinbox) on the GUI.
        """
        logger.info('function FERRET setUpConstantsLabelsAndWidgets called. ')
        try:
            self.clearConstantsGridLayout()
            if len(self.currentModelObject.constantsList) > 0:
                currentRow = 1
                for obj in self.currentModelObject.constantsList:
                    self.labelConstantName = ModelLabel(obj.shortName)
                    self.labelConstantName.show()
                    self.constantsGridLayout.addWidget(self.labelConstantName,currentRow,0, alignment=Qt.AlignBottom)
                    if len(obj.listValues) == 0:
                        #The constant can take any decimal value
                        self.spinBox = ModelParameterSpinBox(obj.shortName)
                        self.spinBox.setDecimals(obj.precision)
                        self.spinBox.setRange(obj.minValue, obj.maxValue)
                        self.spinBox.setSingleStep(obj.stepSize)
                        self.spinBox.setValue(obj.defaultValue)
                        self.spinBox.valueChanged.connect(self.lineGraph.plotGraph)
                        self.constantsGridLayout.addWidget(self.spinBox,currentRow,1, 
                                                           alignment=Qt.AlignBottom | Qt.AlignLeft)
                        self.constantsWidgetList.append(self.spinBox)
                    else:
                        #The constant has a set of discrete values that 
                        #should be displayed in a drop down list.
                        self.comboBox = ModelComboBox(obj.shortName)
                        self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
                        self.comboBox.addItems(obj.listValues)
                        #Display default value
                        self.comboBox.setCurrentIndex(obj.listValues.index(str(obj.defaultValue)))
                        self.constantsGridLayout.addWidget(self.comboBox,currentRow,1, 
                                                           alignment=Qt.AlignBottom | Qt.AlignLeft)
                        self.comboBox.activated.connect(self.lineGraph.plotGraph)
                        self.constantsWidgetList.append(self.comboBox)
                    currentRow+=1
        except Exception as e:
            print('Error in function FERRET setUpConstantsLabelsAndWidgets: ' + str(e) )
            logger.error('Error in function FERRET setUpConstantsLabelsAndWidgets: ' + str(e) )


    def SetUpParameterLabelsAndSpinBoxes(self): 
        """
        Sets up the label displaying the parameters name 
        and its associated spin box to display its value, 
        fixed checkbox & confidence limits label on the GUI.
        """
        logger.info('function FERRET SetUpParameterLabelsAndSpinBoxes called. ')
        try:
            self.clearParameterGridLayout()
            if len(self.currentModelObject.parameterList) > 0:
                currentRow = 1
                for obj in self.currentModelObject.parameterList:
                    self.labelParamName = ModelLabel(obj.shortName)
                    self.labelParamName.show()
                    self.spinBox = ModelParameterSpinBox(obj.shortName)
                    self.spinBox.setDecimals(obj.precision)
                    self.spinBox.setRange(obj.minValue, obj.maxValue)
                    self.spinBox.setSingleStep(obj.stepSize)
                    self.spinBox.setValue(obj.defaultValue)
                    self.spinBox.valueChanged.connect(self.lineGraph.plotGraph)
                    self.spinBox.valueChanged.connect(self.OptimumParameterChanged)
                    if obj.units == "%":
                        self.spinBox.setSuffix('%')
                    else:
                        self.spinBox.setSuffix('')

                    self.chkBox = ModelParameterCheckBox(obj.shortName)
                    self.chkBox.setChecked(False)

                    self.labelConfLimits = ModelParameterConfLimits(obj.shortName)

                    self.parameterSpinBoxList.append(self.spinBox)
                    self.parameterFixedCheckBoxList.append(self.chkBox)
                    self.parameterIntervalLimitList.append(self.labelConfLimits)
                
                    self.paramGridLayout.addWidget(self.labelParamName,currentRow,0, alignment=Qt.AlignBottom)
                    self.paramGridLayout.addWidget(self.spinBox,currentRow,1, alignment=Qt.AlignBottom )
                    self.paramGridLayout.addWidget(self.chkBox,currentRow,2, alignment=Qt.AlignBottom)
                    self.paramGridLayout.addWidget(self.labelConfLimits,currentRow,3, alignment=Qt.AlignBottom )
                    currentRow+=1
         
        except Exception as e:
            print('Error in function FERRET SetUpParameterLabelsAndSpinBoxes: ' + str(e) )
            logger.error('Error in function FERRET SetUpParameterLabelsAndSpinBoxes: ' + str(e) )


    def deleteVariableWidgets(self):
        """
        This function removes the widgets displaying variables from the GUI
        """
        for combo in self.variableComboList:
            self.variablesGridLayout.removeWidget(combo)
            combo.hide()
        for label in self.variableLabelList:
            self.variablesGridLayout.removeWidget(label)
            label.hide()
        self.variableComboList.clear()
        self.variableLabelList.clear()


    def clearParameterGridLayout(self):
        """
        This function removes the widgets displaying parameter data from the GUI
        and from the lists containing them.
        """
        if self.paramGridLayout is not None:
            while self.paramGridLayout.count():
                child = self.paramGridLayout.takeAt(0)
                if child.widget():
                        child.widget().deleteLater()
            #rewrite header row
            self.setUpParameterGridHeader()
            self.parameterSpinBoxList = []
            self.parameterFixedCheckBoxList = []
            self.parameterIntervalLimitList = []


    def clearConstantsGridLayout(self):
        """
        This function removes the widgets displaying constant data from the GUI
        and from the list containing them.
        """
        try:
            if self.constantsGridLayout is not None:
                while self.constantsGridLayout.count():
                    child = self.constantsGridLayout.takeAt(0)
                    if child.widget():
                            child.widget().deleteLater()
                self.constantsWidgetList = []
        except Exception as e:
            print('Error in function FERRET clearConstantsGridLayout: ' + str(e) )
            logger.error('Error in function FERRET clearConstantsGridLayout: ' + str(e) )


    def configureGUIForEachModel(self):
        """
        When a model is selected or no model is selected, 
        this method configures the appearance of the GUI accordingly.  
        """
        try:
            modelName = str(self.cmbModels.currentText())
            logger.info('function FERRET configureGUIForEachModel called when model = ' + modelName)   
            
            #Configure parameter spinboxes and their labels for each model
            if modelName == FerretConstants.PLEASE_SELECT:
                self.lineGraph.clearPlot()
                self.btnFitModel.hide()
                self.btnReset.hide()
                self.groupBoxExport.setExportGroupBoxVisible(False)
                ##if self.groupBoxConstants is not None:
                self.groupBoxConstants.hide()
                ##if self.groupBoxParameters is not None:
                self.groupBoxParameters.hide()
            else:
                if len(self.currentModelObject.constantsList) > 0:
                    self.groupBoxConstants.show()
                if len(self.currentModelObject.parameterList) > 0:
                    self.groupBoxParameters.show()
                self.setUpConstantsLabelsAndWidgets()
                self.SetUpParameterLabelsAndSpinBoxes()
                self.lineGraph.plotGraph()
                self.btnReset.show()
        except Exception as e:
            print('Error in function FERRET configureGUIForEachModel: ' + str(e) )
            logger.error('Error in function FERRET configureGUIForEachModel: ' + str(e) )


def main():
    from SimpleModels import returnDataFileFolder
    #from MyModels import returnModelList
    import StyleSheet as styleSheet
    os.chdir(os.path.dirname(sys.argv[0]))
    app = QApplication(sys.argv )
    window = QMainWindow()
    ferretWidget = Ferret(statusBar=window.statusBar(),
                         dataFileFolder=returnDataFileFolder()) #, modelList=returnModelList()
    
    window.setCentralWidget(ferretWidget)
    window.setStyleSheet(styleSheet.TRISTAN_GREY)
    window.showMaximized()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
