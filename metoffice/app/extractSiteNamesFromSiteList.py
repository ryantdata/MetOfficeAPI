import json
import sys
import os
import logging 



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s -- [src] - %(filename)s, [func] - %(funcName)s, [line] - %(lineno)d', filename=ROOT_DIR + r'\logFiles\extractSiteNames.log', filemode='w', level=logging.INFO)
extractNamesLog = logging.getLogger()



def extractSiteNames():

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    SITE_NAMES_FILE = ROOT_DIR + r'\downloadedData\siteNames.txt'
    SITE_LIST_FILE = ROOT_DIR + r'\downloadedData\siteList.txt'

    if os.path.exists(SITE_NAMES_FILE):
        open(SITE_NAMES_FILE, 'w').close()
    try:
        with open(SITE_LIST_FILE) as file:
            siteList = json.load(file)
    except OSError:
        extractNamesLog.critical(f"OS_ERROR: Unable to open file {SITE_LIST_FILE}!\n{OSError}")
        extractNamesLog.critical(f"Process terminating.")
        sys.exit(1)

    locations = siteList['Locations']['Location']
    siteNames = []
    for location in locations:
        siteNames.append(location['name'])

    try:
        with open(SITE_NAMES_FILE, 'w', encoding='utf-8') as f:
            json.dump(siteNames, f, ensure_ascii=False, indent=4)
    except OSError:
        extractNamesLog.critical(f"OS_ERROR: Unable to open file {SITE_NAMES_FILE}!\n{OSError}")
        extractNamesLog.critical(f"Process terminating.")
        sys.exit(1)



if __name__=="__main__":
    extractSiteNames()