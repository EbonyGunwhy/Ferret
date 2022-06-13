"""
This module contains functions that: 
1. Plot MR signal/time curves on a graph.
2. Calculate and plot the signal/time curve predicted by a mathematical model.
3. Fit the curve predicted by a mathematical model to the experimental data.
4. Calculate the 95% confidence limits associated with the curve fitting.
"""
__author__ = "Steve Shillitoe"
__version__ = "1.0"
__date__ = "Date: 2022/04/26"
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QCursor
import numpy as np
import logging
from lmfit import Parameters, Model
from scipy.stats.distributions import  t
from LineGraph import LineGraph
from SupportModules.GraphSupport import LineColours
from FerretConstants import FerretConstants

#Create and configure the logger
#First delete the previous log file if there is one
LOG_FILE_NAME = "Activity_Log_File.log"
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename=LOG_FILE_NAME, 
                    level=logging.INFO, 
                    format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class FerretPlotData(LineGraph):
    """
    This class inherits from the LineGraph class to provide signal/time 
    curve plotting functionality.

    Additionality it provides functionality for calculating and plotting
    a signal/time curve according to a mathematical model. 

    If plot width = 4,  plot height = 6 and dots per inch is 75 then
        the plot would be 300 and 450 pixels in size.

        Input arguments.
        ****************
        plotWidth - width of the plot in inches 
        plotHeight - height of the plot in inches 
        dotsPerInch - number of pixels per inch 
        xLabel - string containing the X axis label  
        yLabel - string containing the Y axis label  
        title  - string containing the title of the graph displayed above the graph.
        tickLabelSize - size of the axis ticks.
        xyAxisLabelSize - size of the X & Y axis labels.
        titleSize - size of the title.
        backgroundColour - optional parameter for selecting the plot background colour.
                            default value is 'w' for white
    """
    sigGetPlotData =  QtCore.Signal()
    sigGetCurveFitData =  QtCore.Signal()
    sigReturnListModelConcentrations = QtCore.Signal(np.ndarray)
    sigCurveFittingComplete = QtCore.Signal(dict)
    sigReturnOptimumParamDict = QtCore.Signal(dict)

    def __init__(self, plotWidth=4, plotHeight=7, 
                 dotsPerInch=300, xLabel='time', 
                 yLabel='signal', title='Signal/Time Curves',
                 tickLabelSize=2,
                 xyAxisLabelSize=5,
                 titleSize=6,
                 backgroundColour='w'):
        super().__init__(plotWidth, plotHeight, 
                 dotsPerInch, xLabel, 
                 yLabel, title,
                 tickLabelSize,
                 xyAxisLabelSize,
                 titleSize,
                 backgroundColour)
        #dictionary of lists, where name=signal type, value= array of corresponding MR signals
        self._signalData = {} 
        self._currentModelObject = None
        #list of model parameter values
        self._parameterList = []
        #list of optimum parameter values for best fit of model curve to a data curve
        self._curveFitParameterList = []
        #list of checkbox widgets that indicate 
        #if a parameter should be fixed during curve fitting
        self._parameterFixedCheckBoxList = []
        #string of constants used by the model
        self._constantsString = None


    def setConstantsString(self, strConstants):
        self._constantsString = strConstants


    def setParameterFixedCheckBoxList(self, checkBoxList):
        self._parameterFixedCheckBoxList = checkBoxList


    def setCurveFitParameterList(self, paramList):
        self._curveFitParameterList = paramList


    def setSignalData(self, signalData):
        self._signalData = signalData


    def setCurrentModelObject(self, currentModelObject):
        self._currentModelObject = currentModelObject


    def setParameterList(self, paramList):
        self._parameterList = paramList


    def plotGraph(self):  
        """
        This function plots the normalised signal against time curves 
        for each variable in the model objects variables list.
        It also plots the normalised signal/time curve predicted by the 
        selected model.
        """
        try:
            logger.info('function FerretPlotData.plotGraph called')
            self.clearPlot()
            self.sigGetPlotData.emit()
            self.arrayTimes = np.array(self._signalData['time'], dtype='float')
            for variable in self._currentModelObject.variablesList:
                self.plotSignal(variable.value, variable.plotLineColour)
            self.plotModel()
        except Exception as e:
                print('Error in function FerretPlotData plotGraph : ' + str(e))
                logger.error('Error in function FerretPlotData plotGraph : ' + str(e) )


    def calculateAndPlotModelCurve(self, modelFunction, 
                       arrayTimes, 
                       arrayModelInputSignals, 
                       parameterArray):
        """
        Using the function, modelFunction, and its inputs:
         arrayModelInputSignals
         parameterArray
        this function calculates a MR signal/time curve 
        and plots it on the matplotlib plot.

        Inputs
        ------
        modelFunction - function object containing mathematical model 
        arrayTimes - array of time points over which the
                MR signal data is recorded.
        arrayModelInputSignals - array of AIF MR signal data over
                the time period stored in arrayTimes.
        """
        try:
            logger.info('calculateAndPlotModelCurve called')
            timeInputConcs2DArray = np.column_stack((arrayTimes, arrayModelInputSignals))
                    
            listModelConcentrations = modelFunction(timeInputConcs2DArray, *parameterArray, self._constantsString)
            if listModelConcentrations is not None:
                self.plotData(arrayTimes, listModelConcentrations, 
                                        lineStyle=LineColours.greenDashed, 
                                        labelText= 'model')
                self.sigReturnListModelConcentrations.emit(listModelConcentrations)
        except Exception as e:
                print('Error in function FerretPlotData.calculateAndPlotModelCurve ' + str(e) )
                logger.error('Error in function FerretPlotData calculateAndPlotModelCurve ' + str(e) )
    
    
    def plotSignal(self, signalType, lineStyle):
        """
        This function plots the signal/time curve for the variable, signalType
        """
        try:
            if signalType != FerretConstants.PLEASE_SELECT and signalType is not None:
                arraySignals = np.array(self._signalData[signalType], dtype='float')
                self.plotData(xData=self.arrayTimes, 
                                        yData= arraySignals, 
                                        lineStyle=lineStyle, 
                                        labelText=signalType)
        except Exception as e:
            print("Error in FerretPlotData.plotSignal: " + str(e))

                                
    def plotModel(self): 
        """
        This function plots the signal/time curve predicted by the model.

        First it gets the appropriate array of signal/time values for the
        input variable to the model.  Then it calls self.calculateAndPlotModelCurve. 
        """
        try:
            arrayModelInputSignals = []  
            if self._currentModelObject:
                modelInputValue = self._currentModelObject.getValueOfInputVariableToModel()
                if modelInputValue:
                    arrayModelInputSignals = np.array(self._signalData[modelInputValue], dtype='float')
                    self.calculateAndPlotModelCurve(self._currentModelObject.modelFunction, 
                                                                self.arrayTimes, 
                                                                arrayModelInputSignals,  
                                                                self._parameterList)  
        except Exception as e:
            print("Error in FerretPlotData.plotModel: " + str(e))


    def CurveFit(self): 
        """
        This function fits the signal/time curve calculated by 
        the model to a signal/time curve of experimental data.

        The best fit is obtained by adjusting the model's 
        input parameters. These optimum model 
        input parameters are displayed on the GUI 
        and  the line of best fit plotted on the graph on the GUI.
        
        Additionally, the 95% confidence limits of the optimal parameter values  
        are determined.
        """
        try:
            # Get the name of the model to be fitted to the ROI curve
            modelName = self._currentModelObject.shortName
            # Form inputs to the curve fitting function
            self.sigGetCurveFitData.emit()
            modelParams = Parameters()
            modelParams.add_many(*self._curveFitParameterList) 
            #Uncomment the statement below to check parameters 
            #loaded ok into the Parameter object
            #print(modelParams.pretty_print())
            
            # Get arrays of data corresponding to the above 3 regions 
            # and the time over which the measurements were made.
            curveToFitTo = self._currentModelObject.getNameOfCurveToFitTo()
            arrayFitCurveToSignals = np.array(self._signalData[curveToFitTo], dtype='float')
            modelInputValue = self._currentModelObject.getValueOfInputVariableToModel()
            arrayModelInputSignals = np.array(self._signalData[modelInputValue], dtype='float')

            timeInputConcs2DArray = np.column_stack((self.arrayTimes, 
                                                         arrayModelInputSignals))
            
            QApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))
            objModel = Model(self._currentModelObject.modelFunction, \
            independent_vars=['xData2DArray', 'constantsString'])

            bestFitResults = objModel.fit(data=arrayFitCurveToSignals, 
                                  params=modelParams, 
                                  xData2DArray=timeInputConcs2DArray, 
                                  constantsString=self._constantsString)
            self.sigCurveFittingComplete.emit(bestFitResults.best_values)
            QApplication.restoreOverrideCursor()
            logger.info('CurveFit returned optimum parameters {}'
                        .format(bestFitResults.best_values))
            # Plot the best curve on the graph
            self.plotGraph()
           
            # Determine 95% confidence limits.
            numDataPoints = arrayFitCurveToSignals.size
            numParams = len(list(bestFitResults.best_values.values()))
            if bestFitResults.covar.size:
                self._CurveFitCalculate95ConfidenceLimits(numDataPoints, numParams, 
                                    bestFitResults.best_values, bestFitResults.covar)
        except ValueError as ve:
            print ('Value Error: CurveFit with model ' + modelName + ': '+ str(ve))
            logger.error('Value Error: CurveFit with model ' + modelName + ': '+ str(ve))
        except Exception as e:
            print('Error in function FerretPlotData.CurveFit with model ' + modelName + ': ' + str(e))
            logger.error('Error in function FerretPlotData.CurveFit with model ' + modelName + ': ' + str(e))
   

    def _CurveFitCalculate95ConfidenceLimits(self, numDataPoints: int, 
                                            numParams: int, 
                                            optimumParams, 
                                            bestFitResultsCovar):
        """Calculates the 95% confidence limits of optimum 
        parameter values resulting from curve fitting. 

        The the 95% confidence limits are passed back to the
        Ferret GUI for use in the creation of the PDF report
        and for display  on the GUI.
        
        Input Parameters
        ----------------
        numDataPoints -  Number of data points to which the model is fitted.
                Taken as the number of elements in the array of ROI data.
        numParams - Number of model input parameters.
        optimumParams - Array of optimum model input parameter values 
                        resulting from curve fitting.
        bestFitResults.covar - The estimated covariance of 
                the values in optimumParams calculated during 
                curve fitting.
        """
        try:
            logger.info('Function FerretPlotData._CurveFitCalculate95ConfidenceLimits called: numDataPoints ={}, numParams={}, optimumParams={}, bestFitResults.covar={}'
                        .format(numDataPoints, numParams, optimumParams, bestFitResultsCovar))
            alpha = 0.05 # 95% confidence interval = 100*(1-alpha)
            originalOptimumParams = optimumParams.copy()
            originalNumParams = numParams

            # Check for fixed parameters.
            # Removed fixed parameters from the optimum parameter list
            # as they should not be included in the calculation of
            # confidence limits
            for objCheckBox in self._parameterFixedCheckBoxList:
                if objCheckBox.isChecked():
                    del optimumParams[objCheckBox.shortName]
                    
            numDegsOfFreedom = max(0, numDataPoints - numParams) 
        
            # student-t value for the degrees of freedom and the confidence level
            tval = t.ppf(1.0-alpha/2., numDegsOfFreedom)
        
            # Remove results of previous curve fitting
            optimisedParamaterDict = {}
            optimumParamsList = list(optimumParams.values())
            for counter, paramValue, var in zip(range(numDataPoints), optimumParamsList, np.diag(bestFitResultsCovar)):
                # Calculate 95% confidence interval for each parameter 
                # allowed to vary and add these to a list
                key = list(optimumParams.keys())[list(optimumParams.values()).index(paramValue)]
                units = self._currentModelObject.getParameterUnits(key)
                tempList = []
                sigma = var**0.5
                lower = paramValue - sigma*tval
                upper = paramValue + sigma*tval
                if units == "%":
                    paramValue = paramValue * 100
                    lower = lower * 100.0
                    upper = upper * 100.0
                tempList.append(round(paramValue,4))
                tempList.append(round(lower,4))
                tempList.append(round(upper,4))
                tempList.append(units)
                optimisedParamaterDict[key] = tempList
                
            # Now insert fixed parameters into optimisedParameterList
            # if there are any.
            for objCheckBox in self._parameterFixedCheckBoxList:
                if objCheckBox.isChecked():
                    # Add the fixed optimum parameter value to a list
                    fixedParamValue = originalOptimumParams[objCheckBox.shortName]
                    units = self._currentModelObject.getParameterUnits(objCheckBox.shortName)
                    if units == "%":
                        fixedParamValue = fixedParamValue * 100
                    lower = ''
                    upper = ''
                    tempList = [fixedParamValue, lower, upper, units]
                    # Now add this list to the list of lists 
                    optimisedParamaterDict[objCheckBox.shortName] = tempList
            #Return results to the Ferret GUI
            self.sigReturnOptimumParamDict.emit(optimisedParamaterDict)
            logger.info('Leaving FerretPlotData._CurveFitCalculate95ConfidenceLimits, optimisedParamaterDict = {}'.format(optimisedParamaterDict))
        except RuntimeError as rte:
            print('Runtime Error in function FerretPlotData._CurveFitCalculate95ConfidenceLimits ' + str(rte))
            logger.error('Runtime Error in function FerretPlotData._CurveFitCalculate95ConfidenceLimits '  + str(rte))  
        except Exception as e:
            print('Error in function FerretPlotData._CurveFitCalculate95ConfidenceLimits ' + str(e))
            logger.error('Error in function FerretPlotData._CurveFitCalculate95ConfidenceLimits '  + str(e))  
    
