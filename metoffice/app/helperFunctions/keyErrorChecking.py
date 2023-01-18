import logging
from app.rootDir import ROOT_DIR



logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s -- [src] - %(filename)s, [func] - %(funcName)s, [line] - %(lineno)d', filename=ROOT_DIR + r'\logFiles\dataProcessingLog.log', filemode='w', level=logging.INFO)
dataProcessingLog = logging.getLogger()




def checkIfKeyExistsCritical(data, key):
    try:
        data = data[key]
        return data
    except KeyError:
        dataProcessingLog.critical(f"KEY_ERROR! {key} key does not exist.")   
        # SEND ALERT
        return 1 
    except TypeError:
        dataProcessingLog.critical(f"TYPE_ERROR! For key {key}, expected {type({})} but got type {type(data)}.")  
        # SEND ALERT
        return 1 



def checkIfKeyExistsWarning(data, key):
    try:
        data = data[key]
        return data
    except KeyError:
        dataProcessingLog.warning(f"KEY_ERROR! {key} key does not exist.")  
        return 1 
    except TypeError:
        dataProcessingLog.warning(f"TYPE_ERROR! For key {key}, expected {type({})} but got type {type(data)}.")  
        return 1 

