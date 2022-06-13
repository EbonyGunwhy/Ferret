# How to define models for use in Ferret
The following is a description of how to define one or more models for use in Ferret using the
Python programming language. The folder **Ferret\Developer\ModelLibrary** contains a Python file called
*MyModels.py* that contains the definition of two models.  This model library file may be cloned 
and edited to produce more model libraries.

It is assumed that the person carrying out this work is an experienced Python developer.

## Background
The folder **Ferret\Developer\ModelLibrary\SupportModules** contains a Python class module called *Model.py*.

Within *Model.py* there is a definition of the class *Model* that describes a mathematical model. 
As well as storing the long & short names of the model, this class stores name of the external function, 
that contains the logic of the mathematical model. 

A model may have no or  1 or more constants, parameters and variables. Consequently, the class *Model* can
store lists of parameter, constants and variable objects.  
Thus, Model.py, contains definitions of the classes, *ModelVariable*, *ModelConstant* & *ModelParameter* 
that describe a single model variable, model constant and model parameter respectively.

Additionally, the class *Model* has methods that are used to return information to the GUI.

The *Model* class has properties that are set by the following input arguments 
when a model object is created.

    shortName - the model's short name, usually an acronym. 
    longName - the model's full name.
    modelFunction - a function containing the logic of the mathematical model
                passed into the model object as an object

    parameterList - list of parameter objects that describe each of the
                parameters associated with the model. This argument is optional.

    constantsList - list of constant objects that describe each of the constants
                associated with the model. This argument is optional.

    variablesList - list of the variable objects that describe each of the variables
                associated with the model. This argument is optional.

For example, in the following code snippet a model object called *HF1_2CFM_2DSPGR* is created,
    '''
    HF1_2CFM_2DSPGR = Model(shortName='HF1-2CFM+2DSPGR', 
                     longName ='High Flow Single Inlet - Two Compartment Filtration and 2DSPGR Model', 
                     modelFunction = HighFlowSingleInletGadoxetate2DSPGR_Rat,
                     parameterList = setUpParameters(), 
                     constantsList = setUpConstants(),
                     variablesList = setUpVariables())
    '''
    The functions **HighFlowSingleInletGadoxetate2DSPGR_Rat**, **setUpParameters**, **setUpConstants** & 
    **setUpVariables** are defined outside the class.
    **setUpParameters**, **setUpConstants** &  **setUpVariables** return lists of parameter, constant & variable objects
    respectively.

### Model Variable
The *ModelVariable* class has properties that are set by the following input arguments 
when a model variable object is created.

    shortName - the variable's short name, usually an acronym.
    longName - the variable's full name.
    colour - the colour of the line used to plot the variable on a graph.
    inputToModel - boolean indicating if this variable forms input to the model
    fitCurveTo - boolean indicating if the model to fit to the curve of this variable
                    plotted on a graph.

For example, in the following code snippet a variable object called *regionOfInterest* is created,
    '''
    regionOfInterest = ModelVariable('ROI', 'Region of Interest', colour=LineColours.blueLine, inputToModel=False, fitCurveTo=True)
    '''
    This variable will be plotted with a solid blue line.  By including the following import statement in the model library file
    '''
    from SupportModules.GraphSupport import LineColours
    '''
    it is possible to easily define the line type and colour of this variable's plot on the line graph.
    Additionally, this variable will not be used as input to the model but the model curve will be
    fit to its curve.


### Model Constant
    On the Ferret GUI, a constant's value maybe displayed in a spin box
    or in a dropdown list if it takes a set of discrete values.
    On the Ferret GUI, it is possible to adjust the value of a constant
    in order to see how doing so changes the shape of the curve
    predicted by the model.

    The *ModelConstant* class has properties that are set by the following input arguments 
    when a model constant object is created.
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

    For example, in the following code snippet a constant object called *FA* is created,
    '''
    valuesFA = [str(x) for x in range(10,31,1)]
    FA = ModelConstant(shortName='FA', longName=None, defaultValue=20, stepSize=None,
                       precision=1, units = None, minValue=10, maxValue=30, listValues=valuesFA)
    '''
    FA takes an integer value in the range 10-30. It is represented on the GUI by a drop down list containing
    integers in the range 10-30 and it displays the default value of 20.

