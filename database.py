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

config = json.load(open("database_config.json"))

mydb = mysql.connector.connect(
    host=config["host"],
    user=config["user"],
    password=config["password"],
    database=config["database"]
)

mycursor = mydb.cursor()

def fetch_placeid(InputAddress):
    global mydb
    global mycursor

    mycursor.execute("SELECT placeid FROM userinput WHERE inputaddress = %s", (InputAddress,))

    myresult = mycursor.fetchall()

    return myresult

def insert_data(InputAddress, PlaceID, lon, lat, FormattedAddress, OSMnode):
    global mydb
    global mycursor

    input_code = "INSERT INTO userinput (inputaddress, placeid) VALUES (%s, %s)"
    output_code = "INSERT INTO maptable (placeid, coorx, coory, googleaddresses, openmnode) VALUES (%s, %s, %s, %s, %s)"

    try:
        mycursor.execute(input_code, (InputAddress, PlaceID,))
    except mysql.connector.Error as err:
        # print("Something went wrong: " + str(err))
        l = "l"
    try:
        mycursor.execute(output_code, (PlaceID, lon, lat, FormattedAddress, OSMnode))
    except mysql.connector.Error as err:
        # print("Something went wrong: " + str(err))
        l = "l"

    mydb.commit()

def fetch_output_data(PlaceID):
    global mydb
    global mycursor

    mycursor.execute("SELECT openmnode, googleaddresses FROM maptable WHERE placeid = %s", (PlaceID,))

    myresult = mycursor.fetchall()

    return myresult

def purge_data(no_of_year):
    global mydb
    global mycursor

    del_userinput = "DELETE FROM userinput WHERE last_updated < CURRENT_DATE - INTERVAL %s YEAR"

    try:
        mycursor.execute(del_userinput , (no_of_year,))
    except mysql.connector.Error as err:
        mydb.rollback()
        print("Something went wrong: " + str(err))
    mydb.commit()
