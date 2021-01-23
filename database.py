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

def fetch_placeid(placeid):
    config = json.load(open("database_config.json"))

    mydb = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT placeid FROM userinput")

    myresult = mycursor.fetchall()

    return myresult

## TESTING ##
if __name__ == "__main__":
    print(fetch_placeid("ChIJp35uIRzDrIkRy-RDBOC6A38"))