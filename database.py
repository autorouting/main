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

def main(placeid):
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

    print(myresult)

## TESTING ##
if __name__ == "__main__":
    print(main("ChIJp35uIRzDrIkRy-RDBOC6A38"))