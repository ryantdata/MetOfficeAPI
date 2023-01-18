THIS APP IS A PIPELINE FOR DOWNLOADING MET OFFICE HOURLY WEATHER DATA.

PROJECT AIM: A small data engineering project to build a small pipeline that is robust to changes in requested data and alerts the user to any problems. The
app can be scheduled to run autonomously. 

The app performs 3 main operations:

1. Downloads hourly observational weather data for hundreds of weather station locations in the UK. 
2. Performs data format missing data checking with logging.
3. Uploads the processed data to a remote Postgres database.

The app also contains scripts for retrieving and storing metadata from the met office API.
There are comment placeholders for an alert system which would notify the user of any critical error which caused the autonomous process to
be interupted.

The file named 'uploadOneHrObsToServer' is the script which should be scheduled.

A .env file should be setup in the metoffice/app directory with the following parameters:

DB_NAME = name of database
DB_USERNAME = database username
DB_HOST = database host
DB_PORT = database port
DB_PASSWORD = database password
MET_OFFICE_API_KEY = api key to use the met office datapoint API
MET_OFFICE_ROOT_URL = 'http://datapoint.metoffice.gov.uk/public/data/'
