import psycopg2
import sys
import logging
from app.rootDir import ROOT_DIR


logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s -- [src] - %(filename)s, [func] - %(funcName)s, [line] - %(lineno)d', filename=ROOT_DIR + r'\logFiles\dbConnection.log', filemode='w', level=logging.INFO)
dbConnectionLog = logging.getLogger()



def createConnectionToRemoteDatabase(databaseDetails: dict):
    try:
        dbConnection = psycopg2.connect(
            database = databaseDetails['DATABASE'], 
            user = databaseDetails['USER'], 
            host = databaseDetails['HOST'], 
            port = databaseDetails['PORT'], 
            password = databaseDetails['PASSWORD']
        )
        dbConnectionLog.info(f"SUCCESS: Successfully Connected to database {databaseDetails['DATABASE']}!")
    except psycopg2.OperationalError:
        dbConnectionLog.critical(f"DB_CONNECTION_ERROR: Unable to connect to database {databaseDetails['DATABASE']}!")
        dbConnectionLog.critical(f"Process terminating.")
        sys.exit(1)
    return dbConnection

