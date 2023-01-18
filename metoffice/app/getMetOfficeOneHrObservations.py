import os
from app.helperFunctions.requestMetOfficeData import requestMetOfficeData



def requestMetOfficeOneHrObservations():

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    ONE_HR_OBSERVATIONS_URL = 'val/wxobs/all/json/all?res=hourly&'
    ONE_HR_OBSERVATIONS_FILE = ROOT_DIR + r'\downloadedData\oneHrObservations.txt'

    if os.path.exists(ONE_HR_OBSERVATIONS_FILE):
        open(ONE_HR_OBSERVATIONS_FILE, 'w').close()

    requestMetOfficeData(url=ONE_HR_OBSERVATIONS_URL, filename=ONE_HR_OBSERVATIONS_FILE)   



if __name__=="__main__":
    requestMetOfficeOneHrObservations()