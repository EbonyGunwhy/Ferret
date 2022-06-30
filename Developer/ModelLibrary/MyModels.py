"""
This module contains a library of models that can be used in Ferret.

It must contain a returnModelList function and a function for each
mathematical model.
"""
#Python libraries that support running the models
import numpy as np
#from scipy.optimize import fsolve
from joblib import Parallel, delayed
import SupportModules.MathsTools  as tools
import SupportModules.ScipyMathsTools  as scipyTools

#The following 2 module imports are mandatory for model definition.
#Note that modules are imported as parentPackage.module.
#This allows Ferret to be launched from Weasel and used as a
#standalone application.
#At the head of Ferret.py, the path to folder SupportModules is
#added to sys.path, which contains a list of directories 
#that the interpreter will search in for the required module.
from SupportModules.Model import Model, ModelParameter, ModelConstant, ModelVariable 
from SupportModules.GraphSupport import LineColours
#*************************************************************************************
#** Model 1 Definition
#*************************************************************************************
def HighFlowSingleInletGadoxetate2DSPGR_Rat(inputData, Ve, Kbh, Khe, constantsString):
    """This function contains the algorithm for calculating 
    how MR signal from a 2D scan varies with time using the 
    High Flow Single Inlet Two Compartment Gadoxetate Model.
        
        Input Parameters
        ----------------
            inputData - time and AIF concentration 1D arrays 
                stacked into one 2D array.
            Ve - Plasma Volume Fraction (decimal fraction).
            Khe - Hepatocyte Uptake Rate (mL/min/mL)
            Kbh - Biliary Efflux Rate (mL/min/mL) 
            constantsString - A string representation of a dictionary of constant name:value pairs.

        Returns
        -------
        St_rel - list of calculated MR signals at each of the 
            time points in array 'time'.
    """ 
    try:
        t = inputData[:,0]
        Sa = inputData[:,1]
         # Unpack SPGR model constants from 
        # a string representation of a dictionary
        # of constants and their values
        constantsDict = eval(constantsString) 
        TR, baseline, FA, r1, R10a, R10t = float(constantsDict['TR']), \
        int(constantsDict['baseline']),\
        float(constantsDict['FA']), float(constantsDict['r1']), \
        float(constantsDict['R10a']), float(constantsDict['R10t']) 
        # Convert to concentrations
        # n_jobs set to 1 to turn off parallel processing
        # because parallel processing caused a segmentation
        # fault in the compiled version of this application. 
        # This is not a problem in the uncompiled script
        R1a = [Parallel(n_jobs=1)(delayed(scipyTools.fsolve)
           (tools.spgr2d_func, x0=0, 
            args = (r1, FA, TR, R10a, baseline, Sa[p])) 
            for p in np.arange(0,len(t)))]
        
        R1a = np.squeeze(R1a)
        
        ca = (R1a - R10a)/r1
        
        # Correct for spleen Ve
        ve_spleen = 0.43
        ce = ca/ve_spleen
        
        if Kbh != 0:
            Th = (1-Ve)/Kbh
            ct = Ve*ce + Khe*Th*tools.expconv(Th,t,ce, 'HighFlowSingleInletGadoxetate2DSPGR_Rat')
        else:
            ct = Ve*ce + Khe*tools.integrate(ce,t)
        
        # Convert to signal
        St_rel = tools.spgr2d_func_inv(r1, FA, TR, R10t, ct)
        
        #Return tissue signal relative to the baseline St/St_baseline
        return(St_rel) 
    except RuntimeWarning as rtw:
            print ("Runtime Warning : " + str(rtw))
    except Exception as e:
        print('Error in function HighFlowSingleInletGadoxetate2DSPGR_Rat ' + str(e) )
                

