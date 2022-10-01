from setuptools import setup
from typing import List


#Declaring variables for setup functions so that we dont have to go to pip install -r requirements.txt

PROJECT_NAME="housing-predictor"
VERSION="0.0.1"
AUTHOR="Tavleen Bajwa"
DESCRIPTION="Housing predictor uses regression based modelling to predict accurate house prices"
PACKAGES=["housing"]
REQUIREMENT_FILE_NAME="requirements.txt"


#Using this function we are going to read requirements.txt file and return a list from that which has string value/s in it 
# -> means return
def get_requirements_list()->List[str]:
    """
    Description: This function is going to return list of
    requirements mentioned in requirements.txt file 

    return This function is going to return a list which will contain
    name of libraries mentioned  in requirements.txt file
    #.readlines return list[str]  
    
    """
    
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_file.readlines()   



setup(
name=PROJECT_NAME,
version=VERSION,
author=AUTHOR,
description=DESCRIPTION,
packages=PACKAGES,
install_requires=get_requirements_list()  #The returned list comes to install_requires

)




     