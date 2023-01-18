from app.helperFunctions.jsonFileHandling import dumpJsonFile
import requests
from decouple import config
import sys
import logging
from app.rootDir import ROOT_DIR



logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s -- [src] - %(filename)s, [func] - %(funcName)s, [line] - %(lineno)d', filename=ROOT_DIR + r'\logFiles\requestMetOfficeData.log', filemode='w', level=logging.INFO)
requestMetOfficeDataLog = logging.getLogger()



def requestMetOfficeData(url: str, filename: str):
    try:
        r = requests.get(f'{config("MET_OFFICE_ROOT_URL")}{url}{config("MET_OFFICE_API_KEY")}')

        if r.status_code != 200:
            requestMetOfficeDataLog.critical(f"STATUS_CODE_ERROR: Status code = {r.status_code} Unable to retrieve data from URL = {config('MET_OFFICE_ROOT_URL')}{url}{config('MET_OFFICE_API_KEY')}")
            raise Exception(f"STATUS_CODE_ERROR: Status code = {r.status_code} Unable to retrieve data from URL = {config('MET_OFFICE_ROOT_URL')}{url}{config('MET_OFFICE_API_KEY')}")
        else:
            data = r.json()
            dumpJsonFile(filename, data)
    except requests.exceptions.RequestException as err:
        requestMetOfficeDataLog.critical(f"REQUEST_ERROR: Request Failed! Unable to retrieve data from URL = {config('MET_OFFICE_ROOT_URL')}{url}{config('MET_OFFICE_API_KEY')}")
        requestMetOfficeDataLog.critical(f"Process terminating.")
        sys.exit(1)    
    return None
