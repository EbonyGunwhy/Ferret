"""
This module contains classes for the definition of a mathematical model 
for use in Ferret.

Model =  class for an MRI mathematical model
ModelParameter =  class for an MRI mathematical model parameter
"""
from FerretConstants import FerretConstants

class Model:
    """
    This class describes a mathematical model.

    As well as storing the name of the external function, that 
    contains the logic of the mathematical model, this class stores
    lists of parameter, constants and variable objects.

    input arguments
    ***************
    shortName - the model's short name, usually an acronym.
    longName - the model's full name.
    modelFunction - a function containing the logic of the mathematical model
                passed into the model object as an object

    parameterList - list of parameter objects that describe each of the
                parameters associated with the model

    constantsList - list of constant objects that describe each of the constants
                associated with the model

    variablesList - list of the variable objects that describe each of the variables
                associated with the model
    """
    def __init__(self, shortName, longName, modelFunction,
                 parameterList=[], constantsList=[], variablesList=[]):
        self._shortName = shortName
        self._longName = longName
        self._parameterList = parameterList #list of parameter objects
        self._constantsList = constantsList #list of parameter objects
        self._variablesList = variablesList #list of variable objects
        self._modelFunction = modelFunction #function containing the mathematical model


    def getNumberConstants(self):
        return len(self._constantsList)


    def getNumberParameters(self):
        return len(self._parameterList)


    def getNameOfCurveToFitTo(self): 
        """
        This function returns the name of the variable, whose curve the model
        should be fit to by adjusting it's parameters to get a best fit.
        """
        for variable in self._variablesList:
            if variable.fitCurveTo:
                if variable.value != FerretConstants.PLEASE_SELECT:
                    return variable.value
                else:
                    return None


    def getValueOfInputVariableToModel(self): 
        """
        This function returns the value of the variable that
        is input to the model.
        """
        for variable in self._variablesList:
            if variable.inputToModel:
                if variable.value != FerretConstants.PLEASE_SELECT:
                    return variable.value
                else:
                    return None


    def getDefaultConstantValue(self, shortName):
        """
        This function returns the default value of the constant 
        with the short name, shortName
        """
        for const in self._constantsList:
            if const.shortName == shortName:
                return const.defaultValue


    def getConstantListValues(self, shortName):
        """
        This function returns the list of values that the 
        constant, whose name is shortName, may take.
        """
        for const in self._constantsList:
            if const.shortName == shortName:
                return const.listValues


    def getDefaultParameterValue(self, shortName):
        """
        This function returns the default value of the 
        parameter with the short name, shortName
        """
        for param in self._parameterList:
            if param.shortName == shortName:
                return param.defaultValue


    def getParameterUnits(self, shortName):
        """
        This function returns the units of the 
        parameter with the short name, shortName
        """
        for param in self._parameterList:
            if param.shortName == shortName:
                return param.units


    def __repr__(self):
        """Represents this class's objects as a string"""
        return 'Model object for Model {}, {}'.format(self._shortName, self._longName)

    @property
    def shortName(self):
         return self._shortName

    @property
    def longName(self):
         return self._longName

    @property
    def parameterList(self):
        return self._parameterList

    @parameterList.setter
    def parameterList(self, value):
       self._parameterList = value

    @property
    def constantsList(self):
        return self._constantsList

    @constantsList.setter
    def constantsList(self, value):
       self._constantsList = value

    @property
    def variablesList(self):
        return self._variablesList

    @variablesList.setter
    def variablesList(self, value):
       self._variablesList = value

    @property
    def modelFunction(self):
        return self._modelFunction

   
class ModelVariable:
    """
    This class describes a variable in the mathematical model.

    input arguments
    ***************
    shortName - the variable's short name, usually an acronym.
    longName - the variable's full name.
    colour - the colour of the line used to plot the variable on a graph.
    inputToModel - boolean indicating if this variable forms input to the model
    fitCurveTo - boolean indicating if the model to fit to the curve of this variable
                    plotted on a graph.
    """
    def __init__(self, shortName, longName=None, colour=None,  inputToModel=True, fitCurveTo=False):
        self._shortName = shortName
        self._longName = longName
        self._value = None
        self._plotLineColour = colour  #Model output is plotted on a graph with this colour
        self._inputToModel = inputToModel  #This variable is an input to the model
        self._fitCurveTo = fitCurveTo  #Model parameters are adjusted to fit the model to this variable

    def __repr__(self):
            """Represents this class's objects as a string"""
            return 'Variable object for variable {}, {}'.format(self._shortName, self._longName)
    
    @property
    def fitCurveTo(self):
        return self._fitCurveTo

    @property
    def inputToModel(self):
        return self._inputToModel

    @property
    def plotLineColour(self):
        return self._plotLineColour

  
    def setValue(self, value):
       self._value = value

    @property
    def value(self):
        return self._value

    @property
    def shortName(self):
         return self._shortName

    @property
    def longName(self):
         return self._longName


