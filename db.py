import pymysql

db = pymysql.connect(host='sql7.freemysqlhosting.net', user="sql7315715", password="LrhIW4WIhq", db="sql7315715")

#Prepare a cursor object using cursor() method
cursor = db.cursor()

#Create a table
#cursor.execute("CREATE TABLE `demoniac` (`id` INT NOT NULL AUTO_INCREMENT, `age` TEXT NOT NULL, PRIMARY KEY(`id`))")

#Fill a table with 1 test value
#cursor.execute("INSERT INTO `demoniac` (`age`) VALUES ('06/06/1996')")

#Execute the SQL query using execute() method
print ("Mi basura : ", cursor.execute("SELECT id FROM demoniac"))

#Process a unique line using fetchone() method
data = cursor.fetchone()

#Disconnect server
db.close()

print ("Database version : {0}".format(data))

