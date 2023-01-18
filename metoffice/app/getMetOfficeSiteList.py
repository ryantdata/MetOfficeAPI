import os
from app.helperFunctions.requestMetOfficeData import requestMetOfficeData



def requestMetOfficeSiteList():

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    SITELIST_URL = 'val/wxobs/all/json/sitelist?'
    SITELIST_FILE = ROOT_DIR + r'\downloadedData\siteList.txt'

    if not os.path.exists(SITELIST_FILE):
        requestMetOfficeData(url=SITELIST_URL, filename=SITELIST_FILE)



if __name__=="__main__":
    requestMetOfficeSiteList()