from flask import Flask
import sys
from housing.logger import logging 
from housing.exception import HousingException
#from markupsafe import escape

app=Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def index():
    try:
        raise Exception("We are testing custom exeception")
    except Exception as e:
        raise HousingException(e, sys) from e
        housing = HousingException(e,sys)
        logging.info(housing.error_message)
        logging.info("We are pasting logging module")
    return "Starting Machine Learning Project CI CD"

if __name__=="__main__":
    app.run(debug=True)