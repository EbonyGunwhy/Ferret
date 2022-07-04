# Running Ferret
Ferret.py is the start-up file when Ferret is used as a stand-alone application. Ferret.py contains the definition of the Ferret class that inherits from the PyQt5 QWidget class to create a custom widget. When Ferret is run as a stand-alone application, the Ferret widget is hosted on a QMainWindow window. When Ferret is run within Weasel, the Ferret widget is hosted on a PyQt5 QMdiSubWindow subwindow within the Weasel MDI.

LaunchFerretFromWeasel.py is the file that launches Ferret from a menu item in Weasel. To add Ferret to a menu in Weasel, insert the following lines of code in a Menu Python file,

    menu.separator()
    menu.item(
        label = 'Ferret',
        pipeline = 'LaunchFerretFromWeasel')
        
The menu item **Ferret** will be created below a horizontal separater line.

# How to define models for use in Ferret
## Background
The folder **Ferret\Developer\ModelLibrary\SupportModules** contains a Python class module called *Model.py*.

### Model class
Within *Model.py* there is a definition of the class *Model* that describes a mathematical model. 
As well as storing the long & short names of the model, this class stores the external function, 
that contains the logic of the mathematical model, as an object. 

A model may have zero, 1 or more constants, parameters and variables. Consequently, the class *Model* can
store lists of parameter, constant and variable objects.  
Thus, Model.py, contains definitions of the classes, *ModelVariable*, *ModelConstant* & *ModelParameter* 
that describe a single model variable, model constant and model parameter respectively.

Additionally, the class *Model* has methods that are used to return information to the GUI.

The *Model* class has properties that are set by the following input arguments 
when a model object is created.

    shortName - the model's short name, usually an acronym. 
    
    longName - the model's full name.
    
    modelFunction - a function containing the logic of the mathematical model
                passed into the model object as an object.
                
    xDataInputOnly - boolean indicating if the only input to the model is x axis data.
                Default is False, both x and y axis data are input to the model.
                
    parameterList - list of parameter objects that describe each of the
                parameters associated with the model. This argument is optional.

    constantsList - list of constant objects that describe each of the constants
                associated with the model. This argument is optional.

    variablesList - list of the variable objects that describe each of the variables
                associated with the model. This argument is optional.
                
    returnMessageFunctionName - a function returning messages from the equation solving function passed into the model object as an object.

### Model Variable class
The *ModelVariable* class has properties that are set by the following input arguments 
when a model variable object is created.

    shortName - the variable's short name, usually an acronym.
    
    longName - the variable's full name.
    
    colour - the colour of the line used to plot the variable on a graph.
    
    inputToModel - boolean indicating if this variable forms input to the model.
    
    fitCurveTo - boolean indicating if the model to be fitted to the curve of this variable
                    plotted on a graph.

### Model Constant class
On the Ferret GUI, a constant's value is displayed in either a spin box
or in a dropdown list if it takes a set of discrete values.
On the Ferret GUI, it is possible to adjust the value of a constant
in order to see how doing so changes the shape of the curve predicted by the model.

The *ModelConstant* class has properties that are set by the following input arguments 
when a model constant object is created.

        shortName - the constant's short name, usually an acronym.
        
        longName - the constant's full name.
        
        defaultValue - the constant's default value.
        
        stepSize - when constant's spinbox arrows are clicked, 
                the value of the parameter is incremented/decremented by 
                the value of stepSize.
                
        precision - the number of decimal places displayed in the constant's spinbox.
        
        minValue - the minimum value of the constant's spinbox.
        
        maxValue - the maximum value of the constant's spinbox.
        
        listValues - the list of discrete values that a constant may take.
        
### Model Parameter class
On the Ferret GUI, a parameter is displayed in a spin box.
So, many of this class's input arguments pertain to the display of the parameter value in a spin box.
On the Ferret GUI, it is possible to adjust the value of a parameter
in order to see how doing so changes the shape of the curve predicted by the model.

The *ModelParameter* class has properties that are set by the following input arguments 
when a model parameter object is created.

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
                    
The following is a description of how to define one or more models, using the
Python programming language, for use in Ferret. 

