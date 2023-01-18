CREATE_LOCATION_METADATA_TABLE = """
    CREATE TABLE IF NOT EXISTS location_metadata (
        location_id         INTEGER            PRIMARY KEY,
        location_name       VARCHAR(50)        NOT NULL,
        region              VARCHAR(50),
        unitaryautharea     VARCHAR(50),
        longitude           DECIMAL(7,4),
        latitude            DECIMAL(7,4),
        elevation           INTEGER
    )
"""

CREATE_OBSERVATIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS observations (
        location_id                 INTEGER         NOT NULL,
        date                        DATE            NOT NULL,
        hour                        INTEGER         NOT NULL,
        wind_gust                   INTEGER,
        temperature                 DECIMAL(3,1),
        visibility                  INTEGER,
        wind_direction              VARCHAR(4),
        wind_speed                  INTEGER,
        weather_type                INTEGER,
        pressure                    INTEGER,
        pressure_tendency           VARCHAR(4),
        dew_point                   DECIMAL(3,1),
        screen_relative_humidity    DECIMAL(4,1),
        PRIMARY KEY(location_id, date, hour),
        FOREIGN KEY(location_id)
            REFERENCES location_metadata(location_id)    
                ON DELETE CASCADE
    )
"""

CREATE_CATEGORY_METADATA_TABLE = """
    CREATE TABLE IF NOT EXISTS category_metadata (
        category       VARCHAR(30)     PRIMARY KEY,
        units          VARCHAR(10)     NOT NULL,
        description    VARCHAR(200)    NOT NULL
    )
"""

INSERT_INTO_CATEGORY_METADATA = """
    INSERT INTO location_metadata (category, units, description) 
    VALUES (%s, %s, %s)
"""

INSERT_INTO_LOCATION_METADATA = """
    INSERT INTO location_metadata (location_id, location_name, region, unitaryautharea, longitude, latitude, elevation) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

INSERT_INTO_OBSERVATIONS = """
    INSERT INTO observations (location_id, date, hour, wind_gust, temperature, visibility, wind_direction, wind_speed, weather_type, pressure, pressure_tendency, dew_point, screen_relative_humidity) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""