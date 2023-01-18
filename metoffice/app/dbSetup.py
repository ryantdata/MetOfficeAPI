from decouple import config
from app.helperFunctions.dbConnect import createConnectionToRemoteDatabase
from app.sqlQueries import CREATE_LOCATION_METADATA_TABLE, CREATE_OBSERVATIONS_TABLE, CREATE_CATEGORY_METADATA_TABLE
import psycopg2
import logging 
import os
import sys 

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s -- [src] - %(filename)s, [func] - %(funcName)s, [line] - %(lineno)d', filename=ROOT_DIR + r'\logFiles\dbSetup.log', filemode='w', level=logging.INFO)
dbSetupLog = logging.getLogger()



def dbSetup():

    CREATE_TABLES = [
        CREATE_LOCATION_METADATA_TABLE,
        CREATE_OBSERVATIONS_TABLE,
        CREATE_CATEGORY_METADATA_TABLE,
    ]
    DATABASE_DETAILS = {
        'DATABASE': config('DB_NAME'),
        'USER': config('DB_USERNAME'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'PASSWORD': config('DB_PASSWORD'),
    }
    try:
        dbConnection = createConnectionToRemoteDatabase(databaseDetails=DATABASE_DETAILS)
        dbCursor = dbConnection.cursor()
        for QUERY in CREATE_TABLES:
            dbCursor.execute(QUERY)
        dbConnection.close()
        dbConnection.commit()
        dbSetupLog.info(f"SUCCESS: Database {config('DB_NAME')} setup successful!")
    except (Exception, psycopg2.DatabaseError) as dbSetupError:
        dbSetupLog.critical(f"DB_CONNECTION_ERROR: Database {config('DB_NAME')} setup unsuccessful! \n {dbSetupError}")
        dbSetupLog.critical(f"Process terminating.")
        sys.exit(1)
    finally:
        if dbConnection is not None:
            dbConnection.close()
            dbSetupLog.info(f"SUCCESS: Database {config('DB_NAME')} connection succesfully closed!")



if __name__=="__main__":
    dbSetup()