## Defining a simple linear model.
In order to make a simple linear model available for use in Ferret, such as

        y = ax + b
   
where a and b are parameters.
   
the following steps must be followed. The full implementation of this model can be found in the file **Ferret\Developer\ModelLibrary\SimpleModels.py**

1. Place the following import statements at the top of your model library file.     
The first module import is mandatory for model definition.
*LineColours* will only be mandatory if you need to define model parameter(s).
    
        from SupportModules.Model import Model, ModelParameter, ModelConstant, ModelVariable 
        from SupportModules.GraphSupport import LineColours

2. Write a function that executes the mathematical model in your model library file. 

        import numpy as np
        def linearModel(inputData, a, b, constantsString=None):
             return np.multiply(inputData,a) + b
             
 The input argument **inputData** is used for the independent variable and its usuage is required to satisfy the needs of the curve fitting package used in Ferret.   **constantsString** is a string representation of a Python dictionary of constant name:value pairs.  It is also required to satisfy the needs of the curve fitting package used in Ferret.  In the case of this model, there are no constants, so it is set to **None**.
         
 3. Every model library file must have a **returnModelList** function.  Within the **returnModelList** function, define a model object to represent the above model.
 
        def returnModelList():
            linear = Model(shortName='Linear', 
                     longName ='Linear', 
                     xDataInputOnly = True,
                     modelFunction = linearModel,
                     parameterList = setUpParametersForLinearModel(), 
                     variablesList = setUpVariablesForAllModels(),
                     returnMessageFunction=None)
                     
            return [linear]
            
The input argument **returnMessageFunction** is set to **None** because this function can be evaluated by substitution and the **fsolve** function in **Ferret\Developer\ModelLibrary\SupportModules\ScipyMathsTools.py** is not used.  **fsolve** returns messages on the progress of the solution to the GUI via the function name in **returnMessageFunction**.                     
The functions **setUpParametersForLinearModel** and  **setUpVariablesForAllModels** are defined outside the class and they return lists of parameters and variables respectively.

4. Write the function, **setUpParametersForLinearModel** to return a list of model parameters in your model library file.

        def setUpParametersForLinearMode():
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

5. Write the function, **setUpVariablesForAllModels** that returns a list of model variables in your model library file.
    
        def setUpVariablesForAllModels():
            variablesList = []
            X = ModelVariable('X', 'X', LineColours.blueLine, False, True)
            variablesList.append(X)

            X2 = ModelVariable('X2', 'X2', LineColours.redLine, True, False)
            variablesList.append(X2)
            return variablesList


## Defining a simple linear model that utilises the equation of a straight line.
In order to make a simple linear model available for use in Ferret, such as

    y = mx + c
   
    where m is a parameters and c is a constant.
   
the following steps must be followed.
The full implementation of this model can be found in the file  **Ferret\Developer\ModelLibrary*\SimpleModels.py**

1. Place the following import statements at the top of your model library file.     
These 2 module imports are mandatory for model definition. Although *LineColours*
will only be mandatory if you need to define model parameter(s).
    
        from SupportModules.Model import Model, ModelParameter, ModelConstant, ModelVariable 
        from SupportModules.GraphSupport import LineColours

2. Write a function that executes the mathematical model in your model library file.  constantsString is a string representation of a Python dictionary of constant name:value pairs.  It is required to satisfy the needs of the curve fitting package used in Ferret.  

        import numpy as np
        def straightLineModel(inputData, m, constantsString):
            constantsDict = eval(constantsString) 
            c = float(constantsDict['c'])
            return np.multiply(inputData, m) + c
            
 The input argument **inputData** is used for the independent variable and its usuage is required to satisfy the needs of the curve fitting package used in Ferret.   **constantsString** is a string representation of a Python dictionary of constant name:value pairs.  It is also required to satisfy the needs of the curve fitting package used in Ferret.  The building of a string represention of a Python dictionary of constant name:value pairs is done by Ferret and you do not need to worry about this. However, you need to include code in your model function to unpack the value(s) of the constant(s).
         
 3. Every model library file must have a **returnModelList** function.  Within the **returnModelList** function, define a model object to represent the above model.
 
        def returnModelList():
            straightLine = Model(shortName='Straight Line',
                         longName='Straight Line',
                         xDataInputOnly = True,
                         modelFunction = straightLineModel,
                         parameterList = setUpParameterForStraightLineModel(), 
                         variablesList = setUpVariablesForAllModels(),
                         constantsList = setUpConstantForYAxisIntersection(),
                         returnMessageFunction=None)
                     
            return [straightLine]
                     
