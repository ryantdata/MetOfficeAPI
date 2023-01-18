import os
import sys
from decouple import config
from app.sqlQueries import INSERT_INTO_OBSERVATIONS
from app.helperFunctions.keyErrorChecking import dataProcessingLog, checkIfKeyExistsCritical, checkIfKeyExistsWarning
from app.helperFunctions.jsonFileHandling import readJsonFile
from app.helperFunctions.dbConnect import createConnectionToRemoteDatabase
from app.helperFunctions.uploadRecordToServerDatabase import uploadRecordToServerDatabase


# NOTE THIS SCRIPT PROCESSES THE JSON MET OFFICE DATA AND SENDS ALERTS FOR MISSING DATA AND INCORRECT FORMAT.
#
# THE FOLLOWING IS AN EXAMPLE OF THE RELEVANT PARTS OF THE EXPECTED DATA FORMAT.
#
# data = {'SiteRep': 
#           'DV': {
#               'Location': [
#                   {'i': 'locationId',
#                    'name': 'locationName'
#                    'Period': [
#                       {'value': 'date', 
#                        'Rep': [
#                           {'keys': 'values'},
#                           {'keys': 'values'},
#                           {'keys': 'values'},
#                        ]},
#                       {'value': 'date', 
#                        'Rep': [
#                           {'keys': 'values'},
#                           {'keys': 'values'},
#                           {'keys': 'values'},
#                        ]},
#                     ]},
#                    {'i': 'locationId',
#                     'name': 'locationName'
#                     'Period': [
#                         {'value': 'date', 
#                          'Rep': [
#                             {'keys': 'values'},
#                             {'keys': 'values'},
#                             {'keys': 'values'},
#                          ]},
#                         {'value': 'date', 
#                          'Rep': [
#                             {'keys': 'values'},
#                             {'keys': 'values'},
#                             {'keys': 'values'},
#                          ]},
#                       ]},
#                ]
#          }
#     }
#
# NOTE 
#
#   'SiteRep' may only be a <dict>
#   'DV' may only be a <dict>
#   'Location' may only be a <list>
#   'Period' may be either a <list> or <dict>
#   'Rep' may be either a <list> or <dict>