#*************************************************************************************
#** model 2 definition
#************************************************************************************
def HighFlowSingleInletGadoxetate3DSPGR_Rat(inputData,Ve, Kbh, Khe,constantsString):
    """This function contains the algorithm for calculating 
       how the MR signal from a 3D scan varies with time using the 
       High Flow Single Inlet Two Compartment Gadoxetate Model.
        
            Input Parameters
            ----------------
                inputData - time and AIF concentration 1D arrays 
                    stacked into one 2D array.
                Ve - Plasma Volume Fraction (decimal fraction).
                Khe - Hepatocyte Uptake Rate (mL/min/mL)
                Kbh - Biliary Efflux Rate (mL/min/mL) 
                constantsString - A string representation of a dictionary of constant name:value pairs.
            Returns
            -------
            St_rel - list of calculated MR signals at each of the 
                time points in array 'time'.
            """ 
    #try:
        #exceptionHandler.modelFunctionInfoLogger()
    try:
        t = inputData[:,0]
        Sa = inputData[:,1]
        # Unpack SPGR model constants from 
        # a string representation of a dictionary
        # of constants and their values
        constantsDict = eval(constantsString) 
        TR, baseline, FA, r1, R10a, R10t = float(constantsDict['TR']), \
        int(constantsDict['baseline']),\
        float(constantsDict['FA']), float(constantsDict['r1']), \
        float(constantsDict['R10a']), float(constantsDict['R10t']) 
        # Convert to concentrations
        # n_jobs set to 1 to turn off parallel processing
        # because parallel processing caused a segmentation
        # fault in the compiled version of this application.
        # This is not a problem in the uncompiled script
        R1a = [Parallel(n_jobs=1)(delayed(scipyTools.fsolve)
          (tools.spgr3d_func, x0=0, 
           args = (FA, TR, R10a, baseline, Sa[p])) 
           for p in np.arange(0,len(t)))]
        R1a = np.squeeze(R1a)
        
        ca = (R1a - R10a)/r1
        
        # Correct for spleen Ve
        ve_spleen = 0.43
        ce = ca/ve_spleen
        Th = (1-Ve)/Kbh
        ct = Ve*ce + Khe*Th*tools.expconv(Th,t,ce,'HighFlowSingleInletGadoxetate3DSPGR_Rat')
        
        # Convert to signal
        St_rel = tools.spgr3d_func_inv(r1, FA, TR, R10t, ct)
        
        return(St_rel) #Returns tissue signal relative to the baseline St/St_baseline
    except RuntimeWarning as rtw:
            print ("Runtime Warning : " + str(rtw))
    except Exception as e:
        print('Error in function HighFlowSingleInletGadoxetate3DSPGR_Rat ' + str(e) )


#*******************************************************************************
#** Define constants for both models
#*******************************************************************************
def setUpConstants():
    """
    This optional function returns a list of constant objects.

    An object is created for each constant using the ModelConstant class 
    and added to the list, that is returned by this function.

    In the returnModelList function, this function is used to 
    populate the constantList argument. 
    """
    constantList = []
    TR = ModelConstant(shortName='TR', longName=None, defaultValue=0.013, stepSize=0.001,
                       precision=4, units = None, minValue=0, maxValue=0.1, listValues=[])
    constantList.append(TR)

    baseLineValues = [str(x) for x in range(1,11,1)]
    baseline = ModelConstant(shortName='baseline', longName='baseline', 
                             defaultValue=1, stepSize=None,
                       precision=1, units = None, minValue=1, maxValue=10, listValues=baseLineValues)
    constantList.append(baseline)

    valuesFA = [str(x) for x in range(10,31,1)]
    FA = ModelConstant(shortName='FA', longName=None, 
                             defaultValue=20, stepSize=None,
                       precision=1, units = None, minValue=10, maxValue=30, listValues=valuesFA)
    constantList.append(FA)
  
    r1 = ModelConstant(shortName='r1', longName=None, 
                             defaultValue=5.5, stepSize=0.1,
                       precision=1, units = None, minValue=5, maxValue=6, listValues=[])
    constantList.append(r1)

    R10a = ModelConstant(shortName='R10a', longName=None, 
                             defaultValue=0.74575, stepSize=0.1,
                       precision=5, units = None, minValue=0.5, maxValue=1.0, listValues=[])
    constantList.append(R10a)

    R10t = ModelConstant(shortName='R10t', longName=None, 
                             defaultValue=1.3203, stepSize=0.1,
                       precision=4, units = None, minValue=1.0, maxValue=2.0, listValues=[])
    constantList.append(R10t)
    return constantList

#*******************************************************************************
#** Define parameters for both models
#*******************************************************************************
def setUpParameters():
    """
    This optional function returns a list of parameter objects.

    An object is created for each parameter using the ModelParameter class 
    and added to the list, that is returned by this function.

    In the returnModelList function, this function is used to 
    populate the parameterList argument. 
    """
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
    hepatocyteUptakeRate = ModelParameter(shortName='Khe',
                                        longName='Hepatocyte Uptake Rate',
                                        units='mL/min/mL', 
                                        defaultValue=2.358, 
                                        stepSize=0.1, 
                                        precision=3, 
                                        minValue=0.0001, 
                                        maxValue=100.0)
    paramList.append(hepatocyteUptakeRate)    
    return paramList


#*******************************************************************************
# Define variables for both models
#*******************************************************************************
def setUpVariables():
    """
    This optional function returns a list of variable objects.

    An object is created for each variable using the ModelVariable class 
    and added to the list, that is returned by this function.

    In the returnModelList function, this function is used to 
    populate the variablesList argument. 
    """
    variablesList = []
    regionOfInterest = ModelVariable('ROI', 'Region of Interest', LineColours.blueLine, False, True)
    variablesList.append(regionOfInterest)

    arterialInputFunction = ModelVariable('AIF', 'Arterial Input Function', LineColours.redLine, True, False)
    variablesList.append(arterialInputFunction)
    return variablesList


def returnModelList():
    """
    This mandatory function returns a list of Model objects.

    Every model library module must contain an implementation of this function.

    An object is created for each mathematic model using the Model class 
    and added to the list, that is returned by this function.
    """
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


def returnDataFileFolder():
    """
    An optional function that returns the file path to the folder containing 
    CSV data files that form the input to Ferret.
    """
    return 'FerretData'