The input argument **returnMessageFunction** is set to **None** because this function can be evaluated by substitution and the **fsolve** function in **Ferret\Developer\ModelLibrary\SupportModules\ScipyMathsTools.py** is not used.  **fsolve** returns messages on the progress of the solution to the GUI via the function name in **returnMessageFunction**.
The functions **setUpParameterForStraightLineModel**,  **setUpVariablesForAllModels**  and **setUpConstantForYAxisIntersection** are defined outside the class in your model library file and they return lists of parameters, variables and a constant respectively.

4. Write the function, **setUpParameterForStraightLineModel** to return a list of model parameters in your model library file.

       def setUpParameterForStraightLineModel():
            paramList = []
            m = ModelParameter(shortName='m',
                                longName='m',
                                units='/s', 
                                defaultValue=1.0, 
                                stepSize=1, 
                                precision=1, 
                                minValue=1, 
                                maxValue=100.0)
            paramList.append(m)    
            return paramList

5. Write the function, **setUpVariablesForAllModels** that returns a list of model variables in your model library file.
    
        def setUpVariablesForAllModels():
            variablesList = []
            X = ModelVariable('X', 'X', LineColours.blueLine, False, True)
            variablesList.append(X)

            X2 = ModelVariable('X2', 'X2', LineColours.redLine, True, False)
            variablesList.append(X2)
            return variablesList

6. Write the function **setUpConstantForYAxisIntersection** that returns a list of model constants in your model library file.

        def setUpConstantForYAxisIntersection():
            constantList = []
            c = ModelConstant(shortName='c', longName='Y Axis Intersection', defaultValue=1.0, stepSize=10.0,
                               precision=1, units = None, minValue=0, maxValue=10000, listValues=[])
            constantList.append(c)
            return constantList

## Defining a simple quadratic model.
In order to make a simple quadratic model available for use in Ferret, such as

$$y = ax^2 + bx + c$$
   
where a and b are parameters and c is a constant.
   
the following steps must be followed.
The full implementation of this model can be found in the file  **Ferret\Developer\ModelLibrary\SimpleModels.py**

1. Place the following import statements at the top of your model library file.     
These 3 module imports are mandatory for model definition. Although *LineColours*
will only be mandatory if you need to define model parameter(s). 
    
        from SupportModules.Model import Model, ModelParameter, ModelConstant, ModelVariable 
        from SupportModules.GraphSupport import LineColours
        

2. Write a function that executes the mathematical model in your model library file.  

       import numpy as np
       def quadraticModel(inputData, a, b, constantsString):
            constantsDict = eval(constantsString) 
            c = float(constantsDict['c'])
            return np.multiply((inputData**2),a) + np.multiply(inputData, b) + c
 
 The input argument **inputData** is used for the independent variable and its usuage is required to satisfy the needs of the curve fitting package used in Ferret.   **constantsString** is a string representation of a Python dictionary of constant name:value pairs.  It is also required to satisfy the needs of the curve fitting package used in Ferret.  The building of a string represention of a Python dictionary of constant name:value pairs is done by Ferret and you do not need to worry about this. However, you need to include code in your model function to unpack the value(s) of the constant(s).
 
 3. Every model library file must have a **returnModelList** function.  Within the **returnModelList** function, define a model object to represent the above model.
 
        def returnModelList():
            quadratic = Model(shortName='Quadratic',
                         longName='Quadratic',
                         xDataInputOnly = True,
                         modelFunction = quadraticModel,
                         parameterList = setUpParametersForQuadraticModel(), 
                         variablesList = setUpVariablesForAllModels(),
                         constantsList = setUpConstantForYAxisIntersection(),
                         returnMessageFunction=None)
                     
            return [quadratic]
            
