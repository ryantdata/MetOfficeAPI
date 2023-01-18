from decouple import config
from app.sqlQueries import INSERT_INTO_LOCATION_METADATA
from app.helperFunctions.jsonFileHandling import readJsonFile
from app.helperFunctions.uploadRecordToServerDatabase import uploadRecordToServerDatabase
import os
from app.helperFunctions.dbConnect import createConnectionToRemoteDatabase



def uploadLocationMetadataToServer():

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    siteList = readJsonFile(ROOT_DIR + r'\downloadedData\siteList.txt')
    locationsMetaData = siteList['Locations']['Location']
    DATABASE_DETAILS = {
        'DATABASE': config('DB_NAME'),
        'USER': config('DB_USERNAME'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'PASSWORD': config('DB_PASSWORD'),
    }
    dbConnection = createConnectionToRemoteDatabase(databaseDetails=DATABASE_DETAILS)
    dbCursor = dbConnection.cursor()
    metaDataCategories = ['id', 'name', 'region', 'unitaryAuthArea', 'longitude', 'latitude', 'elevation']
    values = {}
    for location in locationsMetaData:
        for category in metaDataCategories:
            try:        
                values[category] = location[category]
            except KeyError:
                values[category] = None
        record = (int(values['id']), values['name'], values['region'], values['unitaryAuthArea'], float(values['longitude']), float(values['latitude']), int(float(values['elevation'])))
        uploadRecordToServerDatabase(connection=dbConnection, cursor=dbCursor, query=INSERT_INTO_LOCATION_METADATA, record=record)
    dbCursor.close()
    dbConnection.commit()



if __name__=="__main__":
    uploadLocationMetadataToServer()