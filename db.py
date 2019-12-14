import pymysql

db = pymysql.connect("sql7.freemysqlhosting.net", "sql7315659", "SmpCiHqeWY", "sql7315659")

#Prepare a cursor object using cursor() method
cursor = db.cursor()

#Execute the SQL query using execute() method
cursor.execute("SELECT *")

#Process a unique line using fetchone() method
data = cursor.fetchone()
print ("Database version : {0}".format(data))

#Disconnect server
db.close()