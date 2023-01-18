from app import getMetOfficeOneHrObservations
from app import uploadOnehrObs
    


def uploadOneHrObsToServer():
    
    getMetOfficeOneHrObservations.requestMetOfficeOneHrObservations()
    uploadOnehrObs.uploadOneHrObs()



if __name__=="__main__":
    uploadOneHrObsToServer()