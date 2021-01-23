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

def insert_data(InputAddress, PlaceID, lon, lat, FormattedAddress, OSMnode):
    config = json.load(open("database_config.json"))

    mydb = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )

    mycursor = mydb.cursor()

    input_code = "INSERT INTO userinput (inputaddress, placeid) VALUES (%s, %s)"
    output_code = "INSERT INTO maptable (placeid, coorx, coory, googleaddresses, openmnode) VALUES (%s, %s, %s, %s, %s)"

    mycursor.execute(input_code, (InputAddress, PlaceID,))
    mycursor.execute(output_code, (PlaceID, lon, lat, FormattedAddress, OSMnode))

    mydb.commit()

def fetch_output_data(PlaceID):
    config = json.load(open("database_config.json"))

    mydb = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT openmnode, googleaddresses FROM maptable WHERE placeid = %s", (PlaceID,))

    myresult = mycursor.fetchall()

    return myresult