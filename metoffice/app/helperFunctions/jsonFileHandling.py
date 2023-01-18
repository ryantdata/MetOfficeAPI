import json
import logging
from app.rootDir import ROOT_DIR



logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s -- [src] - %(filename)s, [func] - %(funcName)s, [line] - %(lineno)d', filename=ROOT_DIR + r'\logFiles\jsonFileHandling.log', filemode='w', level=logging.INFO)
jsonFileHandlingLog = logging.getLogger()



def readJsonFile(filename: str):
    try:
        with open(filename) as f:
            data = json.load(f)
            jsonFileHandlingLog.info(f'SUCCESS: Data retrieved from {filename} successfully!')
    except OSError:
        jsonFileHandlingLog.critical(f'OS_ERROR: Unable to open file {filename}!')
    return data



def dumpJsonFile(filename: str, data: dict):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        jsonFileHandlingLog.info(f'SUCCESS: Data saved to {filename} successfully!')
    except OSError:
        jsonFileHandlingLog.info(f'OS_ERROR: Unable to open file {filename}!')
    return None