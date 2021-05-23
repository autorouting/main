import mysql.connector
import json

"""
CREATE THE FOLLOWING database_config.json
{
    "host":"HOSTNAME",
    "user":"USERNAME",
    "password":"PASSWORD",
    "database":"DATABASENAME"
}
"""

def fetch_placeid(InputAddress):
    """
    Fetch corresponding placeid from database

    Parameters:
    InputAddress (string): The address inputed by user.

    Returns:
    string: The corresponding id for address in databse.
    """
    config = json.load(open("database_config.json"))

    mydb = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT placeid FROM userinput WHERE inputaddress = %s", (InputAddress,))

    myresult = mycursor.fetchall()

    return myresult

def insert_data(InputAddress, PlaceID, lon, lat, FormattedAddress):
    """
    Add row to data base

    Parameters:
    InputAddress (string): The address inputed by user.
    PlaceID (string): The placeid address inputed by user.
    lon (integer): The longitude of the address.
    lat (integer): The latitude of the address.
    FormattedAddress (string): The address produced by google maps.

    Returns:
    No return.
    """
    config = json.load(open("database_config.json"))

    mydb = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )

    mycursor = mydb.cursor()

    input_code = "INSERT INTO userinput (inputaddress, placeid) VALUES (%s, %s)"
    output_code = "INSERT INTO maptable (placeid, coorx, coory, googleaddresses) VALUES (%s, %s, %s, %s)"

    try:
        mycursor.execute(input_code, (InputAddress, PlaceID,))
    except mysql.connector.Error as err:
        # print("Something went wrong: " + str(err))
        l = "l"
    try:
        mycursor.execute(output_code, (PlaceID, lon, lat, FormattedAddress))
    except mysql.connector.Error as err:
        # print("Something went wrong: " + str(err))
        l = "l"

    mydb.commit()

def fetch_output_data(PlaceID):
    """
    Fetch corresponding coordinate and address.

    Parameters:
    placeid (string): The placeid of the address inputed by user.

    Returns:
    list: The corresponding longitude, latitude, and address from google maps
    """
    config = json.load(open("database_config.json"))

    mydb = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT coorx, coory, googleaddresses FROM maptable WHERE placeid = %s", (PlaceID,))

    myresult = mycursor.fetchall()

    return myresult

def purge_data(no_of_year):
    """
    Purge data in database

    Parameters:
    no_of_year (integer): How many years worth of data to delete.

    Returns:
    No return
    """
    config = json.load(open("database_config.json"))

    mydb = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )
    mycursor = mydb.cursor()

    del_userinput = "DELETE FROM userinput WHERE last_updated < CURRENT_DATE - INTERVAL %s YEAR"

    try:
        mycursor.execute(del_userinput , (no_of_year,))
    except mysql.connector.Error as err:
        mydb.rollback()
        print("Something went wrong: " + str(err))
    mydb.commit()