### Model Parameter
The *ModelParameter* class has properties that are set by the following input arguments 
when a model parameter object is created. On the Ferret GUI, a parameter is displayed in a spin box.
So, many of this class's parameters pertain to the display of the parameter value in a spin box

On the Ferret GUI, it is possible to adjust the value of a parameter
in order to see how doing so changes the shape of the curve predicted by the model.

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

For example, in the following code snippet a variable object called *regionOfInterest* is created,
    '''
    regionOfInterest = ModelVariable('ROI', 'Region of Interest', colour=LineColours.blueLine, inputToModel=False, fitCurveTo=True)
    '''
    This variable will be plotted with a solid blue line.  It will not be used as input to the model but the model curve will be
    fit to it.

## How to create a model library file
By analysing the code in *MyModels.py*, the creation of a model library file will be described.

### Import Statements
The following import statements make Python packages available that are needed in the coding of the mathematical models 
used in *MyModels.py*.  They may not be needed in your models.
'''
    #Python libraries that support running the models
    import numpy as np
    from scipy.optimize import fsolve
    from joblib import Parallel, delayed
    import SupportModules.MathsTools  as tools
'''
The following 2 module imports are mandatory for model definition. Although *LineColours*
will only be mandatory if you need to define model parameter(s).
'''
    from SupportModules.Model import Model, ModelParameter, ModelConstant, ModelVariable 
    from SupportModules.GraphSupport import LineColours
'''

### Model Functions
Next the function(s) that solve the mathematical model are defined. In order to comply with the needs
of the curve fitting function, *CurveFit* in *FerretPlotData.py*, the input arguments of this function
must have the following format as show in the definition of *HighFlowSingleInletGadoxetate2DSPGR_Rat*.
'''
    def HighFlowSingleInletGadoxetate2DSPGR_Rat(xData2DArray, Ve, Kbh, Khe, constantsString)
'''
    where 
    xData2DArray = the time and input variable 1-D arrays stacked as columns into a 2-D array. 
                   The formation of xData2DArray is performed in Ferret and the user does not
                   need to concern themself with this. This argument needs to be unpacked in
                   the function; thus,
                   '''
                   t = xData2DArray[:,0]
                   Sa = xData2DArray[:,1]
                   '''
    Ve, Kbh, Khe, = model parameters.  They need to be individually named as this is a requirment 
                    of the curve fitting function. *parameters would not work.
    constantsString = A string representation of a dictionary of constant name:value pairs.
                   The formation of constantsString is performed in Ferret and the user does not
                   need to concern themself with this.
                    This argument needs to be unpacked in the function; thus,
                    '''
                    constantsDict = eval(constantsString) 
                    TR, baseline, FA, r1, R10a, R10t = float(constantsDict['TR']), \
                    int(constantsDict['baseline']),\
                    float(constantsDict['FA']), float(constantsDict['r1']), \
                    float(constantsDict['R10a']), float(constantsDict['R10t']) 
                    '''
### Defining a list of constant objects
If your model uses constants, you will need to write a function that returns a list of one or more
constant objects.  The following is a function that returns a list of 2 constant objects.
'''
    def setUpConstants():
        constantList = []
        TR = ModelConstant(shortName='TR', longName=None, defaultValue=0.013, stepSize=0.001,
                           precision=4, units = None, minValue=0, maxValue=0.1, listValues=[])
        constantList.append(TR)

        baseLineValues = [str(x) for x in range(1,11,1)]
        baseline = ModelConstant(shortName='baseline', longName='baseline', 
                                 defaultValue=1, stepSize=None,
                           precision=1, units = None, minValue=1, maxValue=10, listValues=baseLineValues)
        constantList.append(baseline)
        return constantList
    '''

