import numpy as np

class InputValidation:
    """
    This class contains static methods for the validation of variable type and 
    value.

    When a variable fails validation the appropriate error is raised for capture
    in the host function. 
    """
    @staticmethod
    def validatePositiveNumericVariable( var, variableName='VARIABLE NAME NOT DEFINED'):
        """
        Validates that a variable contains a positive numeric value.
        The number can be either a float or an integer

        If the validation fails because the variable does not contain
        a numeric value a TypeError is raised that 
        can be exception handled in the calling function. 

        If the validation fails because the number is not greater than
        zero (positive) a ValueError is raised.
        """
        if not isinstance(variableName, (str)):
            variableName='VARIABLE NAME NOT CORRECTLY DEFINED '
        if not isinstance(var, (int, float)):
            raise TypeError(variableName + " should be a number")
        if var < 0:
            raise ValueError(variableName + " should be greater than zero")


    @staticmethod
    def validateNumericVariable(var, variableName='VARIABLE NAME NOT DEFINED'):
        """
        Validates that a variable contains a  numeric value.
        The number can be either a float or an integer

        If the validation fails because the variable does not contain
        a numeric value a TypeError is raised that 
        can be exception handled in the calling function. 
        """
        if not isinstance(variableName, (str)):
            variableName='VARIABLE NAME NOT CORRECTLY DEFINED '
        if not isinstance(var, (int, float)):
            raise TypeError(variableName + " should be a number")
   

    @staticmethod
    def validateStringVariable(var, variableName='VARIABLE NAME NOT DEFINED'):
        """
        Validates that a variable contains a string.

        If the validation fails a TypeError is raised that 
        can be exception handled in the calling function.
        """
        if not isinstance(variableName, (str)):
            variableName='VARIABLE NAME NOT CORRECTLY DEFINED '
        if not isinstance(var, (str)):
            raise TypeError(variableName + " should be a string")
    

    @staticmethod
    def validateListVariable(var, variableName='VARIABLE NAME NOT DEFINED'):
        """
        Validates that a variable contains a list.

        If the validation fails a TypeError is raised that 
        can be exception handled in the calling function.
        """
        if not isinstance(variableName, (str)):
            variableName='VARIABLE NAME NOT CORRECTLY DEFINED '
        if not isinstance(var, (list)):
            raise TypeError(variableName + " should be a list")


    @staticmethod
    def validateNumpyArrayVariable(var, variableName='VARIABLE NAME NOT DEFINED'):
        """
        Validates that a variable contains a numpy array.

        If the validation fails a TypeError is raised that 
        can be exception handled in the calling function.
        """
        if not isinstance(variableName, (str)):
            variableName='VARIABLE NAME NOT CORRECTLY DEFINED '
        if not isinstance(var,np.ndarray):
            raise TypeError(variableName + " should be a numpy array")


    @staticmethod
    def validateArrayVariable(var, variableName='VARIABLE NAME NOT DEFINED'):
        """
        Validates that a variable contains a numpy array.

        If the validation fails a TypeError is raised that 
        can be exception handled in the calling function.
        """
        if not isinstance(variableName, (str)):
            variableName='VARIABLE NAME NOT CORRECTLY DEFINED '
        if not (isinstance(var,np.ndarray) or not isinstance(var, (list))):
            raise TypeError(variableName + " should be a numpy array or Python list")