The input argument **returnMessageFunction** is set to **None** because this function can be evaluated by substitution and the **fsolve** function in **Ferret\Developer\ModelLibrary\SupportModules\ScipyMathsTools.py** is not used.  **fsolve** returns messages on the progress of the solution to the GUI via the function name in **returnMessageFunction**.                     
The functions **setUpParametersForQuadraticModel**,  **setUpVariablesForAllModels**  and **setUpConstantForYAxisIntersection** are defined outside the class and they return lists of parameters and variables respectively.

4. Write the function, **setUpParametersForQuadraticModel** to return a list of model parameters in your model library file.

       def setUpParametersForQuadraticModel():
            paramList = []
            a = ModelParameter(shortName='a',
                                longName='a',
                                units='mL/min/mL', 
                                defaultValue=4.0, 
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

5. Write the function, **setUpVariablesForAllModels** that returns a list of model variables in your model library file.
    
        def setUpVariablesForAllModels():
            variablesList = []
            X = ModelVariable('X', 'X', LineColours.blueLine, False, True)
            variablesList.append(X)

            X2 = ModelVariable('X2', 'X2', LineColours.redLine, True, False)
            variablesList.append(X2)
            return variablesList

6. Write the function **setUpConstantForYAxisIntersection** that returns a list of model constants in your model library file.

        def setUpConstantForYAxisIntersection():
            constantList = []
            c = ModelConstant(shortName='c', longName='Y Axis Intersection', defaultValue=1.0, stepSize=10.0,
                               precision=1, units = None, minValue=0, maxValue=10000, listValues=[])
            constantList.append(c)
            return constantList

## Defining a complex model that describes the function of the liver.
The full implementation of this model can be found in the file  **Ferret\Developer\ModelLibrary*\MyModels.py**
The following steps must be followed.

1. Place the following import statements at the top of your model library file.     
These 2 module imports are mandatory for model definition. Although *LineColours*
will only be mandatory if you need to define model parameter(s). *LineColours* provides an easy means of defining line style and colour when plotting variables on a graph. Additionally, *ScipyMathsTools* will only be mandatory if you need to use the **fsolve** fuction to solve your mathematical model.
    
        from SupportModules.Model import Model, ModelParameter, ModelConstant, ModelVariable 
        from SupportModules.GraphSupport import LineColours
        import SupportModules.ScipyMathsTools  as scipyTools

2. Write a function that executes the mathematical model in your model library file.  In order to comply with the needs
of the curve fitting function, *CurveFit* in *FerretPlotData.py*, the input arguments of this function
must have the following format as show in the definition of *HighFlowSingleInletGadoxetate2DSPGR_Rat*.

        def HighFlowSingleInletGadoxetate2DSPGR_Rat(inputData, Ve, Kbh, Khe, constantsString):

where 
inputData = the time and input variable 1-D arrays stacked as columns into a 2-D array. 
               The formation of inputData is performed in Ferret and the user does not
               need to worry about this. The input argument name **inputData** must be used to satisfy the needs of the curve fitting function used in Ferret.
               This argument needs to be unpacked in the function; thus,
               
               t = inputData[:,0]
               Sa = inputData[:,1]
              
Ve, Kbh, Khe, = model parameters.  They need to be individually named as this is a requirment 
                of the curve fitting function. 
                
constantsString = A string representation of a dictionary of constant name:value pairs.
               The formation of constantsString is performed in Ferret and the user does not
               need to concern themself with this.
               This argument needs to be unpacked in the function; thus,
             
                constantsDict = eval(constantsString) 
                TR, baseline, FA, r1, R10a, R10t = float(constantsDict['TR']), \
                int(constantsDict['baseline']),\
                float(constantsDict['FA']), float(constantsDict['r1']), \
                float(constantsDict['R10a']), float(constantsDict['R10t'])  


This function must contain the a global string variable initialised to a blank string; thus,
        global lastMessage
        lastMessage = ''
        
ScipyMathsTools.fsolve return the roots of a (non-linear) equation of the form  *func(x) = 0* given a starting estimate.  See this function's
docstring for further details.  In this model function, its usuage takes the following form,

        results = [scipyTools.fsolve(tools.spgr2d_func, x0=0, 
            args = (r1, FA, TR, R10a, baseline, Sa[p])) 
            for p in np.arange(0,len(t))]

        #The following 3 lines of code are mandatory in order to 
        #extract the result and message from fsolve
        R1a= [item[0] for item in results]
        messages = [item[1] for item in results]
        lastMessage = messages[len(messages)-1]
   

3. Every model library file must have a **returnModelList** function.  Within the **returnModelList** function, define a model object to represent the above model.
 
         def returnModelList():
                HF1_2CFM_2DSPGR = Model(shortName='HF1-2CFM+2DSPGR', 
                         longName ='High Flow Single Inlet - Two Compartment Filtration and 2DSPGR Model', 
                         modelFunction = HighFlowSingleInletGadoxetate2DSPGR_Rat,
                         parameterList = setUpParameters(), 
                         constantsList = setUpConstants(),
                         variablesList = setUpVariables(),
                         returnMessageFunction=None)
                 return [HF1_2CFM_2DSPGR]
 
 The input argument **returnMessageFunction** is set to **None** because this function can be evaluated by substitution and the **fsolve** function in **Ferret\Developer\ModelLibrary\SupportModules\ScipyMathsTools.py** is not used.  **fsolve** returns messages on the progress of the solution to the GUI via the function name in **returnMessageFunction**.
The functions **setUpParameters**, **setUpConstants** & **setUpVariables** are defined outside the class in your model library file.
**setUpParameters**, **setUpConstants** &  **setUpVariables** return lists of parameter, constant & variable objects
respectively.

4. Write the function, **setUpParameters** to return a list of model parameters in your model library file.

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


5. Write the function, **setUpVariables** that returns a list of model variables in your model library file. 

        def setUpVariables():
            variablesList = []
            #This variable will be plotted with a solid blue line
            regionOfInterest = ModelVariable('ROI', 'Region of Interest', LineColours.blueLine, inputToModel=False, fitCurveTo=True)
            variablesList.append(regionOfInterest)

            This variable will be plotted with a solid red line
            arterialInputFunction = ModelVariable('AIF', 'Arterial Input Function', LineColours.redLine, inputToModel=True, fitCurveTo=False)
            variablesList.append(arterialInputFunction)
            
            return variablesList

6. Write the function **setUpConstants** that returns a list of model constants in your model library file.

        def setUpConstants():
            constantList = []

            valuesFA = [str(x) for x in range(10,31,1)]
            FA = ModelConstant(shortName='FA', longName=None, 
                                     defaultValue=20, stepSize=None,
                               precision=1, units = None, minValue=10, maxValue=30, listValues=valuesFA)
            constantList.append(FA)

            return constantList


    In the above code snippet a constant object called *FA* is created,
    FA takes an integer value in the range 10-30. It is represented on the GUI by a drop down list containing
    integers in the range 10-30 and it displays the default value of 20.
    
7. Write the function **returnSolverMessage** to return the last message from fsolve to the GUI for display; thus,

        def returnSolverMessage():
            return lastMessage
    
    
### The function *returnDataFileFolder*
This is a an optional function that returns the file path to the folder containing 
CSV data files that form the input to Ferret. 
Including the following import statement in *Ferret.py* allows this function to be run to return the
file path to the folder containing the data files.  See the *main()* function in Ferret.py.

   
    from MyModels import returnDataFileFolder
    ferretWidget = Ferret(statusBar=window.statusBar(),  dataFileFolder=returnDataFileFolder())
    
 The argument statusBar=window.statusBar(), allows the Ferret widget to display messages in the status bar of the window hosting it.
 
### Passing a list of model objects into Ferret.
Rather than manually selecting a model library file, it is possible to pass a list of model objects
into Ferret.  See the *main()* function in Ferret.py.

    from MyModels import returnDataFileFolder
    from MyModels import returnModelList
    ferretWidget = Ferret(statusBar=window.statusBar(),
                             dataFileFolder=returnDataFileFolder(),
                             modelList=returnModelList())
    
