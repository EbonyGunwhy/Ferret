import numpy as np
from SupportModules.Model import Model, ModelParameter, ModelConstant, ModelVariable 
from SupportModules.GraphSupport import LineColours

def linear(inputData, a, b, constantsString=None):
    return np.multiply(inputData,a) + b

#*******************************************************************************
#** Define parameters for the model
#*******************************************************************************
def setUpParametersForLinearModel():
    """
    This optional function returns a list of parameter objects.

    An object is created for each parameter using the ModelParameter class 
    and added to the list, that is returned by this function.

    In the returnModelList function, this function is used to 
    populate the parameterList argument. 
    """
    paramList = []
    a = ModelParameter(shortName='a',
                        longName='a',
                        units='mL/min/mL', 
                        defaultValue=1.0, 
                        stepSize=1, 
                        precision=1, 
                        minValue=1, 
                        maxValue=100.0)
    paramList.append(a)    
    b = ModelParameter(shortName='b',
                        longName='b',
                        units='mL/min/mL', 
                        defaultValue=2, 
                        stepSize=1, 
                        precision=1, 
                        minValue=1, 
                        maxValue=100.0)
    paramList.append(b)    
    return paramList

#*******************************************************************************
# Define variables for both models
#*******************************************************************************
def setUpVariablesForLinearModel():
    """
    This optional function returns a list of variable objects.

    An object is created for each variable using the ModelVariable class 
    and added to the list, that is returned by this function.

    In the returnModelList function, this function is used to 
    populate the variablesList argument. 
    """
    variablesList = []
    X = ModelVariable('X', 'X', LineColours.blueLine, False, True)
    variablesList.append(X)

    X2 = ModelVariable('X2', 'X2', LineColours.redLine, True, False)
    variablesList.append(X2)
    return variablesList


def returnModelList():
    """
    This mandatory function returns a list of Model objects.

    Every model library module must contain an implementation of this function.

    An object is created for each mathematic model using the Model class 
    and added to the list, that is returned by this function.
    """
    Linear = Model(shortName='Linear', 
                     longName ='Linear', 
                     xDataInputOnly = True,
                     modelFunction = linear,
                     parameterList = setUpParametersForLinearModel(), 
                     variablesList = setUpVariablesForLinearModel()
                     )
   
    return[Linear]


def returnDataFileFolder():
    """
    An optional function that returns the file path to the folder containing 
    CSV data files that form the input to Ferret.
    """
    return 'FerretData'