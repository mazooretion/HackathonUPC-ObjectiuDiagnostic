import pymysql

db = pymysql.connect(host='sql7.freemysqlhosting.net', user="sql7315715", password="LrhIW4WIhq", db="sql7315715")

#Disconnect server
db.close()


