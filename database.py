import mysql.connector

"""
CREATE THE FOLLOWING database_config.json
{
    "host":"HOSTNAME",
    "user":"USERNAME",
    "password":"PASSWORD"
}
"""

mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)