def uploadOneHrObs():

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    observationData = readJsonFile(ROOT_DIR + r'\downloadedData\oneHrObservations.txt')



    keys = ['SiteRep', 'DV', 'Location']
    for key in keys:
        observationData = checkIfKeyExistsCritical(data=observationData, key=key)
        if observationData == 1:
            sys.exit()



    validObservationData = []
    for location in observationData:
        if checkIfKeyExistsCritical(data=location, key='i') == 1:
            continue
        if checkIfKeyExistsCritical(data=location, key='Period') == 1:
            continue
        validObservationData.append(location)



    # NOTE 
    #
    # Each location is expected to have 2 periods, with each period as an element in a list.
    # However, a location may only have one period which is stored as a dict instead of a list.
    # Therefore, it is easiest to split the data types.
    #
    validObservationDataList = []
    validObservationDataDict = []
    missingPeriodCount = 0
    expectedNumberOfPeriods = len(validObservationDataList) + 2*len(validObservationDataDict)
    for location in validObservationData:
        if isinstance(location['Period'], list):
            validObservationDataList.append({'i': location['i'], 'Period': location['Period']})
        elif isinstance(location['Period'], dict):
            dataProcessingLog.warning(f"MISSING_DATA! Missing period for location {location['name']} (id={location['i']}).")  
            validObservationDataDict.append({'i': location['i'], 'Period': location['Period']})    
            missingPeriodCount += 1    
        else:
            dataProcessingLog.warning(f"MISSING_DATA! No data for location {location['name']} (id={location['i']}).")   
            missingPeriodCount += 2     
    dataProcessingLog.warning(f"MISSING_PERIOD_COUNT! {missingPeriodCount} periods missing for location {location['name']} (id={location['i']}).")  
    missingThreshold = 0.5
    if missingPeriodCount >= expectedNumberOfPeriods * missingThreshold:
        # SEND ALERT
        pass



    periods = []
    for location in validObservationDataList:
        for period in location['Period']:
            periodDate = checkIfKeyExistsWarning(data=period, key='value')
            if periodDate == 1:
                continue
            hoursInPeriod = checkIfKeyExistsWarning(data=period, key='Rep')
            if hoursInPeriod == 1:
                continue
            periods.append({'Location': location['i'], 'Date': periodDate, 'Hours': hoursInPeriod})
    for location in validObservationDataDict:
        periodDate = checkIfKeyExistsWarning(data=location['Period'], key='value')
        if periodDate == 1:
            continue
        hoursInPeriod = checkIfKeyExistsWarning(data=location['Period'], key='Rep')
        if hoursInPeriod == 1:
            continue       
        periods.append({'Location': location['i'], 'Date': periodDate, 'Hours': hoursInPeriod})



    # NOTE
    # NUMBER OF MISSING HOURS CALCULATION
    # 
    # Each location can have a maximum of 25 hours worth of data. These hours are usually split between two periods (depending on the time of the request).
    # The amount of hours in each period varies (depending on the time of the request).
    # The sum of the hours in the periods should be 25. So we can get the expected number of hours by multiplying the expected number of periods by 25 and dividing by 2.
    #
    # To get the number of missing hours, it's best to calculate (25 - number of hours in period) for each period.  Since each pair of periods should sum to 25, the leftover should equal 25.
    # Then for each location, we need to subtract 25 to get the missing number of hours for the location.
    #
    # Example: 20 hours in period1 and 5 hours in period2. -> (25 - 20) + (25-5) = 5 + 20 = 25 - 25 = 0 missing hours.
    # Example: 18 hours in period1 and 3 hours in period2. -> (25 - 18) + (25-3) 7 + 22 = 29 - 25 = 4 missing hours for location.
    #  
    # The easiest way to do this is to sum the leftover over all locations and then subtract (expected number of hours) to get the correct number of missing hours.
    #
    hoursList = []
    hoursDict = []
    missingHoursCount = 0
    expectedNumberOfhours = int(25*(expectedNumberOfPeriods)*0.5)
    for period in periods:
        if isinstance(period['Hours'], list):
            hoursList.append(period)
            missingHours = 25 - len(period['Hours'])
            missingHoursCount += missingHours
        elif isinstance(period['Hours'], dict):
            dataProcessingLog.warning(f"MISSING_DATA! Only one hour exists for period {period['Location']} - {period['Date']}.")  
            hoursDict.append(period)
            missingHoursCount += 24
        else:
            dataProcessingLog.warning(f"MISSING_DATA! No data for period {period['Location']} - {period['Date']}.")
            continue
    totalMissingHours = missingHoursCount - expectedNumberOfhours
    missingThreshold = 0.5
    if totalMissingHours >= expectedNumberOfhours * missingThreshold:
        # SEND ALERT
        pass


    DATABASE_DETAILS = {
        'DATABASE': config('DB_NAME'),
        'USER': config('DB_USERNAME'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'PASSWORD': config('DB_PASSWORD'),
    }
    dbConnection = createConnectionToRemoteDatabase(databaseDetails=DATABASE_DETAILS)   
    dbCursor = dbConnection.cursor()
    categories = ['$', 'G', 'T', 'V', 'D', 'S', 'W', 'P', 'Pt', 'Dp', 'H']
    for period in hoursList:
        for hour in period['Hours']:
            values = {}
            for category in categories:
                try:
                    value = hour[category]
                except KeyError:
                    value = None
                values[category] = value
            record = (period['Location'], period['Date'], values['$'], values['G'], values['T'], values['V'], values['D'], values['S'], values['W'], values['P'], values['Pt'], values['Dp'], values['H'])        
            dataProcessingLog.info(record)
            if uploadRecordToServerDatabase(connection=dbConnection, cursor=dbCursor, query=INSERT_INTO_OBSERVATIONS, record=record):
                dataProcessingLog.info("SUCCESS: Record uploaded!")
            else:
                dataProcessingLog.info("ERROR: Unable to upload record!")  
    for period in hoursDict:
        values = {}
        for category in categories:
            try:
                value = period['Hours'][category]
            except KeyError:
                value = None
            values[category] = value
        record = (period['Location'], period['Date'], values['$'], values['G'], values['T'], values['V'], values['D'], values['S'], values['W'], values['P'], values['Pt'], values['Dp'], values['H'])        
        dataProcessingLog.info(record)
        if uploadRecordToServerDatabase(connection=dbConnection, cursor=dbCursor, query=INSERT_INTO_OBSERVATIONS, record=record):
            dataProcessingLog.info("SUCCESS: Record uploaded!")
        else:
            dataProcessingLog.info("ERROR: Unable to upload record!")        
    dbCursor.close()
    dbConnection.commit()



if __name__=="__main__":
    uploadOneHrObs()