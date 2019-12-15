import pymysql

db = pymysql.connect(host='sql7.freemysqlhosting.net', user='sql7315715', password='LrhIW4WIhq', db='sql7315715')

cursor = db.cursor()

#cursor.execute("CREATE TABLE `users` (`id` INT NOT NULL, `name` TEXT NOT NULL, `age` INT NOT NULL, `sex` TEXT NOT NULL, latitude FLOAT, longitude FLOAT, PRIMARY KEY(`id`));")

def create(id, name, age, sex, latitude, longitude): 
    sqlinsert = ("INSERT INTO `users` (id, name, age, sex, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s);")
    cursor.execute(sqlinsert, (id, name, age, sex, latitude, longitude))

def getuser(id):
    sql = ("SELECT * FROM `users` WHERE id = %s")
    cursor.execute(sql, id)
    data = cursor.fetchone()
    print("Mi contenido es el siguiente: ", data)

def existuser(id):
    sql = ("SELECT COUNT(*) FROM `users` WHERE id = %s")
    cursor.execute(sql, id)
    data = cursor.fetchone()
    return data == 0

def updateuser(id, name, age, sex, latitude, longitude):
    sqlupdate = ("UPDATE `users` SET name = %s, age = %s, sex = %s, latitude = %s, longitude = %s WHERE id = %s")
    cursor.execute(sqlupdate, (name, age, sex, latitude, longitude, id))

# desconectar del servidor
db.close()