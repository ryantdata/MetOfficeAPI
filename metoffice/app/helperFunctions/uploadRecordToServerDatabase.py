import psycopg2
from app.helperFunctions.dbConnect import dbConnectionLog



def uploadRecordToServerDatabase(connection, cursor, query, record):
    try:
        cursor.execute(query, record)
        return True
    except psycopg2.errors.UniqueViolation:
        dbConnectionLog.info("UNIQUE_VIOLATION: Record already exists!")
    except psycopg2.errors.InFailedSqlTransaction:
        connection.rollback()
        dbConnectionLog.info("CURSOR_ROLLBACK: Previous record cleared from cursor.")
    return None
