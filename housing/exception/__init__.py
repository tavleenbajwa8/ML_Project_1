import os
import sys

#sys module has info of all the errors and line which is causing it 

class HousingException(Exception):
    

    def __init__(self, error_message:Exception,error_detail:sys):
        """
        Passing error info to parent class initializer
        
        """
        super().__init__(error_message)  
        self.error_message=HousingException.get_detailed_error_message(error_message=error_message,
                                                                        error_detail=error_detail
                                                                        )


    

    @staticmethod  #Can be called w/o creating object
    def get_detailed_error_message(error_message:Exception,error_detail:sys)->str:
        """
        We want to prepare a format(string) of error message and error detail
        for which we use staticmethod
        
        error_message:Exception object 
        error_detail: object of sys module 
        exc_info() returns type,value,traceback but we only want traceback so we will write
        _,_ for the first 2 variables
        """
       
        _,_ ,exec_tb = error_detail.exc_info()
        line_number = exec_tb.tb_frame.f_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"Error occured in script: [{file_name}] at line number: [{line_number}] error message: [{error_message}]"
        return error_message

    def __str__(self):
        return self.error_message



    def __repr__(self) -> str:
        return HousingException.__name__.str()
        