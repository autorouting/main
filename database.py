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

## TESTING ##
if __name__ == "__main__":
    # Input: Chapel Hill, NC
    # Expected Output: ChIJp35uIRzDrIkRy-RDBOC6A38
    insert_data("Chapel Hill, NC", "ChIJp35uIRzDrIkRy-RDBOC6A38", -79.0558445, 35.9131996, "Chapel Hill, NC, USA", "179860")
    print(fetch_placeid("Chapel Hill, NC"))