### Defining a list of parameter objects
If your model uses parameters, you will need to write a function that returns a list of one or more
parameter objects.  The following is a function that returns a list of 2 parameter objects.
'''
    def setUpParameters():
        paramList = []
        extraCellularVolFract = ModelParameter(shortName='Ve',
                                            longName='Extracellular Volume Fraction',
                                            units='%', 
                                            defaultValue=23.0, 
                                            stepSize=1.0, 
                                            precision=2, 
                                            minValue=0.01,
                                            maxValue=99.99)
        paramList.append(extraCellularVolFract)

        billaryEffluxRate = ModelParameter(shortName='Kbh',
                                            longName='Billiary Efflux Rate',
                                            units='mL/min/mL', 
                                            defaultValue=0.0918, 
                                            stepSize=0.01, 
                                            precision=4, 
                                            minValue=0.01, 
                                            maxValue=100.0)
        paramList.append(billaryEffluxRate)     
        return paramList
    '''

### Defining a list of variable objects
If your model uses variables, you will need to write a function that returns a list of one or more
variable objects.  This is a function that returns a list of 2 variable objects.
'''
    def setUpVariables():
        variablesList = []
        regionOfInterest = ModelVariable('ROI', 'Region of Interest', LineColours.blueLine, False, True)
        variablesList.append(regionOfInterest)

        arterialInputFunction = ModelVariable('AIF', 'Arterial Input Function', LineColours.redLine, True, False)
        variablesList.append(arterialInputFunction)
        return variablesList
'''

### Returning a list of model objects to Ferret
Every model library file must contain a **returnModelList()** function that returns a list of model objects
to Ferret.  When a model library file is selected in Ferret, its **returnModelList()** function is executed
in order to generate a list of model objects for use in Ferret.

Below is a **returnModelList()** function that returns a list of 2 model objects. Note the use
of the setUpParameters(), setUpConstants() & setUpVariables() functions to populate the parameterList, 
constantsList & variablesList properties respectively.

'''
    def returnModelList():
        HF1_2CFM_2DSPGR = Model(shortName='HF1-2CFM+2DSPGR', 
                         longName ='High Flow Single Inlet - Two Compartment Filtration and 2DSPGR Model', 
                         modelFunction = HighFlowSingleInletGadoxetate2DSPGR_Rat,
                         parameterList = setUpParameters(), 
                         constantsList = setUpConstants(),
                         variablesList = setUpVariables()
                         )
        
        HF1_2CFM_3DSPGR = Model(shortName='HF1-2CFM+3DSPGR', 
                         longName ='High Flow Single Inlet - Two Compartment Filtration and 3DSPGR Model', 
                         modelFunction = HighFlowSingleInletGadoxetate3DSPGR_Rat,
                         parameterList = setUpParameters(),  
                         constantsList = setUpConstants(),
                         variablesList = setUpVariables()
                         )
    
        return[HF1_2CFM_2DSPGR, HF1_2CFM_3DSPGR]
'''

### The function *returnDataFileFolder*
This is a an optional function that returns the file path to the folder containing 
CSV data files that form the input to Ferret. 
Including the following import statement in *Ferret.py* allows this function to be run to return the
file path to the folder containing the data files.  See the *main()* function in Ferret.py.

'''
    from MyModels import returnDataFileFolder
    ferretWidget = Ferret(statusBar=window.statusBar(),  dataFileFolder=returnDataFileFolder())
'''

### Passing a list of model objects into Ferret.
Rather than manually selecting a model library file, it is possible to pass a list of model objects
into Ferret.  See the *main()* function in Ferret.py.

'''
    from MyModels import returnDataFileFolder
    from MyModels import returnModelList
    ferretWidget = Ferret(statusBar=window.statusBar(),
                             dataFileFolder=returnDataFileFolder(),
                             modelList=returnModelList())
'''