class ModelConstant:
    """
    This class describes a constant in the mathematical model. 

    On the Ferret GUI, a constant's value maybe displayed in a spin box
    or in a dropdown list if it takes a set of discrete values.
    On the Ferret GUI, it is possible to adjust the value of a constant
    in order to see how doing so changes the shape of the curve
    predicted by the model.

    input arguments
    ***************
    shortName - the constant's short name, usually an acronym.
    longName - the constant's full name.
    defaultValue - the constant's default value.
    stepSize - when constant's spinbox arrows are clicked, 
            the value of the parameter is incremented/decremented by 
            the value of stepSize.
    precision - the number of decimal places displayed in the constant's spinbox
    minValue - the minimum value of the constant's spinbox.
    maxValue - the maximum value of the constant's spinbox.
    listValues - the list of discrete values that a constant may take.
    """
    def __init__(self, shortName, longName=None, defaultValue=0.0, stepSize=1.0,precision=3,
                 units = None, minValue=0, maxValue=1000, listValues=[]):
        self._shortName = shortName
        self._longName = longName
        self._units = units
        self._defaultValue = defaultValue
        self._stepSize = stepSize
        self._precision = precision
        self._minValue = minValue
        self._maxValue = maxValue
        self._listValues = listValues

    def __repr__(self):
            """Represents this class's objects as a string"""
            return 'Constant object for constant {}, {}'.format(self._shortName, self._longName)

    @property
    def shortName(self):
         return self._shortName

    @property
    def longName(self):
         return self._longName

    @property
    def units(self):
        return self._units

    @property
    def defaultValue(self):
        return self._defaultValue

    @property
    def stepSize(self):
        return self._stepSize

    @property
    def precision(self):
        return self._precision

    @property
    def minValue(self):
        return self._minValue

    @property
    def maxValue(self):
        return self._maxValue

    @property
    def listValues(self):
        return  self._listValues


class ModelParameter:
    """
    This class describes a parameter associated with a mathematical model.

    On the Ferret GUI, a parameters is displayed in a spin box.

    On the Ferret GUI, it is possible to adjust the value of a parameter
    in order to see how doing so changes the shape of the curve
    predicted by the model.

    input arguments
    ***************
    shortName - the parameter's short name, usually an acronym.
    longName - the parameter's full name.
    units - the units of the parameter
    defaultValue - the parameter's default value.
    stepSize - when parameter's spinbox arrows are clicked, 
            the value of the parameter is incremented/decremented by 
            the value of stepSize.
    precision - the number of decimal places displayed in the parameter's spinbox
    minValue - the minimum value of the parameter's spinbox.
    maxValue - the maximum value of the parameter's spinbox.
    lowerConstraint - the lower constraint put on the parameter's value 
                    when the model is fitted to the curve formed by experimental data.
    upperConstraint - the upper constraint put on the parameter's value 
                    when the model is fitted to the curve formed by experimental data.
    """
    def __init__(self, shortName, 
                 longName, units='%',
                 defaultValue=0.0, stepSize=1.0,
                 precision=3,
                 minValue=0, maxValue=1000,
                 lowerConstraint=None, upperConstraint=None
                 ):
        self._shortName = shortName
        self._longName = longName
        self._units = units
        self._defaultValue = defaultValue
        self._stepSize = stepSize
        self._precision = precision
        self._minValue = minValue
        self._maxValue = maxValue
        self._lowerConstraint = lowerConstraint
        self._upperConstraint = lowerConstraint
        self._parameterValue = 0

    def __repr__(self):
        """Represents this class's objects as a string"""
        return 'Parameter object for parameter {}, {}'.format(self._shortName, self._longName)

    @property
    def shortName(self):
         return self._shortName

    @property
    def longName(self):
         return self._longName

    @property
    def units(self):
        return self._units

    @property
    def defaultValue(self):
        return self._defaultValue

    @property
    def stepSize(self):
        return self._stepSize

    @property
    def precision(self):
        return self._precision

    @property
    def minValue(self):
        return self._minValue

    @property
    def maxValue(self):
        return self._maxValue

    @property
    def lowerConstraint(self):
        return self._lowerConstraint
    
    @property
    def upperConstraint(self):
        return self._upperConstraint

    @property
    def parameterValue(self):
        return self._parameterValue

    @parameterValue.setter
    def parameterValue(self, value):
       self._parameterValue = value




